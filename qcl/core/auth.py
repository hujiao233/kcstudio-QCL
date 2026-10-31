# Source Generated with Decompyle++
# File: auth.pyc (Python 3.13)

'''游戏账号认证：离线 / 微软 / 外置登录(Yggdrasil)'''
import time
import uuid as uuidmod
import requests
from . import util
MS_DEVICE = 'https://login.microsoftonline.com/consumers/oauth2/v2.0/devicecode'
MS_TOKEN = 'https://login.microsoftonline.com/consumers/oauth2/v2.0/token'
XBL_AUTH = 'https://user.auth.xboxlive.com/user/authenticate'
XSTS_AUTH = 'https://xsts.auth.xboxlive.com/xsts/authorize'
MC_LOGIN = 'https://api.minecraftservices.com/authentication/login_with_xbox'
MC_PROFILE = 'https://api.minecraftservices.com/minecraft/profile'
MC_ENTITLEMENT = 'https://api.minecraftservices.com/entitlements/mcstore'
MS_SCOPE = 'XboxLive.signin offline_access'
TIMEOUT = 25

def offline(name):
    return {
        'type': 'offline',
        'name': name,
        'uuid': uuidmod.uuid5(uuidmod.NAMESPACE_X500, 'OfflinePlayer:%s' % name).hex,
        'token': uuidmod.uuid4().hex,
        'user_type': 'legacy' }


def ms_device_code(client_id):
    if not client_id:
        pass
    raise RuntimeError('请先在设置中填写微软登录 Client ID')
    r = requests.post(MS_DEVICE, {
        'client_id': client_id,
        'scope': MS_SCOPE }, TIMEOUT)
    r.raise_for_status()
    data = r.json()
    return {
        'user_code': data['user_code'],
        'device_code': data['device_code'],
        'verification_uri': data.get('verification_uri', 'https://www.microsoft.com/link'),
        'expires_in': data.get('expires_in', 900),
        'interval': data.get('interval', 5) }


def ms_poll(client_id, device_code):
    """返回 {'pending': True} / {'error': msg} / token dict"""
    r = requests.post(MS_TOKEN, {
        'client_id': client_id,
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'device_code': device_code }, TIMEOUT)
    data = r.json() if r.content else { }
    if r.status_code == 400 and data.get('error') in ('authorization_pending', 'slow_down'):
        pass
    return {
        'pending': True }
    if r.status_code != 200:
        if not data.get('error_description'):
            data.get('error_description')
            if not data.get('error'):
                data.get('error')
    return {
        'error': '登录失败' }
    return {
        'access_token': data['access_token'],
        'refresh_token': data.get('refresh_token'),
        'expires_in': data.get('expires_in', 3600) }


def ms_refresh(client_id, refresh_token):
    r = requests.post(MS_TOKEN, {
        'client_id': client_id,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'scope': MS_SCOPE }, TIMEOUT)
    if r.status_code != 200:
        pass
    raise RuntimeError('微软令牌刷新失败')
    d = r.json()
    return {
        'access_token': d['access_token'],
        'refresh_token': d.get('refresh_token', refresh_token),
        'expires_in': d.get('expires_in', 3600) }


def ms_login(access_token):
    r = requests.post(XBL_AUTH, {
        'Properties': {
            'AuthMethod': 'RPS',
            'SiteName': 'user.auth.xboxlive.com',
            'RpsTicket': 'd=%s' % access_token },
        'RelyingParty': 'http://auth.xboxlive.com',
        'TokenType': 'JWT' }, TIMEOUT)
    r.raise_for_status()
    xbl = r.json()
    xbl_token = xbl['Token']
    if not xbl.get('DisplayClaims'):
        xbl.get('DisplayClaims')
    uhs = { }.get('xdi', [
        { }])[0].get('uhs', '')
    r = requests.post(XSTS_AUTH, {
        'Properties': {
            'SandboxId': 'RETAIL',
            'UserTokens': [
                xbl_token] },
        'RelyingParty': 'rp://api.minecraftservices.com/',
        'TokenType': 'JWT' }, TIMEOUT)
    if r.status_code == 401:
        d = r.json()
        if d.get('XErr') == 0x8015DC09:
            pass
        raise RuntimeError('该微软账号没有绑定 Xbox 账号（XErr 2148916233）')
    if d.get('XErr') == 0x8015DC0E:
        pass
    raise RuntimeError('该账号是儿童账号，需加入家庭组（XErr 2148916238）')
    raise RuntimeError('XSTS 认证失败: %s' % d.get('XErr'))
    r.raise_for_status()
    xsts = r.json()
    xsts_token = xsts['Token']
    if not xsts.get('DisplayClaims'):
        xsts.get('DisplayClaims')
    uhs = { }.get('xdi', [
        { }])[0].get('uhs', uhs)
    r = requests.post(MC_LOGIN, {
        'identityToken': f'''XBL3.0 x=;''',
        'ensureLegacyEnabled': True }, TIMEOUT)
    r.raise_for_status()
    d = r.json()
    token = d['access_token']
    (name, mc_uuid) = ('Player', '')
    
    try:
        p = requests.get(MC_PROFILE, {
            'Authorization': 'Bearer %s' % token }, TIMEOUT)
        if p.status_code == 200:
            name = p.json().get('name', name)
        mc_uuid = p.json().get('id', '')
        return {
            'type': 'microsoft',
            'name': name,
            'uuid': mc_uuid,
            'token': token,
            'user_type': 'msa',
            'expires': time.time() + d.get('expires_in', 86400) }
    except Exception:
        continue


