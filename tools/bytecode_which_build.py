"""判定仓库源码对应 dev 还是 zip 构建。

用法:
    python bytecode_which_build.py            # 只判 5 个差异模块
    python bytecode_which_build.py --all      # 判全部模块

做法是比较源码里出现的字符串常量与字节码常量的命中率，高者为同源。
"""

import marshal
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, os.pardir, 'bytecode')
SRC = os.path.join(HERE, os.pardir, 'qcl')

# 两份构建中代码有差异的模块
DIFFERING = ['qcl.core.paths', 'qcl.core.server', 'qcl.ui.pages.community',
             'qcl.ui.pages.multiplayer', 'qcl.ui.pages.settings_page']


def consts(co, out):
    for c in co.co_consts:
        if isinstance(c, str):
            out.add(c)
        elif hasattr(c, 'co_consts'):
            consts(c, out)
    return out


def load(build, mod):
    fp = os.path.join(BASE, build, *mod.split('.')) + '.pyc'
    return consts(marshal.loads(open(fp, 'rb').read()[16:]), set())


def score(src_text, strings):
    if not strings:
        return 0.0
    hit = sum(1 for s in strings if s and len(s) > 3 and s in src_text)
    return hit / len(strings)


def main():
    if '--all' in sys.argv:
        mods = []
        for dirpath, _dirs, files in os.walk(os.path.join(BASE, 'dev')):
            for f in files:
                if f.endswith('.pyc'):
                    rel = os.path.relpath(os.path.join(dirpath, f),
                                          os.path.join(BASE, 'dev'))
                    mods.append(rel[:-4].replace(os.sep, '.'))
    else:
        mods = DIFFERING

    tally = {'dev': 0, 'zip': 0, 'tie': 0}
    for m in sorted(mods):
        rel = m.split('.', 1)[1].replace('.', os.sep) + '.py'
        p = os.path.join(SRC, rel)
        if not os.path.exists(p):
            print('%-32s MISSING %s' % (m, rel))
            continue
        text = open(p, encoding='utf-8').read()
        sa = score(text, load('dev', m))
        sb = score(text, load('zip', m))
        winner = 'dev' if sa > sb else ('zip' if sb > sa else 'tie')
        tally[winner] += 1
        if len(mods) > 5 or winner != 'dev':
            print('%-32s dev=%.3f  zip=%.3f  -> %s' % (m, sa, sb, winner))
    print('\n总计: %s' % tally)


if __name__ == '__main__':
    main()
