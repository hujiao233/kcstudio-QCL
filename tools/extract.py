"""从 QCL-Setup-2.0.0.exe 中取出软件本体（QCL.exe）及其字节码。

用法:
    python extract.py --exe QCL-Setup-2.0.0.exe --out work/
    python extract.py --app work/payload/QCL.exe --pyc-out work/pyc/
"""

import argparse
import os
import struct
import sys
import zipfile

MAGIC = b'MEI\x0c\x0b\x0a\x0b\x0e'
ENTRY = '!iIIIBc'          # entryLen, entryPos, cmprsdDataSize, uncmprsdDataSize, cmprsFlag, type
ENTRY_SIZE = 18


def read_carchive(path):
    """返回 (pkg_start, entries)，entries 为 (name, pos, csize, usize, cflag, type)。"""
    data = open(path, 'rb').read()
    cookie_pos = data.find(MAGIC)
    if cookie_pos < 0:
        raise SystemExit('not a PyInstaller archive: %s' % path)
    (magic, lengthof_package, toc, toc_len, pyvers,
     pylibname) = struct.unpack('!8sIIii64s', data[cookie_pos:cookie_pos + 88])
    pkg_start = cookie_pos + 88 - lengthof_package
    print('%s: python=%d.%d, pkg_start=0x%X' % (path, pyvers >> 8, pyvers & 0xFF, pkg_start))

    toc_blob = data[pkg_start + toc: pkg_start + toc + toc_len]
    try:
        toc_blob = zlib_decompress(toc_blob)
    except Exception:
        pass

    entries = []
    p = 0
    while p < len(toc_blob):
        entry_len, pos, csize, usize, cflag, typ = struct.unpack(ENTRY, toc_blob[p:p + ENTRY_SIZE])
        name = toc_blob[p + ENTRY_SIZE:p + entry_len].rstrip(b'\x00').decode('utf-8', 'replace')
        entries.append((name, pos, csize, usize, cflag, chr(typ[0])))
        p += entry_len
    return data, pkg_start, entries


def zlib_decompress(blob):
    import zlib
    return zlib.decompress(blob)


def dump_carchive(path, outdir):
    import zlib
    data, pkg_start, entries = read_carchive(path)
    os.makedirs(outdir, exist_ok=True)
    for name, pos, csize, usize, cflag, typ in entries:
        raw = data[pkg_start + pos: pkg_start + pos + csize]
        if cflag:
            raw = zlib.decompress(raw)
        safe = name.replace('\\', '/').replace('..', '__')
        fp = os.path.join(outdir, safe)
        os.makedirs(os.path.dirname(fp) or outdir, exist_ok=True)
        open(fp, 'wb').write(raw)
    print('wrote %d entries -> %s' % (len(entries), outdir))
    return entries


def unpack_payload(extracted_dir, out_root):
    """把外壳解包目录中的 payload.zip 展开到 out_root/payload。"""
    src = None
    for root, _dirs, files in os.walk(extracted_dir):
        for f in files:
            if f == 'payload.zip':
                src = os.path.join(root, f)
    if not src:
        raise SystemExit('payload.zip not found under %s' % extracted_dir)
    dst = os.path.join(out_root, 'payload')
    with zipfile.ZipFile(src) as z:
        z.extractall(dst)
    print('payload -> %s' % dst)
    return dst


def extract_pyz(app_exe, pyc_out, only_prefix='qcl'):
    """解包 QCL.exe，把 PYZ 中指定前缀的模块写成 .pyc。"""
    import zlib
    _, _, entries = read_carchive(app_exe)
    tmp = os.path.join(os.path.dirname(pyc_out) or '.', '_pyz_tmp')
    dump_carchive(app_exe, tmp)
    pyz = open(os.path.join(tmp, 'PYZ.pyz'), 'rb').read()
    pymagic, toc_pos, toc_len = struct.unpack('!4sii', pyz[:12])
    toc_blob = pyz[toc_pos:toc_pos + toc_len]
    try:
        toc_blob = zlib.decompress(toc_blob)
    except Exception:
        pass

    os.makedirs(pyc_out, exist_ok=True)
    n = 0
    p = 0
    while p < len(toc_blob):
        entry_len, pos, csize, usize, cflag, typ = struct.unpack(ENTRY, toc_blob[p:p + ENTRY_SIZE])
        name = toc_blob[p + ENTRY_SIZE:p + entry_len].rstrip(b'\x00').decode('utf-8', 'replace')
        p += entry_len
        if only_prefix and not name.startswith(only_prefix):
            continue
        raw = pyz[pos:pos + csize]
        if cflag:
            raw = zlib.decompress(raw)
        fp = os.path.join(pyc_out, name.replace('..', '__') + '.pyc')
        os.makedirs(os.path.dirname(fp) or pyc_out, exist_ok=True)
        open(fp, 'wb').write(pymagic + b'\x00' * 12 + raw)
        n += 1
    print('wrote %d pyc -> %s' % (n, pyc_out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--exe', help='外层安装包 QCL-Setup-*.exe')
    ap.add_argument('--out', default='work', help='工作目录')
    ap.add_argument('--app', help='软件本体 QCL.exe')
    ap.add_argument('--pyc-out', default='work/pyc')
    args = ap.parse_args()

    if args.exe:
        dump_carchive(args.exe, os.path.join(args.out, 'setup_extracted'))
        unpack_payload(os.path.join(args.out, 'setup_extracted'), args.out)
    if args.app:
        extract_pyz(args.app, args.pyc_out)
    if not args.exe and not args.app:
        ap.print_help()
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
