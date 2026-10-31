"""用真实的 Python 3.13 检查还原结果能否被解析，并报告首个语法错误的位置。

用法:
    python check_syntax.py --root .. --python313 /path/to/python3.13.exe
若省略 --python313，则用当前解释器（版本不同结果会略有差异）。
"""

import argparse
import os
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--python313')
    args = ap.parse_args()

    files = []
    for dirpath, _dirs, fs in os.walk(args.root):
        for f in sorted(fs):
            if f.endswith('.py') and 'tools' not in dirpath.replace('\\', '/').split('/'):
                files.append(os.path.join(dirpath, f))
    files.sort()

    script = r'''
import sys
bad = 0
for p in sys.argv[1:]:
    src = open(p, "rb").read()
    try:
        compile(src, p, "exec")
    except SyntaxError as e:
        bad += 1
        lines = src.decode("utf-8", "replace").split("\n")
        ln = e.lineno or 0
        print("SYNTAX %s:%s: %s" % (p, e.lineno, e.msg))
        for i in range(max(0, ln - 3), min(len(lines), ln + 2)):
            print("   %5d| %s" % (i + 1, lines[i][:110]))
print("checked %d, bad %d" % (len(sys.argv) - 1, bad))
'''
    py = args.python313 or sys.executable
    r = subprocess.run([py, '-c', script] + files, capture_output=True)
    sys.stdout.write(r.stdout.decode('utf-8', 'replace'))
    sys.stderr.write(r.stderr.decode('utf-8', 'replace'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
