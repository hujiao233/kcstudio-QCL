"""反编译结果的后处理。

做三件事：
  1. 还原相对导入   —— pycdc 会丢掉 `from . import x` / `from .core import y` 中的点号
  2. 还原函数内的 from-import —— pycdc 会把 `from .core import a as b` 渲染成 `b = a` + `import core`
  3. 清理 Python 3.13 编译器产物与反编译器噪声

用法:
    python postprocess.py --root ..
"""

import argparse
import os
import re
import sys

# 这些顶层名字是第三方/标准库，不能被改写成相对导入
KNOWN_EXTERNAL = set("""os sys re json time math io shutil pickle ctypes threading subprocess
socket ssl struct zlib hashlib base64 uuid random tempfile pathlib glob fnmatch
collections itertools functools dataclasses enum typing traceback logging asyncio
urllib http platform stat string textwrap warnings weakref zipfile tarfile
requests urllib3 certifi idna charset_normalizer psutil PySide6 shiboken6
setuptools packaging distutils copy datetime calendar decimal fractions pprint
secrets hmac mimetypes webbrowser email html xml configparser argparse getpass
signal select errno queue contextlib importlib inspect ast dis marshal gc sysconfig
locale ipaddress winreg msvcrt mmap csv sqlite3 tkinter""".split())

DROP_LINE = [
    re.compile(r'^\s*__firstlineno__\s*=\s*\d+\s*$'),
    re.compile(r'^\s*__static_attributes__\s*='),
    re.compile(r'^\s*__classcell__\s*=\s*__class__\s*$'),
]
BARE_IMPORT = re.compile(r'^(\s*)import\s*$')
NODE_PLACEHOLDER = re.compile(r'<NODE:\d+>')
FROM_EMPTY = re.compile(r'^(\s*)from\s+import\s+(.+)$')
FROM_NAMED = re.compile(r'^(\s*)from\s+([A-Za-z_][\w.]*)\s+import\s+(.+)$')
LOCAL_FROM = re.compile(
    r'^(\s*)([A-Za-z_]\w*) = ([A-Za-z_]\w*)\s*\n\1import ([A-Za-z_][\w.]*)\s*$', re.M)


def collect_modules(root):
    mods = set()
    for dirpath, _dirs, files in os.walk(root):
        for f in files:
            if f.endswith('.py'):
                rel = os.path.relpath(os.path.join(dirpath, f), root)
                name = rel[:-3].replace(os.sep, '.')
                mods.add(name)
                if name.endswith('.__init__'):
                    mods.add(name[:-len('.__init__')])
    return mods


def resolve_level(parts, module, mods):
    """module 相对当前模块应在第几层包里，返回点号串或 None。"""
    for level in range(1, len(parts)):
        pkg = '.'.join(parts[:-level])
        if (pkg + '.' + module) in mods:
            return '.' * level
    return None


def fix_imports(root, mods):
    n = 0
    for dirpath, _dirs, files in os.walk(root):
        for f in sorted(files):
            if not f.endswith('.py'):
                continue
            fp = os.path.join(dirpath, f)
            parts = os.path.relpath(fp, root)[:-3].replace(os.sep, '.').split('.')
            lines = open(fp, encoding='utf-8').read().split('\n')
            changed = False
            for i, ln in enumerate(lines):
                m = FROM_EMPTY.match(ln)
                if m:                                     # `from  import x` -> `from . import x`
                    indent, names = m.group(1), m.group(2)
                    wanted = [x.strip().split(' as ')[0].strip() for x in names.split(',')]
                    dots = None
                    for level in range(1, len(parts)):
                        pkg = '.'.join(parts[:-level])
                        if all((pkg + '.' + w) in mods for w in wanted):
                            dots = '.' * level
                            break
                    if dots:
                        lines[i] = '%sfrom %s import %s' % (indent, dots, names)
                        changed = True
                        n += 1
                    continue

                m = FROM_NAMED.match(ln)
                if m:
                    indent, name, names = m.group(1), m.group(2), m.group(3)
                    if name.startswith('.') or name.split('.')[0] in KNOWN_EXTERNAL:
                        continue
                    dots = resolve_level(parts, name, mods)
                    if dots:
                        lines[i] = '%sfrom %s%s import %s' % (indent, dots, name, names)
                        changed = True
                        n += 1
            if changed:
                open(fp, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    return n


def fix_local_from(root, mods):
    total = [0]

    def repl(m, parts):
        indent, alias, name, module = m.group(1), m.group(2), m.group(3), m.group(4)
        dots = resolve_level(parts, module, mods)
        if dots is None:
            return m.group(0)
        total[0] += 1
        if alias == name:
            return '%sfrom %s%s import %s' % (indent, dots, module, name)
        return '%sfrom %s%s import %s as %s' % (indent, dots, module, name, alias)

    for dirpath, _dirs, files in os.walk(root):
        for f in sorted(files):
            if not f.endswith('.py'):
                continue
            fp = os.path.join(dirpath, f)
            parts = os.path.relpath(fp, root)[:-3].replace(os.sep, '.').split('.')
            txt = open(fp, encoding='utf-8').read()
            new = LOCAL_FROM.sub(lambda m: repl(m, parts), txt)
            if new != txt:
                open(fp, 'w', encoding='utf-8', newline='\n').write(new)
    return total[0]


def cleanup(root):
    n_drop = n_imp = n_node = 0
    for dirpath, _dirs, files in os.walk(root):
        for f in sorted(files):
            if not f.endswith('.py'):
                continue
            fp = os.path.join(dirpath, f)
            out, blank = [], 0
            for ln in open(fp, encoding='utf-8').read().split('\n'):
                if any(p.match(ln) for p in DROP_LINE):
                    n_drop += 1
                    continue
                m = BARE_IMPORT.match(ln)
                if m:
                    out.append('%s# import  # [decompiler] module name lost' % m.group(1))
                    n_imp += 1
                    continue
                if NODE_PLACEHOLDER.search(ln):
                    ln = NODE_PLACEHOLDER.sub('None', ln)
                    n_node += 1
                if ln.strip() == '':
                    blank += 1
                    if blank > 2:
                        continue
                else:
                    blank = 0
                out.append(ln)
            open(fp, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
    return n_drop, n_imp, n_node


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    args = ap.parse_args()

    mods = collect_modules(args.root)
    print('modules:', len(mods))
    print('relative imports restored:', fix_imports(args.root, mods))
    print('function-scope from-imports restored:', fix_local_from(args.root, mods))
    d, i, n = cleanup(args.root)
    print('artifact lines dropped: %d, bare imports commented: %d, placeholders: %d' % (d, i, n))
    return 0


if __name__ == '__main__':
    sys.exit(main())
