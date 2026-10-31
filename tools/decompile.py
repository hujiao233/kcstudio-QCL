"""调用 pycdc 把 qcl 包的 .pyc 反编译成 .py。

用法:
    python decompile.py --pyc work/pyc --pycdc /path/to/pycdc --out ..
"""

import argparse
import os
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pyc', required=True, help='存放 .pyc 的目录（含 qcl/ 与 qcl_entry.pyc）')
    ap.add_argument('--pycdc', required=True, help='pycdc 可执行文件路径')
    ap.add_argument('--out', required=True, help='源码输出根目录')
    args = ap.parse_args()

    ok = fail = 0
    for root, _dirs, files in os.walk(args.pyc):
        for f in sorted(files):
            if not f.endswith('.pyc'):
                continue
            src = os.path.join(root, f)
            rel = os.path.relpath(src, args.pyc)[:-4]
            if rel.replace(os.sep, '/') == 'qcl_entry':
                dst = os.path.join(args.out, 'qcl_entry.py')
            else:
                dst = os.path.join(args.out, rel + '.py')
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            r = subprocess.run([args.pycdc, src], capture_output=True)
            if r.returncode != 0 or not r.stdout.strip():
                fail += 1
                print('FAIL %s: %s' % (src, r.stderr.decode('utf-8', 'replace').strip()))
                continue
            open(dst, 'wb').write(r.stdout.replace(b'\r\n', b'\n'))
            ok += 1
    print('decompiled %d, failed %d' % (ok, fail))
    return 0 if fail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
