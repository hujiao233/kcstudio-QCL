# Source Generated with Decompyle++
# File: multiplayer.pyc (Python 3.13)

'''联机：虚拟网（账号 + 好友 + 房间）/ 局域网 / 服务器'''
import ipaddress
import socket
from urllib.parse import urlparse
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QInputDialog, QLabel, QLineEdit, QListWidget, QListWidgetItem, QMessageBox, QPushButton, QTabWidget, QVBoxLayout
from ..pages import Page
from .. import theme
from ..widgets import hbox, vbox, make_card
from ...core import account as account_mod, instances as instances_mod, settings
from ...core.relay import GuestProxy, HostTunnel
from ...core.qtdownload import run_async

def local_ips():
    '''本机可用于联机的地址。

UDP connect 不发包，只是让系统选一条出口路由，然后读 socket 的本地地址。
但它默认没有超时：某些网络（VPN、多网卡、路由不可达）会在这里卡 3-5 秒，
而这段代码跑在界面线程里 —— 表现就是"点开联机页卡一下"。
所以统一设 1 秒超时、失败就换下一个探测目标，并且无论成败都 close。
'''
    out = {
        '127.0.0.1'}
    
    try:
        out.add(socket.gethostbyname(socket.gethostname()))
        for target in ('223.5.5.5', '8.8.8.8', '1.1.1.1'):
            s = None
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1)
            s.connect((target, 80))
            out.add(s.getsockname()[0])
            if s is not None:
                s.close()
                ('223.5.5.5', '8.8.8.8', '1.1.1.1')
            return out
            return out
        return out
    except Exception:
        continue
        return None
        except Exception:
            if s is None:
                continue
            s.close()
            continue
            except Exception:
                continue
        if s is not None:
            s.close()


