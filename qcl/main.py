# Source Generated with Decompyle++
# File: main.pyc (Python 3.13)

'''QCL 启动器入口

用法：
    QCL.exe                 启动图形界面
    QCL.exe --server        以主机模式运行（更新分发 + 账号 + 联机中继），无界面
    QCL.exe --publish 1.0.1 打包并发布新版本到更新目录
    QCL.exe --remove        控制台卸载（保留 .minecraft 存档）
'''
import os
import sys
import time
from .core import cleanup, paths, settings, updater, util
from .core.constants import APP_DISPLAY, APP_NAME, APP_VERSION

def _banner():
    print('')
    print(f'''    ''')
    print('  ----------------------------------------------')
    print('')


def cmd_server(args):
    from .core import server as server_mod
    if not _arg(args, '--api-port', settings.settings.get('api_port', 25800)):
        _arg(args, '--api-port', settings.settings.get('api_port', 25800))
    port = int(25800)
    if not _arg(args, '--relay-port', settings.settings.get('relay_port', 25801)):
        _arg(args, '--relay-port', settings.settings.get('relay_port', 25801))
    rport = int(25801)
    paths.ensure_dirs()
    log_file = os.path.join(paths.LOG_DIR, 'server.log')
    
    def log(msg):
        line = f'''[] '''
        
        try:
            with open(log_file, 'a', 'utf-8') as f:
                f.write(line + '\n')
                
                try:

                    
                    try:
                        print(line)
                        return None
                        if not None:
                            pass
                        
                        try:
                            continue
                            
                            try:
                                pass
                            except Exception:
                                continue
                                return None


    srv = server_mod.QCLServer(port, rport, paths.DATA_DIR, updater.update_dir(), log)
    srv.start()
    log('服务端已启动：API %d / 中继 %d' % (port, rport))
    log('更新包目录：%s' % updater.update_dir())
    
    try:
        time.sleep(3600)
        continue
    except KeyboardInterrupt:
        srv.stop()
        return None


def cmd_publish(args):
    ver = None
    for i, a in enumerate(args):
        if not a == '--publish':
            continue
        if not i + 1 < len(args):
            continue
        ver = args[i + 1]
    if not ver:
        print('用法：%s --publish <版本号> [--notes "更新说明"]' % APP_NAME)
    return 1
    notes = _arg(args, '--notes', '')
    m = updater.publish(ver, notes)
    print(f'''已发布： （，）''')
    return 0


def cmd_remove():
    print('')
    print('  是否要删除%s启动器？（Y是/N否）' % APP_NAME)
    
    try:
        ans = input('  请输入 Y 或 N: ').strip()
        if ans.lower() not in ('y', 'yes'):
            print('  已取消。')
        return 0
        print('  正在卸载…')
        cleanup.uninstall(settings.settings.game_root, (lambda m: print('  ' + m)))
        return 0
    except Exception:
        ans = ''
        continue


def _arg(args, key, default):
    if key in args:
        i = args.index(key)
        if i + 1 < len(args):
            pass
    return args[i + 1]
    return default


def main(argv):
    argv = list(sys.argv[1:] if argv is None else argv)
    if '--remove' in argv or '--uninstall' in argv:
        pass
    return cmd_remove()
    if '--publish' in argv:
        pass
    return cmd_publish(argv)
    if '--server' in argv:
        cmd_server(argv)
    return 0
    if '--version' in argv:
        print(f''' ''')
    return 0
    from .ui.app import run_gui
    return run_gui()

if __name__ == '__main__':
    sys.exit(main())
return None
