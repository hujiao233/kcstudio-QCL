"""反汇编 qcl 字节码中的指定函数，用于校正反编译结果。

用法:
    _dis.py <dev|zip> <module> [qualname]
    _dis.py dev qcl.core.constants              # 列出顶层名字
    _dis.py dev qcl.core.constants required_java
"""
import os, sys, marshal, dis

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir,
                    'bytecode')


def find_code(co, name):
    if co.co_name == name:
        return co
    for c in co.co_consts:
        if hasattr(c, 'co_consts'):
            r = find_code(c, name)
            if r is not None:
                return r
    return None


def walk(co, depth=0, prefix=''):
    if depth > 2:
        return
    print('  ' * depth + prefix + co.co_name)
    for c in co.co_consts:
        if hasattr(c, 'co_consts'):
            walk(c, depth + 1)


def main():
    tag, mod = sys.argv[1], sys.argv[2]
    # 模块按点分层存放：qcl.core.paths -> bytecode/<tag>/qcl/core/paths.pyc
    fp = os.path.join(BASE, tag, *mod.split('.')) + '.pyc'
    co = marshal.loads(open(fp, 'rb').read()[16:])
    if len(sys.argv) < 4:
        walk(co)
        return
    target = find_code(co, sys.argv[3])
    if target is None:
        sys.exit('not found: ' + sys.argv[3])
    dis.dis(target, depth=0)


main()
