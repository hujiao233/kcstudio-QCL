"""量化反编译产物的语义退化程度。

语法能不能通过是一回事，语义对不对是另一回事。这里统计几类
"语法合法但语义已丢失"的模式 —— 它们不会报错，只会静默出错。
"""
import collections
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else r'c:\Users\Sapnap\CodeBuddy\QCL\qcl'

# `if not X:` 紧跟一行同名裸表达式 —— 丢失了 `or` 回退值
LOST_OR = re.compile(r'^\s*if not (\w+(?:\.\w+)*):\s*$')
# 空字典常量出现在取值上下文里 —— 丢失了字典来源
EMPTY_DICT = re.compile(r'\{\s*\}')
# 空列表常量
EMPTY_LIST = re.compile(r'\[\s*\]')
# 裸表达式语句（一行只有一个名字），几乎总是伪影
BARE_NAME = re.compile(r'^\s{4,}([a-z_]\w*(\.\w+)*)\s*$')

total = collections.Counter()
per_file = {}

for dirpath, _dirs, files in os.walk(ROOT):
    for f in sorted(files):
        if not f.endswith('.py'):
            continue
        p = os.path.join(dirpath, f)
        rel = os.path.relpath(p, ROOT)
        lines = open(p, encoding='utf-8').read().split('\n')
        c = collections.Counter()
        for i, ln in enumerate(lines):
            if LOST_OR.match(ln):
                nxt = lines[i + 1].strip() if i + 1 < len(lines) else ''
                if nxt == LOST_OR.match(ln).group(1):
                    c['lost_or'] += 1
            stripped = ln.strip()
            if EMPTY_DICT.search(ln) and ('get(' in ln or '=' in ln):
                c['empty_dict'] += 1
            if BARE_NAME.match(ln):
                c['bare_stmt'] += 1
        if c:
            per_file[rel] = c
            total.update(c)

print('%-24s %8s %8s %8s' % ('file', 'lost_or', 'empty_dct', 'bare_stmt'))
for rel, c in sorted(per_file.items(), key=lambda x: -sum(x[1].values()))[:16]:
    print('%-24s %8d %8d %8d'
          % (rel, c['lost_or'], c['empty_dict'], c['bare_stmt']))
print()
print('TOTAL:', dict(total), ' sum=%d' % sum(total.values()))
print('files with degradation: %d' % len(per_file))
