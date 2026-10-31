# Source Generated with Decompyle++
# File: account.pyc (Python 3.13)

'''QCL 联机账号：注册 / 登录 / 好友 / 房间（与主机通信）'''
import time
import requests
TIMEOUT = 8

class ApiError(Exception):
    pass


class Api:
    
    def __init__(self, base):
        if not base:
            base
        self.base = ''.rstrip('/')

    
    def set_base(self, base):
        self.base = base.rstrip('/')

    
    def _headers(self, token):
        h = {
            'Content-Type': 'application/json',
            'Accept': 'application/json' }
        if token:
            h['Authorization'] = 'Bearer %s' % token
        return h

    
    def _call(self, method, path, payload = None, token = None, timeout = TIMEOUT):
        if not self.base:
            pass
        raise ApiError('未设置主机地址')
        url = self.base + path
        
        try:
            if method == 'GET':
                r = requests.get(url, payload, self._headers(token), timeout)
            else:
                
                try:
                    if not payload:
                        payload
                    r = requests.post(url, { }, self._headers(token), timeout)
                    data = { }
                    
                    try:
                        data = r.json() if r.content else { }
                        if r.status_code >= 400 or data.get('error'):
                            if not data.get('error'):
                                data.get('error')
                        raise ApiError('HTTP %s' % r.status_code)
                        return data
                        except requests.RequestException:
                            e = None
                            raise ApiError('主机不在线或无法连接（%s）' % self.base)
                            e = None
                            del e
                    except Exception:
                        data = { }
                        continue


    def ping(self):
        return self._call('GET', '/api/ping', 4)

    
    def update_manifest(self):
        return self._call('GET', '/api/update/manifest', 6)

    
    def register(self, username, password, nickname):
        if not nickname:
            nickname
        return self._call('POST', '/api/account/register', {
            'username': username,
            'password': password,
            'nickname': username }, 10)

    
    def login(self, username, password):
        return self._call('POST', '/api/account/login', {
            'username': username,
            'password': password }, 10)

    
    def me(self, token):
        return self._call('GET', '/api/account/me', token)

    
    def update_status(self, token, status, playing):
        return self._call('POST', '/api/account/status', {
            'status': status,
            'playing': playing }, token)

    
    def friend_add(self, token, target):
        return self._call('POST', '/api/friend/add', {
            'username': target }, token)

    
    def friend_accept(self, token, target):
        return self._call('POST', '/api/friend/accept', {
            'username': target }, token)

    
    def friend_remove(self, token, target):
        return self._call('POST', '/api/friend/remove', {
            'username': target }, token)

    
    def friend_list(self, token):
        return self._call('GET', '/api/friend/list', token)

    
    def room_create(self, token, mc, name, port, mode):
        return self._call('POST', '/api/room/create', {
            'mc': mc,
            'name': name,
            'port': port,
            'mode': mode }, token, 10)

    
    def room_update(self, token, port, mc):
        return self._call('POST', '/api/room/update', {
            'port': port,
            'mc': mc }, token)

    
    def room_close(self, token):
        return self._call('POST', '/api/room/close', { }, token)

    
    def room_list(self, token):
        return self._call('GET', '/api/room/list', token)

    
    def room_info(self, token):
        return self._call('GET', '/api/room/info', token)

    
    def room_resolve(self, token, owner, room_id):
        return self._call('POST', '/api/room/resolve', {
            'owner': owner,
            'room_id': room_id }, token)

    
    def heartbeat(self, token):
        return self._call('POST', '/api/room/heartbeat', { }, token, 5)

    
    def forum_posts(self, token):
        return self._call('GET', '/api/forum/posts', token)

    
    def forum_post(self, token, title, body):
        return self._call('POST', '/api/forum/post', {
            'title': title,
            'body': body }, token, 10)

    
    def forum_reply(self, token, post_id, body):
        return self._call('POST', '/api/forum/reply', {
            'post_id': post_id,
            'body': body }, token, 10)

    
    def chat_messages(self, token, since):
        return self._call('GET', '/api/chat/messages', {
            'since': since }, token, 6)

    
    def chat_send(self, token, text):
        return self._call('POST', '/api/chat/send', {
            'text': text }, token, 6)


def cached_user():
    settings = settings
    # import  # [decompiler] module name lost
    if not settings.settings.get('qcl_user'):
        settings.settings.get('qcl_user')
    return { }


def save_user(user):
    settings = settings
    # import  # [decompiler] module name lost
    settings.settings.set('qcl_user', user)


def clear_user():
    settings = settings
    # import  # [decompiler] module name lost
    settings.settings.set('qcl_user', None)


def token():
    u = cached_user()
    if u:
        pass
    return u.get('token', '')
    return ''


def username():
    u = cached_user()
    if u:
        pass
    return u.get('username', '')
    return ''


def online():
    if token():
        token()
        if not cached_user().get('expire', 0):
            cached_user().get('expire', 0)
    if not time.time() < 0:
        time.time() < 0
    return bool(token())

