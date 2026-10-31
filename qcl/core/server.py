# Source Generated with Decompyle++
# File: server.pyc (Python 3.13)

'''QCL 主机服务：更新分发 + 账号 + 虚拟网房间 + 中继（纯标准库，可后台常驻）'''
import hashlib
import json
import os
import secrets
import socket
import struct
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .constants import APP_NAME, APP_VERSION, DEFAULT_API_PORT, DEFAULT_RELAY_PORT
from .relay import BUFSIZE, CLOSE, DATA, FrameReader, OPEN, pack

class Store:
    
    def __init__(self, path):
        self.path = path
        self.lock = threading.RLock()
        self.data = {
            'users': { },
            'tokens': { },
            'rooms': { },
            'logs': [],
            'forum': [],
            'chat': [] }
        self.load()

    
    def load(self):
        if os.path.exists(self.path):
            
            try:
                with open(self.path, 'r', 'utf-8') as f:
                    self.data.update(json.load(f))
                    
                    try:

                        return None
                        return None
                        if not None:
                            pass
                        
                        try:
                            return None
                            
                            try:
                                pass
                            except Exception:
                                return None


    def save(self):
        os.makedirs(os.path.dirname(self.path), True)
        with self.lock:
            tmp = self.path + '.tmp'
            with open(tmp, 'w', 'utf-8') as f:
                json.dump(self.data, f, False, 2)

            os.replace(tmp, self.path)

            return None
            if not None:
                pass
        continue
        if not None:
            pass


