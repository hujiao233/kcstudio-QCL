"""从 PyInstaller 打包产物中取出 qcl 模块的字节码。

原始安装包已丢失，bytecode/ 里的两份字节码是孤本；本脚本用于在拿到新的
发行包时重建它们。

用法:
    python extract_pyz.py <QCL.exe 或含它的 zip> <输出目录> [--all]

默认只导出 qcl.* 模块（本项目的代码）；--all 会导出全部模块。

两个来源的差异（实测）:
    dev  onedir 部署目录里的 QCL.exe  —— 与仓库源码同源（较旧版本）
    zip  QCL.zip 里的 QCL.exe         —— 较新版本，5 个模块代码不同
判定源码归属可用字符串常量命中率比对，见 tools/ 下的比对脚本。
"""

import argparse
import marshal
import os
import struct
import sys
import zipfile
import zlib

MEI = b'MEI\014\013\012\013\016'


def read_bytes(src):
    """接受 exe 路径，或只含一个 exe 的 zip 路径。"""
    if zipfile.is_zipfile(src):
        with zipfile.ZipFile(src) as z:
            for n in z.namelist():
                if n.lower().endswith('.exe'):
                    return z.read(n)
        raise SystemExit('zip 里没有 exe')
    with open(src, 'rb') as f:
        return f.read()


def parse_carchive(data):
    pos = data.rfind(MEI)
    if pos < 0:
        raise SystemExit('不是 PyInstaller 产物')
    magic, lengthofPackage, toc, tocLen, pyvers = struct.unpack(
        '!8siIIi', data[pos:pos + 24])
    pkgstart = len(data) - lengthofPackage
    entries = {}
    p = pkgstart + toc
    end = p + tocLen
    while p < end:
        (elen,) = struct.unpack('!i', data[p:p + 4])
        if elen <= 18 or p + elen > end:
            break
        epos, dlen, ulen, cflag, typcd = struct.unpack(
            '!iiiBB', data[p + 4:p + 18])
        name = data[p + 18:p + elen].rstrip(b'\0').decode('utf-8', 'replace')
        entries[name] = (pkgstart + epos, dlen, ulen, cflag, typcd)
        p += elen
    return pyvers, entries


def load_pyz(data, entries):
    # 条目名带后缀，例如 'PYZ.pyz'
    key = next((k for k in entries if k.split('.')[0] == 'PYZ'), None)
    if key is None:
        raise SystemExit('找不到 PYZ（条目: %s）' % sorted(entries))
    off, dlen, ulen, cflag, _ = entries[key]
    raw = data[off:off + dlen]
    assert raw[:4] == b'PYZ\0', raw[:4]
    pymagic = raw[4:8]
    (toc_pos,) = struct.unpack('!i', raw[8:12])
    toc = marshal.loads(raw[toc_pos:])
    # 3.13 起 TOC 是 {name: (typ, pos, length)}，旧版是 [(name, ...), ...]
    if isinstance(toc, dict):
        items = toc.items()
    else:
        items = [(t[0], (t[1][0], t[1][1], t[1][2])) for t in toc]
    out = {}
    for name, meta in items:
        pos, length = meta[1], meta[2]
        # 别名条目（同一代码对象登记多个模块名）长度为 0，没有自己的数据
        if length == 0:
            continue
        out[name] = zlib.decompress(raw[pos:pos + length])
    return pymagic, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('outdir')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--prefix', default='qcl')
    args = ap.parse_args()

    data = read_bytes(args.src)
    pyvers, entries = parse_carchive(data)
    pymagic, modules = load_pyz(data, entries)
    print('pyvers=%d  pymagic=%d  modules=%d'
          % (pyvers, int.from_bytes(pymagic, 'little'), len(modules)))

    n = 0
    for name, body in sorted(modules.items()):
        if not args.all and not name.startswith(args.prefix):
            continue
        dst = os.path.join(args.outdir, *name.split('.')) + '.pyc'
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, 'wb') as f:
            f.write(pymagic + b'\0' * 12 + body)
        n += 1
    print('wrote %d modules to %s' % (n, args.outdir))


if __name__ == '__main__':
    sys.exit(main())
