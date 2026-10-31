# Source Generated with Decompyle++
# File: relay.pyc (Python 3.13)

'''虚拟网隧道：房主端 / 客户端本地代理 / 协议帧'''
import select
import socket
import struct
import threading
import time
from .constants import LAN_MULTICAST_GROUP, LAN_MULTICAST_PORT
(OPEN, DATA, CLOSE) = (0, 1, 2)
BUFSIZE = 65536

def pack(t, sid, data):
    payload = bytes([
        t]) + struct.pack('>H', sid) + data
    return struct.pack('>H', len(payload)) + payload


class FrameReader:
    
    def __init__(self, sock):
        self.sock = sock
        self.buf = b''

    
    def read(self):
        '''返回 (type, sid, data)，连接关闭返回 None'''
        if len(self.buf) >= 2:
            (n,) = struct.unpack('>H', self.buf[:2])
            if len(self.buf) >= 2 + n:
                payload = self.buf[2:2 + n]
                self.buf = self.buf[2 + n:]
                if n >= 3:
                    t = payload[0]
                    sid = struct.unpack('>H', payload[1:3])[0]
                return (t, sid, payload[3:])
            
            try:
                chunk = self.sock.recv(BUFSIZE)
                if not chunk:
                    pass
                return None
                continue
            except Exception:
                return None


class Stopper:
    
    def __init__(self):
        self._e = threading.Event()

    
    def set(self):
        self._e.set()

    stopped = (lambda self: self._e.is_set())()


def _recv_line(sock, timeout):
    sock.settimeout(timeout)
    buf = b''
    
    try:
        if buf.endswith(b'\n') and len(buf) < 4096:
            d = sock.recv(1)
            if not d:
                pass
            else:
                
                try:
                    buf += d
                    if buf.endswith(b'\n') and len(buf) < 4096:
                        continue
                    return buf.decode('utf-8', 'ignore').strip()
                except Exception:
                    continue


def _pump(a, b, stop):
    
    try:
        if not stop.stopped:
            (r,)
            for None in r:
                data = s.recv(BUFSIZE)
                
                try:
                    if not data:
                        select.select([
                            a,
                            b], [], [], 0.5)
                        for s in (a, b):
                            s.close()
                    return None
                    b if s is a else a.sendall(data)
                    
                    try:
                        continue
                        if not stop.stopped:
                            continue
                        for s in (a, b):
                            s.close()
                        return None
                        except Exception:
                            
                            try:
                                for s in (a, b):
                                    s.close()
                                    except Exception:
                                        continue
                                return None
                                
                                try:
                                    except Exception:
                                        continue
                                    except Exception:
                                        
                                        try:
                                            for s in (a, b):
                                                s.close()
                                                except Exception:
                                                    continue
                                            return None
                                            
                                            try:
                                                pass
                                            except Exception:
                                                
                                                try:
                                                    continue
                                                    
                                                    try:
                                                        except Exception:
                                                            continue
                                                    except:
                                                        for s in (a, b):
                                                            s.close()
                                                            except Exception:
                                                                continue