class RelayServer(threading.Thread):
    
    def __init__(self, port, store, log):
        super.__init__(True)
        self.port = port
        self.store = store
        self.log = log
        self.sock = None
        self.stop_event = threading.Event()
        self.pending = { }
        self.plock = threading.Lock()

    
    def _say(self, msg):
        if self.log:
            self.log('[中继] ' + msg)
        return None

    
    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.sock.bind(('0.0.0.0', self.port))
            self.sock.listen(64)
            self._say('中继服务已启动，端口 %d' % self.port)
            if not self.stop_event.is_set():
                
                try:
                    (conn, addr) = self.sock.accept()
                    threading.Thread(self._handle_conn, (conn, addr), True).start()
                    if not self.stop_event.is_set():
                        continue
                    return None
                    return None
                    except OSError:
                        e = None
                        self._say('端口 %d 绑定失败：%s' % (self.port, e))
                        e = None
                        del e
                        return None
                        e = None
                        del e
                except Exception:
                    return None


    def _handle_conn(self, conn, addr):
        line = b''
        
        try:
            conn.settimeout(15)
            if line.endswith(b'\n') and len(line) < 4096:
                d = conn.recv(1)
                if not d:
                    pass
                raise ConnectionError
            line += d
            if line.endswith(b'\n') and len(line) < 4096:
                continue
            conn.settimeout(None)
            parts = line.decode('utf-8', 'ignore').strip().split()
            if len(parts) >= 3 and parts[0].upper() == 'HOST':
                self._as_host(conn, addr, parts[1], parts[2], int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 0)
            return None
            if len(parts) >= 3 and parts[0].upper() == 'JOIN':
                self._as_guest(conn, addr, parts[1], parts[2])
            return None
            
            try:
                conn.close()
                return None
                except Exception:
                    conn.close()
                except Exception:
                    pass
                return None
            except Exception:
                return None


    def _as_host(self, conn, addr, room_id, token, port):
        with self.store.lock:
            name = self.store.data['tokens'].get(token)

        if not name:
            
            try:
                conn.sendall(b'ERR\n')
                conn.close()
                return None
                with self.store.lock:
                    room = self.store.data['rooms'].setdefault(room_id, { })
                    room.update({
                        'owner': name,
                        'ip': addr[0],
                        'host_conn': None,
                        'guests': { },
                        'next_sid': 1,
                        'port': port,
                        'online': True,
                        'mc': room.get('mc', ''),
                        'name': room.get('name', name),
                        'created': room.get('created', int(time.time())) })
                    room['host_conn'] = conn

                self._say(f'''房主  上线（房间 ，来自 ）''')
                with self.plock:
                    waiters = self.pending.pop(room_id, [])

                for gsock, gtoken in waiters:
                    self._link(room_id, gsock, gtoken)
                reader = FrameReader(conn)
                
                try:
                    if not self.stop_event.is_set():
                        frame = reader.read()
                        if frame is None:
                            pass
                        else:
                            
                            try:
                                (t, sid, data) = frame
                                if t == DATA:
                                    g = room.get('guests', { }).get(sid)
                                    if g:
                                        
                                        try:
                                            g.sendall(data)
                                            
                                            try:
                                                pass
                                            except:
                                                if t == CLOSE:
                                                    g = room.get('guests', { }).pop(sid, None)
                                                    if g:
                                                        
                                                        try:
                                                            g.close()
                                                            
                                                            try:
                                                                if not self.stop_event.is_set():
                                                                    continue
                                                                room['online'] = False
                                                                room['host_conn'] = None
                                                                for g in list(room.get('guests', { }).values()):
                                                                    g.close()
                                                                room['guests'] = { }
                                                                self._say('房主 %s 断开' % name)
                                                                
                                                                try:
                                                                    conn.close()
                                                                    return None
                                                                    if not None:
                                                                        pass
                                                                    continue
                                                                    return None
                                                                    if not None:
                                                                        pass
                                                                    continue
                                                                    if not None:
                                                                        pass
                                                                    continue
                                                                    except Exception:
                                                                        room['guests'].pop(sid, None)
                                                                        
                                                                        try:
                                                                            continue
                                                                            
                                                                            try:
                                                                                except Exception:
                                                                                    
                                                                                    try:
                                                                                        continue
                                                                                        
                                                                                        try:
                                                                                            pass
                                                                                        except Exception:
                                                                                            continue
                                                                                            except Exception:
                                                                                                continue
                                                                                            return None


    def _as_guest(self, conn, addr, room_id, token):
        with self.store.lock:
            name = self.store.data['tokens'].get(token)

        if not name:
            
            try:
                conn.sendall(b'ERR\n')
                conn.close()
                return None
                room = self.store.data['rooms'].get(room_id)
                if not room or room.get('host_conn'):
                    with self.plock:
                        self.pending.setdefault(room_id, []).append((conn, token))

                    deadline = time.time() + 20
                    if time.time() < deadline:
                        room = self.store.data['rooms'].get(room_id)
                        if room and room.get('host_conn'):
                            with self.plock:
                                lst = self.pending.get(room_id, [])
                                if (conn, token) in lst:
                                    lst.remove((conn, token))
                                    self._link(room_id, conn, token)

                            return None

                        time.sleep(0.3)
                        if time.time() < deadline:
                            continue
                    with self.plock:
                        lst = self.pending.get(room_id, [])
                        if (conn, token) in lst:
                            pass
                        lst.remove((conn, token))

                    
                    try:
                        conn.close()
                        return None
                        self._link(room_id, conn, token)
                        return None
                        if not None:
                            pass
                        continue
                        return None
                        if not None:
                            pass
                        continue
                        if not None:
                            pass
                        continue
                        if not None:
                            pass
                        continue
                    except Exception:
                        return None


    def _link(self, room_id, conn, token):
        room = self.store.data['rooms'].get(room_id)
        if not room or room.get('host_conn'):
            
            try:
                conn.close()
                return None
                sid = room.get('next_sid', 1)
                room['next_sid'] = sid + 1
                room['guests'][sid] = conn
                
                try:
                    room['host_conn'].sendall(pack(OPEN, sid))
                    self._say('客人接入房间 %s（通道 %d）' % (room_id, sid))
                    
                    try:
                        data = conn.recv(BUFSIZE)
                        if not data:
                            pass
                        else:
                            
                            try:
                                room['host_conn'].sendall(pack(DATA, sid, data))
                                continue
                                room['guests'].pop(sid, None)
                                
                                try:
                                    room['host_conn'].sendall(pack(CLOSE, sid))
                                    
                                    try:
                                        conn.close()
                                        return None
                                        return None
                                        except Exception:
                                            room['guests'].pop(sid, None)
                                            conn.close()
                                        except Exception:
                                            pass
                                        return None
                                        continue
                                        continue
                                    except Exception:
                                        return None


    def stop(self):
        self.stop_event.set()
        
        try:
            self.sock.close()
            return None
        except Exception:
            return None


    return __class__


