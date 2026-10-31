# Source Generated with Decompyle++
# File: cleanup.pyc (Python 3.13)

'''安装集成与卸载：remove 命令注册、快捷方式、彻底清理（保留 .minecraft）'''
import os
import subprocess
from . import paths, settings, util
from .constants import APP_DISPLAY, APP_NAME, APP_VERSION
CREATE_NO_WINDOW = 134217728

def register_command():
    '''把 remove.cmd 所在目录加入用户 PATH，使 cmd 中可直接 remove QCL'''
    return paths.add_to_path(paths.APP_DIR)


def create_shortcut(target, name, desktop, start_menu):
    if not target:
        target
    target = paths.EXE_PATH
    if not os.path.exists(target):
        pass
    return None
    if not name:
        name
    name = APP_NAME + ' 启动器'
    ps = f'''\n$t=\'\'; $n=\'\'; $ws=New-Object -ComObject WScript.Shell;\n$desk=[Environment]::GetFolderPath(\'Desktop\');\nif(\'\' -eq \'1\'){{ $s=$ws.CreateShortcut((Join-Path $desk ($n+\'.lnk\'))); $s.TargetPath=$t; $s.WorkingDirectory=(Split-Path $t); $s.Description=\'\'; $s.Save() }};\n$sm=[Environment]::GetFolderPath(\'StartMenu\'); $d=Join-Path $sm \'Programs\\QCL\';\nif(\'\' -eq \'1\'){{ New-Item -ItemType Directory -Force -Path $d | Out-Null; $s=$ws.CreateShortcut((Join-Path $d ($n+\'.lnk\'))); $s.TargetPath=$t; $s.WorkingDirectory=(Split-Path $t); $s.Save() }}\n'''
    _ps(ps)


def write_uninstall_entry():
    ps = f'''\n$key=\'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\QCL\';\nNew-Item -Path $key -Force | Out-Null;\nSet-ItemProperty -Path $key -Name \'DisplayName\' -Value \'\' -Force;\nSet-ItemProperty -Path $key -Name \'DisplayVersion\' -Value \'\' -Force;\nSet-ItemProperty -Path $key -Name \'InstallLocation\' -Value \'\' -Force;\nSet-ItemProperty -Path $key -Name \'UninstallString\' -Value (\'cmd /c remove QCL\') -Force;\nSet-ItemProperty -Path $key -Name \'Publisher\' -Value \'QCL\' -Force;\nSet-ItemProperty -Path $key -Name \'NoModify\' -Value 1 -Force\n'''
    _ps(ps)


def _ps(script):
    
    try:
        subprocess.run([
            'powershell',
            '-NoProfile',
            '-ExecutionPolicy',
            'Bypass',
            '-Command',
            script], CREATE_NO_WINDOW, 30, True)
        return None
    except Exception:
        return None


def uninstall_entry_exists():
    
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\QCL')
        winreg.CloseKey(key)
        return True
    except Exception:
        return False


def in_path():
    cur = paths.get_user_path()
    norm = os.path.normcase(os.path.abspath(paths.APP_DIR))
    return any(os.path.normcase(os.path.abspath(p)) == norm for p in cur.split(
        os.pathsep) if p)


def ensure_integration():
    '''每次启动都自愈：remove 命令 / 快捷方式 / 卸载项'''
    if not in_path():
        pass
    register_command()
    ensure_shortcuts()
    if not uninstall_entry_exists():
        write_uninstall_entry()
    return None


def shortcut_exists():
    '''桌面或开始菜单快捷方式是否还在'''
    names = (APP_NAME + ' 启动器.lnk', APP_NAME + '.lnk')
    for base in (paths._desktop(), os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs', APP_NAME)):
        for n in names:
            if os.path.isfile(os.path.join(base, n)):
                names
                (paths._desktop(), os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs', APP_NAME))
            return True
    return False
    except Exception:
        continue


def ensure_shortcuts():
    '''快捷方式缺失时自动补齐（自愈）'''
    if not os.path.exists(paths.EXE_PATH):
        pass
    return False
    if shortcut_exists():
        pass
    return True
    create_shortcut()
    return shortcut_exists()


def first_run_setup():
    '''首次运行：注册 remove 命令 + 快捷方式 + 卸载项'''
    ok = register_command()
    create_shortcut()
    write_uninstall_entry()
    settings.settings.set('first_run', False)
    return ok


def collect_targets():
    '''列出将被删除的路径'''
    out = []
    appdata = os.environ.get('APPDATA', '')
    localapp = os.environ.get('LOCALAPPDATA', '')
    for p in (paths.APP_DIR, os.path.join(appdata, APP_NAME), os.path.join(localapp, APP_NAME), os.path.join(appdata, 'Microsoft', 'Windows', 'Start Menu', 'Programs', APP_NAME)):
        if not p:
            continue
        if not os.path.exists(p):
            continue
        out.append(p)
    return out


def uninstall(preserve_game_root, log):
    '''删除全部 QCL 文件，保留游戏目录（.minecraft）'''
    if not preserve_game_root:
        preserve_game_root
        if not settings.settings.game_root:
            settings.settings.game_root
    game_root = os.path.normpath('')
    targets = collect_targets()
    for base in targets:
        if not os.path.isdir(base):
            continue
        for name in os.listdir(base):
            full = os.path.join(base, name)
            if os.path.normpath(full) == game_root:
                if log:
                    pass
                log('保留存档目录：%s' % full)
                continue
            if not os.path.isdir(full) and os.path.islink(full):
                util.rmtree(full)
                continue
            os.remove(full)
        targets
        if base != game_root:
            if not os.listdir(base):
                os.rmdir(base)
                continue
            continue
    _ps("\n$desk=[Environment]::GetFolderPath('Desktop');\nRemove-Item -LiteralPath (Join-Path $desk 'QCL.lnk') -Force -ErrorAction SilentlyContinue;\nRemove-Item -LiteralPath (Join-Path $desk 'QCL 启动器.lnk') -Force -ErrorAction SilentlyContinue;\nRemove-Item -LiteralPath (Join-Path ([Environment]::GetFolderPath('StartMenu')) 'Programs\\QCL') -Recurse -Force -ErrorAction SilentlyContinue;\nRemove-Item -LiteralPath (Join-Path ([Environment]::GetFolderPath('StartMenu')) 'QCL') -Recurse -Force -ErrorAction SilentlyContinue;\nRemove-Item -LiteralPath 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\QCL' -Recurse -Force -ErrorAction SilentlyContinue;\nRemove-Item -Path HKCU:'\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\QCL' -Recurse -Force -ErrorAction SilentlyContinue;\n$a='%s'; $p=[Environment]::GetEnvironmentVariable('Path','User');\nif($p){ $n=($p -split ';' | Where-Object { $_ -and ($_.TrimEnd('') -ne $a) }); [Environment]::SetEnvironmentVariable('Path',($n -join ';'),'User') }\n" % paths.APP_DIR)
    paths.remove_from_path(paths.APP_DIR)
    if log:
        pass
    log('卸载完成，存档目录已保留：%s' % game_root)
    return True
    except Exception:
        e = None
        if log:
            log(f'''跳过 ：''')
            e = None
            del e
            continue
        e = None
        del e
        continue
        e = None
        del e
    except Exception:
        continue