class HostTunnel:
    __doc__ = '房主启动器：与服务器保持一条控制连接，把各客人的流量转到本机 MC 端口'
    
    def __init__(self, host, port, room_id, token, lan_port, log, on_status):
        self.addr = (host, port)
        self.room_id = room_id
        self.token = token
        self.lan_port = lan_port
        self.log = log
        self.on_status = on_status
        self.stop = Stopper()
        self.sock = None
        self.streams = { }
        self.lock = threading.Lock()
        self.thread = None

    
    def start(self):
        self.thread = threading.Thread(self._run, True)
        self.thread.start()
        return self

    
    def _say(self, msg):
        if self.log:
            self.log(msg)
        return None

    
    def _connect(self):
        s = socket.create_connection(self.addr, 15)
        s.settimeout(None)
        s.sendall(('HOST %s %s %d\n' % (self.room_id, self.token, self.lan_port)).encode())
        return s

    
    def _run(self):
        
        try:
            self.sock = self._connect()
            self._say('虚拟网已连接主机 %s:%s' % self.addr)
            if self.on_status:
                pass
            self.on_status(True, '已连接')
            reader = FrameReader(self.sock)
            
            try:
                if not self.stop.stopped:
                    frame = reader.read()
                    if frame is None:
                        
                        try:
                            pass
                        try:
                            (t, sid, data) = frame
                            if t == OPEN:
                                self._open_stream(sid)
                            elif t == DATA:
                                with self.lock:
                                    st = self.streams.get(sid)
                                    
                                    try:
                                        None(None, None)
                                        if st:
                                            
                                            try:
                                                st.sendall(data)
                                                
                                                try:
                                                    pass
                                                except:
                                                    if t == CLOSE:
                                                        pass
                                                    self._close_stream(sid)

                                                if not self.stop.stopped:
                                                    continue
                                                self.close()
                                                return None
                                                except Exception:
                                                    e = None
                                                    self._say('连接主机失败：%s' % e)
                                                    if self.on_status:
                                                        pass
                                                    self.on_status(False, '连接主机失败')
                                                    e = None
                                                    del e
                                                    return None
                                                    e = None
                                                    del e
                                                if not None:
                                                    pass
                                                
                                                try:
                                                    continue
                                                    except Exception:
                                                        self._close_stream(sid)
                                                        
                                                        try:
                                                            continue
                                                            
                                                            try:
                                                                pass
                                                            except Exception:
                                                                e = None
                                                                self._say('虚拟网断开：%s' % e)
                                                                
                                                                try:
                                                                    e = None
                                                                    del e
                                                                    continue
                                                                    e = None
                                                                    del e
                                                                    
                                                                    try:
                                                                        pass
                                                                    except:
                                                                        self.close()


    def _open_stream(self, sid):
        
        try:
            local = socket.create_connection(('127.0.0.1', self.lan_port), 5)
            with self.lock:
                self.streams[sid] = local
            None(None, None)
            threading.Thread(self._stream_reader, (sid, local), True).start()
            self._say('有玩家接入（通道 %d）' % sid)
            return None
        except Exception:
            self.sock.sendall(pack(CLOSE, sid))
        except Exception:
            pass

        return None
        if not None:
            pass
        continue

    
    def _stream_reader(self, sid, local):
        
        try:
            if not self.stop.stopped:
                data = local.recv(BUFSIZE)
                if not data:
                    pass
                else:
                    
                    try:
                        self.sock.sendall(pack(DATA, sid, data))
                        if not self.stop.stopped:
                            continue
                        self._close_stream(sid)
                        return None
                    except Exception:
                        continue


    def _close_stream(self, sid):
        with self.lock:
            st = self.streams.pop(sid, None)
        None(None, None)
        if st:
            
            try:
                st.close()
                
                try:
                    self.sock.sendall(pack(CLOSE, sid))
                    return None
                    if not None:
                        pass
                    continue
                    continue
                except Exception:
                    return None


    def close(self):
        self.stop.set()
        with self.lock:
            for s in list(self.streams.values()):
                s.close()
            self.streams.clear()
            None(None, None)
            if self.sock:
                
                try:
                    self.sock.close()
                    self.sock = None
                    return None
                    return None
                    except Exception:
                        continue
                    if not None:
                        pass
                    continue
                except Exception:
                    continue