class ApiHandler(BaseHTTPRequestHandler):
    server_version = 'QCL/%s' % APP_VERSION
    store: Store = None
    update_dir: str = ''
    relay_port: int = DEFAULT_RELAY_PORT
    logger = None
    
    def log_message(self, fmt, *args):
        pass

    
    def _send(self, code, data, ctype, raw):
        if raw is not None:
            pass
        elif data is not None:
            pass
        
        body = data({ }, False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        
        try:
            self.wfile.write(body)
            return None
        except Exception:
            json.dumps
            return None


    def _body(self):
        if not self.headers.get('Content-Length'):
            self.headers.get('Content-Length')
        n = int(0)
        if not n:
            pass
        return { }
        
        try:
            return json.loads(self.rfile.read(n).decode('utf-8', 'ignore'))
        except Exception:
            return 


    def _token(self):
        h = self.headers.get('Authorization', '')
        return h.replace('Bearer', '').strip()

    _query_int = (lambda q, key, default: try:
if not q:
qfor part in ''.lstrip('?').split('&'):
if not '=' in part:
continuetry:
(k, v) = part.split('=', 1)if not k == key:
continuetry:
''.lstrip('?').split('&'), int(v)try:
defaultexcept Exception:
default)()
    
    def _user(self, token):
        if not token:
            token
        return self.store.data['tokens'].get(self._token())

    
    def _need(self, token):
        u = self._user(token)
        if not u:
            pass
        raise PermissionError('登录状态已失效')

    
    def _say(self, msg):
        if ApiHandler.logger:
            ApiHandler.logger(msg)
        return None

    
    def do_GET(self):
        path = self.path.split('?')[0]
        q = self.path[len(path):]
        
        try:
            if path == '/api/ping':
                pass
            return self._send(200, {
                'ok': True,
                'app': APP_NAME,
                'version': APP_VERSION,
                'time': int(time.time()),
                'relay_port': ApiHandler.relay_port,
                'users': len(self.store.data['users']) })
            
            try:
                if path == '/api/update/manifest':
                    pass
                return self._update_manifest()
                
                try:
                    if path.startswith('/download/'):
                        pass
                    return self._download(path[len('/download/'):])
                    
                    try:
                        if not path.startswith('/api/'):
                            pass
                        return self._send(404, {
                            'error': 'not found' })
                        
                        try:
                            self._need()
                            me = self._user()
                            if path == '/api/account/me':
                                u = self.store.data['users'].get(me, { })
                            return self._send(200, {
                                'username': me,
                                'nickname': u.get('nickname', me),
                                'status': u.get('status', ''),
                                'playing': u.get('playing', '') })
                            
                            try:
                                if path == '/api/friend/list':
                                    pass
                                return self._friend_list(me)
                                
                                try:
                                    if path == '/api/room/list':
                                        pass
                                    return self._room_list(me)
                                    
                                    try:
                                        if path == '/api/room/info':
                                            pass
                                        return self._room_info(me)
                                        
                                        try:
                                            if path == '/api/forum/posts':
                                                pass
                                            return self._forum_list()
                                            
                                            try:
                                                if path == '/api/chat/messages':
                                                    pass
                                                return self._chat_list(self._query_int(q, 'since'))
                                                
                                                try:
                                                    self._send(404, {
                                                        'error': 'not found' })
                                                    return None
                                                except PermissionError:
                                                    e = None
                                                    self._send(401, {
                                                        'error': str(e) })
                                                    e = None
                                                    del e
                                                    return None
                                                    e = None
                                                    del e
                                                    except Exception:
                                                        e = None
                                                        self._send(500, {
                                                            'error': str(e) })
                                                        e = None
                                                        del e
                                                        return None
                                                        e = None
                                                        del e


    def do_POST(self):
        path = self.path.split('?')[0]
        data = self._body()
        
        try:
            if path == '/api/account/register':
                pass
            return self._register(data)
            
            try:
                if path == '/api/account/login':
                    pass
                return self._login(data)
                
                try:
                    if not path.startswith('/api/'):
                        pass
                    return self._send(404, {
                        'error': 'not found' })
                    
                    try:
                        self._need()
                        me = self._user()
                        if path == '/api/account/status':
                            pass
                        return self._status(me, data)
                        
                        try:
                            if path == '/api/room/heartbeat':
                                with self.store.lock:
                                    u = self.store.data['users'].get(me, { })
                                    u['last_seen'] = int(time.time())
                                    
                                    try:

                                        room = self.store.data['rooms'].get(me)
                                        if room:
                                            room['last_seen'] = int(time.time())
                                        return self._send(200, {
                                            'ok': True })
                                        
                                        try:
                                            if path == '/api/friend/add':
                                                pass
                                            return self._friend_add(me, data)
                                            
                                            try:
                                                if path == '/api/friend/accept':
                                                    pass
                                                return self._friend_accept(me, data)
                                                
                                                try:
                                                    if path == '/api/friend/remove':
                                                        pass
                                                    return self._friend_remove(me, data)
                                                    
                                                    try:
                                                        if path == '/api/room/create':
                                                            pass
                                                        return self._room_create(me, data)
                                                        
                                                        try:
                                                            if path == '/api/room/update':
                                                                pass
                                                            return self._room_update(me, data)
                                                            
                                                            try:
                                                                if path == '/api/room/close':
                                                                    pass
                                                                return self._room_close(me)
                                                                
                                                                try:
                                                                    if path == '/api/room/resolve':
                                                                        pass
                                                                    return self._room_resolve(me, data)
                                                                    
                                                                    try:
                                                                        if path == '/api/forum/post':
                                                                            pass
                                                                        return self._forum_post(me, data)
                                                                        
                                                                        try:
                                                                            if path == '/api/forum/reply':
                                                                                pass
                                                                            return self._forum_reply(me, data)
                                                                            
                                                                            try:
                                                                                if path == '/api/chat/send':
                                                                                    pass
                                                                                return self._chat_send(me, data)
                                                                                
                                                                                try:
                                                                                    self._send(404, {
                                                                                        'error': 'not found' })
                                                                                    return None
                                                                                    if not None:
                                                                                        pass
                                                                                    
                                                                                    try:
                                                                                        continue
                                                                                    except PermissionError:
                                                                                        e = None
                                                                                        self._send(401, {
                                                                                            'error': str(e) })
                                                                                        e = None
                                                                                        del e
                                                                                        return None
                                                                                        e = None
                                                                                        del e
                                                                                        except Exception:
                                                                                            e = None
                                                                                            self._send(500, {
                                                                                                'error': str(e) })
                                                                                            e = None
                                                                                            del e
                                                                                            return None
                                                                                            e = None
                                                                                            del e


    def _forum_list(self):
        with self.store.lock:
            if not self.store.data.get('forum'):
                self.store.data.get('forum')
            posts = list([])

        posts.sort((lambda p: p.get('ts', 0)), True)
        return self._send(200, {
            'posts': posts[:100] })
        if not None:
            pass
        continue

    
    def _forum_post(self, me, d):
        if not d.get('title'):
            d.get('title')
        title = ''.strip()
        if not d.get('body'):
            d.get('body')
        body = ''.strip()
        if not title:
            pass
        raise ValueError('标题不能为空')
        if len(title) > 60:
            pass
        raise ValueError('标题最多 60 个字')
        if not body:
            pass
        raise ValueError('内容不能为空')
        if len(body) > 4000:
            pass
        raise ValueError('内容最多 4000 个字')
        with self.store.lock:
            posts = self.store.data.setdefault('forum', [])
        , []
        if not p,:
            p,
        None, posts, p([
            0]) + 1 = max
        posts.append({
            'id': pid,
            'title': title,
            'body': body,
            'author': me,
            'ts': int(time.time()),
            'replies': [] })

        self.store.save()
        return self._send(200, {
            'ok': True,
            'id': pid })
        
        if not p,:
            pass
        None, None, None
        continue

    
    def _forum_reply(self, me, d):
        if not d.get('post_id'):
            d.get('post_id')
        pid = int(0)
        if not d.get('body'):
            d.get('body')
        body = ''.strip()
        if not body:
            pass
        raise ValueError('回复内容不能为空')
        if len(body) > 2000:
            pass
        raise ValueError('回复最多 2000 个字')
        with self.store.lock:
            if not self.store.data.get('forum'):
                self.store.data.get('forum')
            for p in []:
                if not p.get('id') == pid:
                    continue
                p.setdefault('replies', []).append({
                    'author': me,
                    'body': body,
                    'ts': int(time.time()) })
                []
            raise ValueError('帖子不存在（可能已被主机清理）')

            self.store.save()
            return self._send(200, {
                'ok': True })
            if not None:
                pass
        continue

    
    def _chat_list(self, since):
        with self.store.lock:
            if not self.store.data.get('chat'):
                self.store.data.get('chat')
        
        , [], msgs = [], m
        m = None

        return self._send(200, {
            'messages': msgs[-200:] })
        
        if not m,:
            pass
        None, None, None
        continue

    
    def _chat_send(self, me, d):
        if not d.get('text'):
            d.get('text')
        text = ''.strip()
        if not text:
            pass
        raise ValueError('不能发送空消息')
        if len(text) > 500:
            pass
        raise ValueError('单条消息最多 500 个字')
        with self.store.lock:
            msgs = self.store.data.setdefault('chat', [])
        , []
        if not m,:
            m,
        None, msgs, m([
            0]) + 1 = max
        msgs.append({
            'id': mid,
            'user': me,
            'text': text,
            'ts': int(time.time()) })
        if len(msgs) > 500:
            pass
        del msgs[:len(msgs) - 500]

        self.store.save()
        return self._send(200, {
            'ok': True,
            'id': mid })
        
        if not m,:
            pass
        None, None, None
        continue

    _hash = (lambda pw, salt: hashlib.pbkdf2_hmac('sha256', pw.encode(), salt.encode(), 120000).hex())()
    
    def _register(self, d):
        if not d.get('username'):
            d.get('username')
        name = ''.strip()
        if not d.get('password'):
            d.get('password')
        pw = ''
        if len(name) < 3 or len(name) > 20:
            pass
        raise ValueError('用户名需 3-20 个字符')
        if len(pw) < 6:
            pass
        raise ValueError('密码至少 6 位')
        with self.store.lock:
            pass
        , []
        if name.lower(), self.store.data['users'], u in u,:
            pass
        raise ValueError('该用户名已被注册')
        secrets.token_hex(8) = None
        if not d.get('nickname'):
            d.get('nickname')
        self.store.data['users'][name] = {
            'password': self._hash(pw, salt),
            'salt': salt,
            'nickname': name,
            'created': int(time.time()),
            'last_seen': int(time.time()),
            'friends': [],
            'pending': [],
            'status': '',
            'playing': '',
            'token': '' }

        self.store.save()
        self._say('新用户注册：%s' % name)
        return self._login(d)
        
        if not u,:
            pass
        None, None, None
        continue

    
    def _login(self, d):
        if not d.get('username'):
            d.get('username')
        name = ''.strip()
        if not d.get('password'):
            d.get('password')
        pw = ''
        with self.store.lock:
            real = None
            for u in self.store.data['users']:
                if not u.lower() == name.lower():
                    continue
                real = u
                self.store.data['users']
            if not real:
                pass
        raise PermissionError('用户名或密码错误')
        u = self.store.data['users'][real]
        if u['password'] != self._hash(pw, u['salt']):
            pass
        raise PermissionError('用户名或密码错误')
        old = u.get('token')
        if old:
            pass
        self.store.data['tokens'].pop(old, None)
        tok = secrets.token_hex(24)
        u['token'] = tok
        u['last_seen'] = int(time.time())
        self.store.data['tokens'][tok] = real

        self.store.save()
        return self._send(200, {
            'token': tok,
            'username': real,
            'nickname': u.get('nickname', real) })
        if not None:
            pass
        continue

    
    def _status(self, me, d):
        with self.store.lock:
            u = self.store.data['users'].get(me, { })
            u['status'] = d.get('status', '')
            u['playing'] = d.get('playing', '')
            u['last_seen'] = int(time.time())

        return self._send(200, {
            'ok': True })
        if not None:
            pass
        continue

    
    def _friend_add(self, me, d):
        if not d.get('username'):
            d.get('username')
        target = ''.strip()
        if not target:
            pass
        raise ValueError('请输入用户名')
        if target.lower() == me.lower():
            pass
        raise ValueError('不能添加自己')
        with self.store.lock:
            if target not in self.store.data['users']:
                pass
            raise ValueError('用户不存在')
            u = self.store.data['users'][me]
            t = self.store.data['users'][target]
            if target in u['friends']:
                (None, None)
        return None, self._send(200, {
            'ok': True,
            'msg': '已经是好友' })
        if target in u['pending']:
            (None, None)
        return None, self._send(200, {
            'ok': True,
            'msg': '请求已发送' })
        if me in t['pending']:
            t['pending'].remove(me)
            u['friends'].append(target)
            t['friends'].append(me)
            self.store.save()
            (None, None)
        return None, self._send(200, {
            'ok': True,
            'msg': '已成为好友' })
        t['pending'].append(me)

        self.store.save()
        return self._send(200, {
            'ok': True,
            'msg': '好友请求已发送' })
        if not None:
            pass
        continue

    
    def _friend_accept(self, me, d):
        if not d.get('username'):
            d.get('username')
        target = ''.strip()
        with self.store.lock:
            u = self.store.data['users'][me]
            if target not in u['pending']:
                (None, None)
        return None, self._send(200, {
            'ok': True,
            'msg': '没有该请求' })
        u['pending'].remove(target)
        if t:
            u['friends'].append(target)
            t['friends'].append(me)
            if me in t.get('pending', []):
                pass
        t['pending'].remove(me)
        self.store.data['users'].get(target)(None, None)
        self.store.save()
        return self._send(200, {
            'ok': True,
            'msg': '已添加好友' })
        if not None:
            pass
        continue

    
    def _friend_remove(self, me, d):
        if not d.get('username'):
            d.get('username')
        target = ''.strip()
        with self.store.lock:
            u = self.store.data['users'].get(me, { })
            t = self.store.data['users'].get(target, { })
            if target in u.get('friends', []):
                pass
            u['friends'].remove(target)
            if me in t.get('friends', []):
                pass
            t['friends'].remove(me)

        self.store.save()
        return self._send(200, {
            'ok': True })
        if not None:
            pass
        continue

    
    def _friend_list(self, me):
        with self.store.lock:
            u = self.store.data['users'].get(me, { })
            out = []
            for f in u.get('friends', []):
                fu = self.store.data['users'].get(f, { })
                room = self.store.data['rooms'].get(f, { })
                if bool(room.get('online')):
                    bool(room.get('online'))
                out.append({
                    'username': f,
                    'nickname': fu.get('nickname', f),
                    'online': int(time.time()) - int(fu.get('last_seen', 0)) < 90,
                    'status': fu.get('status', ''),
                    'playing': fu.get('playing', ''),
                    'in_room': room.get('port', 0) > 0,
                    'room_mc': room.get('mc', ''),
                    'room_name': room.get('name', '') })
            pending = list(u.get('pending', []))

        return self._send(200, {
            'friends': out,
            'pending': pending })
        if not None:
            pass
        continue

    
    def _room_create(self, me, d):
        with self.store.lock:
            if self.store.data['rooms'].get(me, { }).get('online'):
                pass
            if not d.get('name'):
                d.get('name')
            if not d.get('port'):
                d.get('port')
            self.store.data['rooms'][me] = {
                'owner': me,
                'name': '%s 的世界' % me,
                'mc': d.get('mc', ''),
                'port': int(0),
                'mode': d.get('mode', 'auto'),
                'created': int(time.time()),
                'last_seen': int(time.time()),
                'online': False,
                'host_conn': None,
                'guests': { },
                'next_sid': 1,
                'ip': '' }

        if not d.get('name'):
            d.get('name')
        return self._send(200, {
            'ok': True,
            'room_id': me,
            'relay_port': ApiHandler.relay_port,
            'name': '%s 的世界' % me })
        if not None:
            pass
        continue

    
    def _room_update(self, me, d):
        with self.store.lock:
            room = self.store.data['rooms'].get(me)
            if not room:
                pass
            raise ValueError('请先创建房间')
            if d.get('port'):
                room['port'] = int(d['port'])
            if d.get('mc'):
                room['mc'] = d['mc']
            room['last_seen'] = int(time.time())

        return self._send(200, {
            'ok': True })
        if not None:
            pass
        continue

    
    def _room_close(self, me):
        with self.store.lock:
            self.store.data['rooms'].pop(me, None)

        return self._send(200, {
            'ok': True })
        if not None:
            pass
        continue

    
    def _room_info(self, me):
        with self.store.lock:
            r = dict(self.store.data['rooms'].get(me, { }))

        r.pop('host_conn', None)
        r.pop('guests', None)
        return self._send(200, {
            'room': r })
        if not None:
            pass
        continue

    
    def _room_list(self, me):
        with self.store.lock:
            u = self.store.data['users'].get(me, { })
            friends = list(u.get('friends', []))
            out = []
            for owner, r in self.store.data['rooms'].items():
                if not r.get('online') or r.get('port'):
                    continue
                if owner != me and owner not in friends:
                    continue
                out.append({
                    'room_id': owner,
                    'owner': owner,
                    'name': r.get('name', ''),
                    'mc': r.get('mc', ''),
                    'players': len(r.get('guests', { })),
                    'created': r.get('created', 0),
                    'ip': r.get('ip', '') })

        out.sort((lambda x: -x.get('created', 0)))
        return self._send(200, {
            'rooms': out })
        if not None:
            pass
        continue

    
    def _room_resolve(self, me, d):
        if not d.get('owner'):
            d.get('owner')
            if not d.get('room_id'):
                d.get('room_id')
        target = ''.strip()
        with self.store.lock:
            real = None
            for u in self.store.data['users']:
                if not u.lower() == target.lower():
                    continue
                real = u
                self.store.data['users']
            if not real:
                pass
        raise ValueError('用户不存在')
        r = self.store.data['rooms'].get(real)
        if not r and r.get('online') or r.get('port'):
            pass
        raise ValueError('对方尚未开启联机世界')
        (None, None)
        return None, self._send(200, {
            'room_id': real,
            'owner': real,
            'mc': r.get('mc', ''),
            'name': r.get('name', ''),
            'ip': r.get('ip', ''),
            'port': r.get('port'),
            'relay_port': ApiHandler.relay_port })
        if not None:
            pass

    
    def _update_manifest(self):
        p = os.path.join(ApiHandler.update_dir, 'manifest.json')
        if not os.path.exists(p):
            pass
        return self._send(404, {
            'error': '暂无发布版本' })
        
        try:
            with open(p, 'r', 'utf-8') as f:
                
                try:
                    (None, None)
                    return None, self._send(200, json.load(f))
                    if not None:
                        pass
                    
                    try:
                        return None
                        
                        try:
                            pass
                        except Exception:
                            del e
                            return None
                            None = 
                            del e


    def _download(self, name):
        name = os.path.basename(name)
        p = os.path.join(ApiHandler.update_dir, name)
        if not os.path.exists(p):
            pass
        return self._send(404, {
            'error': '文件不存在' })
        
        try:
            with open(p, 'rb') as f:
                raw = f.read()
                
                try:

                    return self._send(200, raw, 'application/octet-stream')
                    if not None:
                        pass
                    
                    try:
                        continue
                    except Exception:
                        e = None
                        del e
                        return None
                        None = 
                        del e


class QCLServer:
    
    def __init__(self, api_port = DEFAULT_API_PORT, relay_port = DEFAULT_RELAY_PORT, data_dir = '', update_dir = '', log = None):
        self.api_port = api_port
        self.relay_port = relay_port
        self.data_dir = data_dir
        self.update_dir = update_dir
        self.log = log
        self.store = Store(os.path.join(data_dir, 'server_data.json'))
        self.http = None
        self.relay = None
        self._hb = None

    
    def start(self):
        ApiHandler.store = self.store
        ApiHandler.update_dir = self.update_dir
        ApiHandler.relay_port = self.relay_port
        ApiHandler.logger = self.log
        self.http = ThreadingHTTPServer(('0.0.0.0', self.api_port), ApiHandler)
        threading.Thread(self.http.serve_forever, True).start()
        self.relay = RelayServer(self.relay_port, self.store, self.log)
        self.relay.start()
        self._hb = threading.Thread(self._cleaner, True)
        self._hb.start()
        if self.log:
            pass
        self.log('QCL 主机服务已启动：API %d / 中继 %d' % (self.api_port, self.relay_port))
        return self

    
    def _cleaner(self):
        time.sleep(60)
        
        try:
            now = int(time.time())
            with self.store.lock:
                for rid, r in list(self.store.data['rooms'].items()):
                    if r.get('online'):
                        continue
                    if not now - r.get('last_seen', now) > 21600:
                        continue
                    self.store.data['rooms'].pop(rid, None)
                
                try:

                    self.store.save()
                    continue
                    if not None:
                        pass
                    
                    try:
                        continue
                    except Exception:
                        continue


    def stop(self):
        
        try:
            self.http.shutdown()
            
            try:
                self.http.server_close()
                
                try:
                    self.relay.stop()
                    
                    try:
                        self.store.save()
                        return None
                        continue
                        continue
                        continue
                    except Exception:
                        return None

