"""删除 pycdc 对 with 语句 __exit__ 调用的错误渲染。

Python 3.11+ 的 with 依赖 BEFORE_WITH / WITH_EXCEPT_START 与 __exit__ 调用，
pycdc 会把它们渲染成独立语句 `None(None, None)` / `None(None, None, None)`。
这些是纯伪影，运行期会抛 TypeError（None 不可调用），必须清除。

判定"删除还是退化为 pass"不能用整文件编译校验（这些文件本身还带别的
语法错误，编译必然失败），改用缩进拓扑：若该伪影是其所在块的唯一语句
（前一条非空行是块头或更浅缩进，后一条非空行缩进更浅或是块续关键字），
删掉会留下空块，此时退化为 `pass`。
"""

import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir, 'qcl')

WHOLE = re.compile(r'^(\s*)None\(None, None(?:, None)?\)\s*$')
# 伪影被粘连在一条完整语句之后，例如 `f(x)None(None, x)`
TRAIL = re.compile(r'^(.*\)+)\s*None\((?:None, )*[A-Za-z_]\w*\)\s*$')
BLOCK_KW = re.compile(r'^\s*(except|else|elif|finally|case)\b')


def _ind(ln):
    return len(ln) - len(ln.lstrip())


def neighbours(lines, i):
    prev = next_ = ''
    for j in range(i - 1, -1, -1):
        if lines[j].strip():
            prev = lines[j]
            break
    for j in range(i + 1, len(lines)):
        if lines[j].strip():
            next_ = lines[j]
            break
    return prev, next_


def is_only_statement(lines, i):
    prev, nxt = neighbours(lines, i)
    cur = _ind(lines[i])
    first = (not prev) or prev.rstrip().endswith(':') or _ind(prev) < cur
    last = (not nxt) or _ind(nxt) < cur or bool(BLOCK_KW.match(nxt))
    return first and last


def fix_file(path):
    src = open(path, encoding='utf-8').read()
    lines = src.split('\n')
    deleted = passed = split = 0

    for i in range(len(lines)):
        ln = lines[i]
        m = WHOLE.match(ln)
        if m:
            if is_only_statement(lines, i):
                lines[i] = m.group(1) + 'pass'
                passed += 1
            else:
                lines[i] = ''
                deleted += 1
            continue
        m = TRAIL.match(ln)
        if m:
            lines[i] = m.group(1)
            split += 1

    out = '\n'.join(lines)
    if out != src:
        open(path, 'w', encoding='utf-8', newline='\n').write(out)
    return deleted, passed, split


tot = [0, 0, 0]
bad = []
for dp, dn, fn in os.walk(ROOT):
    for f in sorted(fn):
        if not f.endswith('.py'):
            continue
        p = os.path.join(dp, f)
        d, s, t = fix_file(p)
        tot[0] += d
        tot[1] += s
        tot[2] += t
        try:
            compile(open(p, 'rb').read(), p, 'exec')
        except SyntaxError:
            bad.append(os.path.relpath(p, ROOT))

print('deleted=%d  ->pass=%d  split=%d' % tuple(tot))
print('still bad: %d' % len(bad))