class MultiplayerPage(Page):
    title = '联机'
    
    def __init__(self, ctx, parent):
        super.__init__(ctx, parent)
        self.lan_rooms = { }
        self.joined = None
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 16, 20, 14)
        lay.setSpacing(10)
        tabs = QTabWidget()
        tabs.addTab(self._virtual_tab(), '虚拟网联机')
        tabs.addTab(self._lan_tab(), '局域网 / 服务器')
        lay.addWidget(tabs, 1)
        self.timer = QTimer(self)
        self.timer.setInterval(10000)
        self.timer.timeout.connect(self._tick)
        self.timer.start()
        self._refresh_account()

    
    def bind_events(self):
        self.listen('lan_found', self._on_lan)

    
    def _virtual_tab(self):
        w = QFrame()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(4, 8, 4, 8)
        lay.setSpacing(12)
        ac = make_card()
        ac.setFixedHeight(96)
        al = hbox(14, 10)
        self.acc_state = QLabel('未登录 QCL 账号')
        self.acc_state.setStyleSheet('font-size: 15px; font-weight: 700;')
        self.acc_tip = QLabel('登录后才能使用虚拟网联机')
        self.acc_tip.setProperty('sub', True)
        self.u_name = QLineEdit()
        self.u_name.setPlaceholderText('用户名')
        self.u_name.setFixedWidth(150)
        self.u_pwd = QLineEdit()
        self.u_pwd.setPlaceholderText('密码')
        self.u_pwd.setEchoMode(QLineEdit.Password)
        self.u_pwd.setFixedWidth(150)
        self.btn_login = QPushButton('登录')
        self.btn_login.setProperty('primary', True)
        self.btn_login.clicked.connect((lambda : self._do_account('login')))
        self.btn_reg = QPushButton('注册')
        self.btn_reg.clicked.connect((lambda : self._do_account('register')))
        self.btn_out = QPushButton('退出登录')
        self.btn_out.clicked.connect(self._logout)
        self.btn_out.hide()
        self.host_tip = QLabel('主机：%s' % self.ctx.settings.host_url)
        self.host_tip.setProperty('sub', True)
        info = vbox(2)
        info.addWidget(self.acc_state)
        info.addWidget(self.acc_tip)
        al.addLayout(info, 1)
        al.addWidget(self.u_name)
        al.addWidget(self.u_pwd)
        al.addWidget(self.btn_login)
        al.addWidget(self.btn_reg)
        al.addWidget(self.btn_out)
        ac.setLayout(al)
        lay.addWidget(ac)
        body = QHBoxLayout()
        body.setSpacing(12)
        fc = make_card()
        fl = vbox(12, 8)
        t = QLabel('好友')
        t.setStyleSheet('font-weight: 700; font-size: 15px;')
        fl.addWidget(t)
        self.friends = QListWidget()
        self.friends.setSpacing(3)
        self.friends.itemDoubleClicked.connect(self._join_friend)
        fl.addWidget(self.friends, 1)
        add_row = hbox(6)
        self.f_input = QLineEdit()
        self.f_input.setPlaceholderText('输入对方用户名添加好友')
        self.f_input.returnPressed.connect(self._add_friend)
        b = QPushButton('添加')
        b.setFixedWidth(64)
        b.clicked.connect(self._add_friend)
        add_row.addWidget(self.f_input, 1)
        add_row.addWidget(b)
        fl.addLayout(add_row)
        self.pending_btn = QPushButton('处理好友请求 (0)')
        self.pending_btn.clicked.connect(self._pending)
        self.pending_btn.hide()
        fl.addWidget(self.pending_btn)
        fc.setLayout(fl)
        body.addWidget(fc, 1)
        rc = make_card()
        rl = vbox(12, 8)
        t2 = QLabel('我的联机房间')
        t2.setStyleSheet('font-weight: 700; font-size: 15px;')
        rl.addWidget(t2)
        self.room_state = QLabel('未开启')
        self.room_state.setWordWrap(True)
        self.room_help = QLabel('开启后在游戏里点击「对局域网开放」，启动器会自动接管并让好友加入。')
        self.room_help.setProperty('sub', True)
        self.room_help.setWordWrap(True)
        rl.addWidget(self.room_state)
        rl.addWidget(self.room_help)
        self.btn_room = QPushButton('开启联机房间')
        self.btn_room.setProperty('primary', True)
        self.btn_room.setFixedHeight(34)
        self.btn_room.clicked.connect(self._toggle_room)
        self.btn_room.setProperty('danger', False)
        rl.addWidget(self.btn_room)
        port_row = hbox(6)
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText('也可手动填写游戏内显示的端口')
        b2 = QPushButton('使用此端口')
        b2.setFixedWidth(100)
        b2.clicked.connect(self._manual_port)
        port_row.addWidget(self.port_input, 1)
        port_row.addWidget(b2)
        rl.addLayout(port_row)
        rl.addSpacing(6)
        jt = QLabel('加入好友的世界')
        jt.setStyleSheet('font-weight: 700;')
        rl.addWidget(jt)
        self.join_state = QLabel('未连接')
        self.join_state.setProperty('sub', True)
        self.join_state.setWordWrap(True)
        rl.addWidget(self.join_state)
        row = hbox(6)
        self.join_input = QLineEdit()
        self.join_input.setPlaceholderText('输入对方的用户名')
        self.join_input.returnPressed.connect(self._join_by_name)
        bj = QPushButton('加入')
        bj.setProperty('primary', True)
        bj.setFixedWidth(70)
        bj.clicked.connect(self._join_by_name)
        row.addWidget(self.join_input, 1)
        row.addWidget(bj)
        rl.addLayout(row)
        row2 = hbox(6)
        self.btn_copy = QPushButton('复制联机地址')
        self.btn_copy.clicked.connect(self._copy_addr)
        self.btn_leave = QPushButton('断开联机')
        self.btn_leave.clicked.connect(self._leave)
        self.btn_leave.hide()
        row2.addWidget(self.btn_copy)
        row2.addWidget(self.btn_leave)
        row2.addStretch(1)
        rl.addLayout(row2)
        rl.addStretch(1)
        rc.setLayout(rl)
        body.addWidget(rc, 1)
        lay.addLayout(body, 1)
        return w

    
    def _lan_tab(self):
        w = QFrame()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(4, 8, 4, 8)
        lay.setSpacing(12)
        top = QHBoxLayout()
        top.setSpacing(12)
        lc = make_card()
        ll = vbox(12, 8)
        t = QLabel('局域网内的世界')
        t.setStyleSheet('font-weight: 700; font-size: 15px;')
        tip = QLabel('同一网络下，有人在 Minecraft 里点了「对局域网开放」就会自动出现在这里')
        tip.setProperty('sub', True)
        tip.setWordWrap(True)
        ll.addWidget(t)
        ll.addWidget(tip)
        self.lan_list = QListWidget()
        self.lan_list.setSpacing(3)
        self.lan_list.itemDoubleClicked.connect(self._copy_lan)
        ll.addWidget(self.lan_list, 1)
        b = QPushButton('复制选中地址')
        b.clicked.connect(self._copy_lan)
        ll.addWidget(b)
        lc.setLayout(ll)
        top.addWidget(lc, 1)
        sc = make_card()
        sl = vbox(12, 8)
        t2 = QLabel('服务器列表')
        t2.setStyleSheet('font-weight: 700; font-size: 15px;')
        sl.addWidget(t2)
        self.srv_list = QListWidget()
        self.srv_list.itemDoubleClicked.connect(self._copy_srv)
        sl.addWidget(self.srv_list, 1)
        row = hbox(6)
        self.srv_input = QLineEdit()
        self.srv_input.setPlaceholderText('mc.example.com 或 1.2.3.4:25565')
        self.srv_input.returnPressed.connect(self._add_srv)
        b1 = QPushButton('添加')
        b1.setFixedWidth(64)
        b1.clicked.connect(self._add_srv)
        b2 = QPushButton('删除')
        b2.setFixedWidth(64)
        b2.setProperty('danger', True)
        b2.clicked.connect(self._del_srv)
        row.addWidget(self.srv_input, 1)
        row.addWidget(b1)
        row.addWidget(b2)
        sl.addLayout(row)
        b3 = QPushButton('复制选中地址')
        b3.clicked.connect(self._copy_srv)
        sl.addWidget(b3)
        sc.setLayout(sl)
        top.addWidget(sc, 1)
        lay.addLayout(top, 1)
        help_ = QLabel('提示：跨网络联机请用上面的「虚拟网联机」——双方都登录 QCL 账号后，输入对方用户名即可接入，数据会通过主机转发。')
        help_.setProperty('sub', True)
        help_.setWordWrap(True)
        lay.addWidget(help_)
        self._fill_servers()
        return w

    
    def _refresh_account(self):
        u = account_mod.cached_user()
        if u and u.get('token'):
            self.acc_state.setText(u.get('username', ''))
            self.acc_tip.setText('已登录，可以创建房间或加入好友的世界')
            self.u_name.hide()
            self.u_pwd.hide()
            self.btn_login.hide()
            self.btn_reg.hide()
            self.btn_out.show()
            self._load_friends()
        return None
        self.acc_state.setText('未登录 QCL 账号')
        self.acc_tip.setText('本机地址 %s ｜ 登录后可使用虚拟网' % self.ctx.settings.host_url)
        self.u_name.show()
        self.u_pwd.show()
        self.btn_login.show()
        self.btn_reg.show()
        self.btn_out.hide()
        self.friends.clear()

    
    def _is_local_host(self):
        if not self.ctx.settings.host_url:
            self.ctx.settings.host_url
        u = ''.lower()
        if not '127.0.0.1' in u:
            '127.0.0.1' in u
            if not 'localhost' in u:
                'localhost' in u
        return '::1' in u

    
    def _account_error_text(self, e):
        '''把 API 错误翻译成可操作的提示'''
        msg = str(e)
        if '无法连接' in msg and '不在线' in msg or '超时' in msg:
            if not self._is_local_host() and self.ctx.settings.get('is_host', False):
                pass
            return '连不上本机主机服务。若这是你自己的电脑，请到「设置」页勾选「这台电脑就是主机」后重试'
        return '连不上主机 %s，请确认主机在线、地址填写正确' % self.ctx.settings.host_url
        if '用户名或密码错误' in msg:
            pass
        return '账号或密码不对；若还没注册过，请先点「注册」'
        if '已存在' in msg or '已被注册' in msg:
            pass
        return '该用户名已被占用，换一个试试'
        return msg

    
    def _do_account(self, kind):
        name = self.u_name.text().strip()
        pwd = self.u_pwd.text()
        if len(name) < 3 or len(pwd) < 6:
            self.ctx.toast('用户名至少 3 位，密码至少 6 位', 'warn')
        return None
        api = self.ctx.api
        
        def work():
            if kind == 'register':
                pass
            return api.register(name, pwd)
            return api.login(name, pwd)

        
        def done(d):
            if not d.get('username'):
                d.get('username')
            account_mod.save_user({
                'username': name,
                'token': d.get('token'),
                'nickname': d.get('nickname', name) })
            if not d.get('username'):
                d.get('username')
            self.ctx.toast('已登录：%s' % name, 'ok')
            self._refresh_account()

        self.ctx.toast('正在连接主机…', 'info')
        run_async(work, done, (lambda e: self.ctx.toast(self._account_error_text(e), 'err')))

    
    def _logout(self):
        self._leave()
        self._close_room(True)
        account_mod.clear_user()
        self._refresh_account()

    
    def _load_friends(self):
        api = self.ctx.api
        tok = account_mod.token()
        if not tok:
            pass
        return None
        run_async((lambda : api.friend_list(tok)), self._on_friends)

    
    def _on_friends(self, d):
        self.friends.clear()
        for f in d.get('friends', []):
            state = '在线' if f.get('online') else '离线'
            if f.get('in_room'):
                if not f.get('room_mc'):
                    f.get('room_mc')
            state = '房间开放中（%s）' % ''
            it = QListWidgetItem(f'''  ·  ''')
            it.setData(Qt.UserRole, f)
            row = self._friend_row(f)
            it.setSizeHint(row.sizeHint())
            self.friends.addItem(it)
            self.friends.setItemWidget(it, row)
        pend = d.get('pending', [])
        if pend:
            self.pending_btn.setText('处理好友请求 (%d)' % len(pend))
            self.pending_btn.show()
        return None
        self.pending_btn.hide()

    
    def _friend_row(self, f):
        w = QFrame()
        w.setObjectName('card2')
        lay = QHBoxLayout(w)
        lay.setContentsMargins(10, 6, 10, 6)
        lay.setSpacing(8)
        lab = QLabel('%s' % f.get('username'))
        if f.get('in_room'):
            pass
        elif f.get('online'):
            pass
        
        st = '在线'('离线')
        st.setProperty('sub', True)
        if f.get('in_room'):
            pass
        st.setStyleSheet('color:%s;' % theme.ACCENT)
        lay.addWidget(lab, 1)
        lay.addWidget(st)
        if f.get('in_room'):
            b = QPushButton('加入')
            b.setFixedWidth(64)
            b.setProperty('primary', True)
            b.clicked.connect((lambda : self._join(f.get('username'))))
        lay.addWidget(b)
        return w

    
    def _add_friend(self):
        name = self.f_input.text().strip()
        if not name:
            pass
        return None
        api = self.ctx.api
        tok = account_mod.token()
        if not tok:
            pass
        return None
        run_async((lambda : api.friend_add(tok, name)), (lambda d: if not d.get('msg'):
d.get('msg')(self.ctx.toast('已发送', 'ok'), self.f_input.clear(), self._load_friends())), (lambda e: self.ctx.toast('%s' % e, 'err')))

    
    def _pending(self):
        api = self.ctx.api
        tok = account_mod.token()
        if not tok:
            pass
        return None
        
        def done(d):
            pend = d.get('pending', [])
            if not pend:
                pass
            return None
            (name, ok) = QInputDialog.getItem(self, '好友请求', '选择要接受的请求：', pend, 0, False)
            if ok:
                if name:
                    run_async((lambda : api.friend_accept(tok, name)), (lambda r: (self.ctx.toast('已添加 %s' % name, 'ok'), self._load_friends())), (lambda e: self.ctx.toast('%s' % e, 'err')))
                return None
            return None

        run_async((lambda : api.friend_list(tok)), done)

    
    def _join_friend(self, item):
        f = item.data(Qt.UserRole)
        if f:
            self._join(f.get('username'))
        return None

    
    def _toggle_room(self):
        if self.ctx.room_host is not None:
            self._close_room()
        return None
        self._open_room()

    
    def _open_room(self):
        tok = account_mod.token()
        if not tok:
            self.ctx.toast('请先登录 QCL 账号', 'warn')
        return None
        inst = instances_mod.get_or_default(self.ctx.game_root)
        mc = inst.mc if inst else ''
        api = self.ctx.api
        
        def done(d):
            if not d.get('room_id'):
                d.get('room_id')
            self.room_id = account_mod.username()
            self.room_state.setText('房间已创建，等待游戏内「对局域网开放」…')
            self.room_help.setText('请启动游戏并进入存档 → 暂停菜单 → 对局域网开放。启动器会自动识别端口。 若未自动识别，可在下面手动填写游戏里显示的端口。')
            self.btn_room.setProperty('danger', True)
            self.btn_room.style().unpolish(self.btn_room)
            self.btn_room.style().polish(self.btn_room)
            self.btn_room.setText('关闭联机房间')
            self.ctx.toast('房间已创建', 'ok')
            self.waiting_port = True

        run_async((lambda : api.room_create(tok, mc, '%s 的世界' % account_mod.username())), done, (lambda e: self.ctx.toast('%s' % e, 'err')))

    
    def _close_room(self, silent):
        api = self.ctx.api
        tok = account_mod.token()
        if self.ctx.room_host:
            self.ctx.room_host.close()
            self.ctx.room_host = None
        if tok:
            pass
        run_async((lambda : api.room_close(tok)))
        self.waiting_port = False
        self.btn_room.setProperty('danger', False)
        self.btn_room.style().unpolish(self.btn_room)
        self.btn_room.style().polish(self.btn_room)
        self.btn_room.setText('开启联机房间')
        self.room_state.setText('未开启')
        if not silent:
            self.ctx.toast('房间已关闭', 'ok')
        return None

    
    def _manual_port(self):
        
        try:
            p = int(self.port_input.text().strip())
            self._set_port(p)
            return None
        except Exception:
            self.ctx.toast('请输入正确的端口', 'warn')
            return None


    def _on_lan(self, info):
        
        try:
            if ipaddress.ip_address(info['ip']).is_private and info['ip'] in local_ips() and getattr(self, 'waiting_port', False):
                pass
            self._set_port(info['port'])
            self.lan_rooms[f''':'''] = info
            self._fill_lan()
            return None
        except Exception:
            continue


    def _set_port(self, port):
        tok = account_mod.token()
        api = self.ctx.api
        self.waiting_port = False
        self.room_port = port
        self.room_state.setText('房间已开启（端口 %d），好友可以加入了' % port)
        self.room_help.setText('保持游戏开启即可。好友在「联机」里输入你的用户名就能接入，流量经主机转发。')
        run_async((lambda : api.room_update(tok, port)))
        relay_host = self._relay_host()
        if not self.ctx.settings.get('relay_port', 0):
            self.ctx.settings.get('relay_port', 0)
        relay_port = int(0)
        if not relay_port:
            pass
        relay_port = 25801
        tun = HostTunnel(relay_host, relay_port, account_mod.username(), tok, port, (lambda m: self.ctx.append_log('[虚拟网] ' + m)))
        self.ctx.room_host = tun
        tun.start()
        self.ctx.append_log('[虚拟网] 已开启房间，端口 %d' % port)

    
    def _relay_host(self):
        url = self.ctx.settings.host_url
        
        try:
            host = urlparse(url).hostname
            if not host:
                host
            return '127.0.0.1'
        except Exception:
            host = ''
            continue


    def _join_by_name(self):
        name = self.join_input.text().strip()
        if name:
            self._join(name)
        return None

    
    def _join(self, owner):
        tok = account_mod.token()
        if not tok:
            self.ctx.toast('请先登录 QCL 账号', 'warn')
        return None
        api = self.ctx.api
        self.join_state.setText('正在连接 %s 的世界…' % owner)
        
        def resolve():
            return api.room_resolve(tok, owner)

        
        def done(d):
            self._start_guest(d, owner)

        run_async(resolve, done, (lambda e: (self.join_state.setText('未连接'), self.ctx.toast('%s' % e, 'err'))))

    
    def _start_guest(self, d, owner):
        relay_host = self._relay_host()
        if not d.get('relay_port'):
            d.get('relay_port')
            if not self.ctx.settings.get('relay_port'):
                self.ctx.settings.get('relay_port')
        relay_port = int(25801)
        if not self.ctx.settings.get('local_proxy_port', 25565):
            self.ctx.settings.get('local_proxy_port', 25565)
        local_port = int(25565)
        if self.joined:
            pass
        self._leave()
        
        try:
            proxy = GuestProxy(local_port, (relay_host, relay_port), d['room_id'], account_mod.token(), ('', int(0)) if d.get('ip') and d.get('port') else None, (lambda m: self.ctx.append_log('[虚拟网] ' + m)))
            proxy.start()
            self.joined = proxy
            self.join_addr = '127.0.0.1:%d' % local_port
            self.join_state.setText(f'''已接入  的世界：''')
            self.btn_leave.show()
            self.ctx.append_log(f'''[虚拟网] 已接入  的世界，游戏内连接 ''')
            self._copy_addr()
            return None
        except Exception:
            e = None
            self.join_state.setText('未连接')
            self.ctx.toast('%s' % e, 'err')
            e = None
            del e
            return None
            e = None
            del e


    def _copy_addr(self):
        addr = getattr(self, 'join_addr', '')
        if not addr:
            self.ctx.toast('还没有加入任何房间', 'warn')
        return None
        QApplication.clipboard().setText(addr)
        self.ctx.toast('已复制 %s，在游戏里「直接连接」粘贴即可' % addr, 'ok')

    
    def _leave(self):
        if self.joined:
            self.joined.close()
            self.joined = None
        self.join_state.setText('未连接')
        self.btn_leave.hide()

    
    def _fill_lan(self):
        if not hasattr(self, 'lan_list'):
            pass
        return None
        self.lan_list.clear()
        now = __import__('time').time()
        for k, v in list(self.lan_rooms.items()):
            if now - v.get('time', 0) > 40:
                self.lan_rooms.pop(k, None)
                continue
            it = QListWidgetItem(f''':  ''')
            it.setData(Qt.UserRole, f''':''')
            self.lan_list.addItem(it)

    
    def _copy_lan(self, item):
        if not item:
            item
        it = self.lan_list.currentItem()
        if not it:
            self.ctx.toast('请先选中一个世界', 'warn')
        return None
        addr = it.data(Qt.UserRole)
        QApplication.clipboard().setText(addr)
        self.ctx.toast('已复制 %s' % addr, 'ok')

    
    def _fill_servers(self):
        if not hasattr(self, 'srv_list'):
            pass
        return None
        self.srv_list.clear()
        if not self.ctx.settings.get('servers'):
            self.ctx.settings.get('servers')
        for s in []:
            it = QListWidgetItem(f'''  ·  ''')
            it.setData(Qt.UserRole, s.get('addr'))
            self.srv_list.addItem(it)

    
    def _add_srv(self):
        addr = self.srv_input.text().strip()
        if not addr:
            pass
        return None
        name = addr.split(':')[0]
        if not self.ctx.settings.get('servers'):
            self.ctx.settings.get('servers')
        lst = list([])
        lst.append({
            'name': name,
            'addr': addr })
        self.ctx.settings.set('servers', lst)
        self.srv_input.clear()
        self._fill_servers()

    
    def _del_srv(self):
        it = self.srv_list.currentItem()
        if not it:
            pass
        return None
        addr = it.data(Qt.UserRole)
        if not self.ctx.settings.get('servers'):
            self.ctx.settings.get('servers')
        , []
        [], s, lst, s = None
        self.ctx.settings.set('servers', lst)
        self._fill_servers()
        return None
        

    def _copy_srv(self, item):
        if not item:
            item
        it = self.srv_list.currentItem()
        if not it:
            self.ctx.toast('请先选中一个服务器', 'warn')
        return None
        QApplication.clipboard().setText(it.data(Qt.UserRole))
        self.ctx.toast('已复制地址', 'ok')

    
    def _tick(self):
        if account_mod.token():
            self._load_friends()
            if self.ctx.room_host is not None:
                api = self.ctx.api
                run_async((lambda : api.heartbeat(account_mod.token())))
            return None
        return None

    
    def on_show(self):
        self.host_tip.setText('主机：%s' % self.ctx.settings.host_url)
        self._refresh_account()
        self._fill_servers()



