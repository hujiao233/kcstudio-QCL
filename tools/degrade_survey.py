"""量化反编译产物的语义退化程度。

语法能不能通过是一回事，语义对不对是另一回事。这里统计几类
"语法合法但语义已丢失"的模式 —— 它们不会报错，只会静默出错。

注意口径：裸语句里的 `pass` / `continue` 是合法关键字，不一律算伪影，
单独列为 lost_body（条件/循环体被吞掉），需结合上下文判断。
"""
import collections
import keyword
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir, 'qcl')

# `if not X:` 紧跟一行同名裸表达式 —— 丢失了 `or` 回退值
LOST_OR = re.compile(r'^\s*if not (\w+(?:\.\w+)*):\s*$')
EMPTY_DICT = re.compile(r'\{\s*\}')
BARE = re.compile(r'^\s{4,}([a-z_]\w*(\.\w+)*)\s*$')
# 复合语句头（体应缩进在其下）
HEAD = re.compile(r'^\s*(if|elif|while|for|try|except|else|with)\b.*:\s*$')

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
            m = LOST_OR.match(ln)
            if m:
                nxt = lines[i + 1].strip() if i + 1 < len(lines) else ''
                if nxt == m.group(1):
                    c['lost_or'] += 1
            if EMPTY_DICT.search(ln) and ('get(' in ln or '=' in ln):
                c['empty_dict'] += 1
            bm = BARE.match(ln)
            if bm:
                name = bm.group(1)
                if keyword.iskeyword(name):
                    # 条件/循环体只剩 pass —— 原体很可能被吞掉了
                    prev = lines[i - 1].rstrip() if i else ''
                    if name == 'pass' and HEAD.match(prev):
                        c['lost_body'] += 1
                else:
                    c['bare_stmt'] += 1
        if c:
            per_file[rel] = c
            total.update(c)

print('%-24s %8s %8s %8s %8s'
      % ('file', 'lost_or', 'empty_dct', 'bare_stmt', 'lost_body'))
for rel, c in sorted(per_file.items(), key=lambda x: -sum(x[1].values()))[:14]:
    print('%-24s %8d %8d %8d %8d'
          % (rel, c['lost_or'], c['empty_dict'], c['bare_stmt'],
             c['lost_body']))
print()
print('TOTAL:', dict(total), ' sum=%d' % sum(total.values()))
print('files with degradation: %d' % len(per_file))