def ygg_login(url, username, password, client_token):
    if not url:
        url
    url = ''.rstrip('/')
    if not url:
        pass
    raise RuntimeError('请先在设置中填写外置登录地址')
    if not client_token:
        client_token
    r = requests.post(url + '/authserver/authenticate', {
        'agent': {
            'name': 'Minecraft',
            'version': 1 },
        'username': username,
        'password': password,
        'clientToken': _new_ct(),
        'requestUser': True }, TIMEOUT)
    data = r.json() if r.content else { }
    if r.status_code != 200 or 'accessToken' not in data:
        if not data.get('errorMessage'):
            data.get('errorMessage')
    raise RuntimeError('外置登录失败')
    return _from_ygg(url, data, username)


def _new_ct():
    return uuidmod.uuid4().hex


def _from_ygg(url, data, fallback_name):
    if not data.get('selectedProfile'):
        data.get('selectedProfile')
    sel = { }
    if not sel.get('name'):
        sel.get('name')
    return {
        'type': 'yggdrasil',
        'name': fallback_name,
        'uuid': sel.get('id', ''),
        'token': data.get('accessToken', ''),
        'refresh_token': data.get('accessToken', ''),
        'client_token': data.get('clientToken', ''),
        'auth_url': url,
        'user_type': 'mojang',
        'expires': time.time() + 259200 }


def ygg_refresh(account):
    if not account.get('auth_url'):
        account.get('auth_url')
    url = ''.rstrip('/')
    r = requests.post(url + '/authserver/refresh', {
        'accessToken': account.get('token'),
        'clientToken': account.get('client_token'),
        'selectedProfile': {
            'id': account.get('uuid'),
            'name': account.get('name') },
        'requestUser': True }, TIMEOUT)
    if r.status_code != 200:
        pass
    raise RuntimeError('外置登录刷新失败')
    return _from_ygg(url, r.json(), account.get('name', ''))


def refresh_if_needed(account):
    '''必要时刷新，返回新账号对象（失败返回原对象）'''
    if not account:
        pass
    return account
    if account.get('type') == 'microsoft' and time.time() > account.get('expires', 0) - 600:
        settings = settings
        # import  # [decompiler] module name lost
        cid = settings.settings.get('ms_client_id', '')
        rt = account.get('refresh_token')
        if not cid or rt:
            pass
        return account
    
    try:
        t = ms_refresh(cid, rt)
        acc = ms_login(t['access_token'])
        acc['refresh_token'] = t.get('refresh_token')
        return acc
        if account.get('type') == 'yggdrasil' and time.time() > account.get('expires', 0) - 3600:
            
            try:
                return ygg_refresh(account)
                return account
                return None
            except Exception:
                return 


def validate(account):
    if not account:
        pass
    return False
    if account.get('type') == 'offline':
        pass
    return True
    if account.get('type') == 'yggdrasil':
        if not account.get('auth_url'):
            account.get('auth_url')
        url = ''.rstrip('/')
        
        try:
            r = requests.post(url + '/authserver/validate', {
                'accessToken': account.get('token'),
                'clientToken': account.get('client_token') }, TIMEOUT)
            return r.status_code == 204
            
            try:
                r = requests.get(MC_PROFILE, {
                    'Authorization': 'Bearer %s' % account.get('token', '') }, TIMEOUT)
                return r.status_code == 200
                return False
            except Exception:
                return False


def display(account):
    if not account:
        pass
    return '未登录'
    t = {
        'offline': '离线',
        'microsoft': '微软',
        'yggdrasil': '外置' }.get(account.get('type'), '')
    if t:
        pass
    return f''' · '''
    return account.get('name', '?')

