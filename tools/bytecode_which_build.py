"""判定仓库源码中这 5 个模块分别对应 dev 还是 zip 构建。"""
import marshal
import os

MODS = ['qcl.core.paths', 'qcl.core.server', 'qcl.ui.pages.community',
        'qcl.ui.pages.multiplayer', 'qcl.ui.pages.settings_page']
SRC = r'c:\Users\Sapnap\CodeBuddy\QCL\qcl'


def consts(co, out):
    for c in co.co_consts:
        if isinstance(c, str):
            out.add(c)
        elif hasattr(c, 'co_consts'):
            consts(c, out)
    return out


def score(src_text, strings):
    hit = sum(1 for s in strings if s and len(s) > 3 and s in src_text)
    return hit / len(strings) if strings else 0.0


for m in MODS:
    rel = m.split('.', 1)[1].replace('.', os.sep) + '.py'
    p = os.path.join(SRC, rel)
    if not os.path.exists(p):
        print('%-32s MISSING %s' % (m, rel))
        continue
    text = open(p, encoding='utf-8').read()
    a = consts(marshal.loads(open('_pyc/dev/%s.pyc' % m, 'rb').read()[16:]), set())
    b = consts(marshal.loads(open('_pyc/zip/%s.pyc' % m, 'rb').read()[16:]), set())
    sa, sb = score(text, a), score(text, b)
    winner = 'dev' if sa > sb else ('zip' if sb > sa else 'tie')
    print('%-32s dev=%.3f  zip=%.3f  -> %s' % (m, sa, sb, winner))