class GuestProxy:
    __doc__ = '客人启动器：本地监听 127.0.0.1:port，把 MC 流量送入虚拟网'
    
    def __init__(self, local_port, relay_addr, room_id, token, direct_addr, log, on_status):
        self.local_port = local_port
        self.relay_addr = relay_addr
        self.room_id = room_id
        self.token = token
        self.direct_addr = direct_addr
        self.log = log
        self.on_status = on_status
        self.stop = Stopper()
        self.server = None
        self.clients = 0

    
    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server.bind(('127.0.0.1', self.local_port))
            self.server.listen(8)
            threading.Thread(self._accept_loop, True).start()
            if self.log:
                pass
            self.log('本地联机端口已就绪：127.0.0.1:%d' % self.local_port)
            return self
        except OSError:
            e = None
            raise RuntimeError('本地端口 %d 被占用，请在设置中更换本地联机端口' % self.local_port)
            e = None
            del e


    def _say(self, msg):
        if self.log:
            self.log(msg)
        return None

    
    def _accept_loop(self):
        if not self.stop.stopped:
            
            try:
                (conn, _) = self.server.accept()
                if self.on_status:
                    pass
                self.on_status(True, '已连接 %d 个游戏' % self.clients)
                threading.Thread(self._handle, (conn,), True).start()
                if not self.stop.stopped:
                    continue
                return None
                return None
            except Exception:
                return None


    def _handle(self, conn):
        remote = None
        
        try:
            if self.direct_addr:
                
                try:
                    remote = socket.create_connection(self.direct_addr, 3)
                    self._say('直连 %s:%d 成功' % self.direct_addr)
                    
                    try:
                        if remote is None:
                            remote = socket.create_connection(self.relay_addr, 15)
                            remote.sendall(f'''JOIN  \n'''.encode())
                        self._say('已通过主机中继接入房间')
                        _pump(conn, remote, self.stop)
                        if self.on_status:
                            self.on_status(True, '已连接 %d 个游戏' % max(0, self.clients))
                        return None
                        return None
                        except Exception:
                            None = None
                            
                            try:
                                continue
                                
                                try:
                                    pass
                                except Exception:
                                    e = None
                                    self._say('联机通道异常：%s' % e)
                                    
                                    try:
                                        e = None
                                        del e
                                        continue
                                        e = None
                                        del e
                                        
                                        try:
                                            pass
                                        except:
                                            if self.on_status:
                                                self.on_status(True, '已连接 %d 个游戏' % max(0, self.clients))


    def close(self):
        self.stop.set()
        
        try:
            self.server.close()
            
            try:
                socket.create_connection(('127.0.0.1', self.local_port), 0.3).close()
                return None
                continue
            except Exception:
                return None


class LANScanner:
    __doc__ = '监听 Minecraft 局域网组播，自动发现开放到局域网的世界'
    
    def __init__(self, callback, log):
        self.callback = callback
        self.log = log
        self.stop = Stopper()

    
    def start(self):
        threading.Thread(self._run, True).start()
        return self

    
    def _run(self):
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', LAN_MULTICAST_PORT))
            mreq = socket.inet_aton(LAN_MULTICAST_GROUP) + socket.inet_aton('0.0.0.0')
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            sock.settimeout(0.5)
            if not self.stop.stopped:
                
                try:
                    (data, addr) = sock.recvfrom(2048)
                    text = data.decode('utf-8', 'ignore')
                    if '[AD]' not in text:
                        continue
                    port = ''
                    motd = ''
                    if '[AD]' in text and '[/AD]' in text:
                        pass
                    port = text.split('[AD]')[1].split('[/AD]')[0]
                    if '[MOTD]' in text and '[/MOTD]' in text:
                        pass
                    motd = text.split('[MOTD]')[1].split('[/MOTD]')[0]
                    
                    try:
                        self.callback({
                            'ip': addr[0],
                            'port': int(port),
                            'motd': motd,
                            'time': time.time() })
                        if not self.stop.stopped:
                            continue
                        
                        try:
                            sock.close()
                            return None
                            except Exception:
                                e = None
                                if self.log:
                                    pass
                                self.log('局域网发现启动失败：%s' % e)
                                e = None
                                del e
                                return None
                                e = None
                                del e
                            except socket.timeout:
                                continue
                            except Exception:
                                continue
                            continue
                        except Exception:
                            return None

