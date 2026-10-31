# Source Generated with Decompyle++
# File: community.pyc (Python 3.13)

'''社区页：启动器论坛 + 实时聊天

数据放在主机服务端（server.py 的 /api/forum/*、/api/chat/*），
所有人连同一个主机地址就是同一个社区：自己开主机就是自己当服主。
'''
import html
import time
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QPlainTextEdit, QPushButton, QTabWidget, QTextBrowser, QVBoxLayout, QWidget
from ..pages import Page
from .. import theme
from ..widgets import hbox, make_card, vbox
from ...core import account
from ...core.qtdownload import run_async

def _fmt_time(ts):
    
    try:
        return time.strftime('%m-%d %H:%M', time.localtime(int(ts)))
    except Exception:
        return ''


class NewPostDialog(QDialog):
    
    def __init__(self, parent):
        super.__init__(parent)
        self.setWindowTitle('发布新帖')
        self.resize(520, 400)
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel('标题'))
        self.title_edit = QLineEdit()
        self.title_edit.setMaxLength(60)
        self.title_edit.setPlaceholderText('一句话说清你要问/分享什么')
        lay.addWidget(self.title_edit)
        lay.addWidget(QLabel('内容'))
        self.body_edit = QPlainTextEdit()
        self.body_edit.setPlaceholderText('详细描述，比如报错信息、整合包版本、你试过什么…')
        lay.addWidget(self.body_edit, 1)
        box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.button(QDialogButtonBox.Ok).setText('发布')
        box.button(QDialogButtonBox.Cancel).setText('取消')
        box.accepted.connect(self._ok)
        box.rejected.connect(self.reject)
        lay.addWidget(box)

    
    def _ok(self):
        if not self.title_edit.text().strip():
            self.title_edit.setFocus()
        return None
        if not self.body_edit.toPlainText().strip():
            self.body_edit.setFocus()
        return None
        self.accept()

    
    def payload(self):
        return {
            'title': self.title_edit.text().strip(),
            'body': self.body_edit.toPlainText().strip() }




class CommunityPage(Page):
    title = '社区'
    
    def __init__(self, ctx, parent):
        super.__init__(ctx, parent)
        self.posts = []
        self.current_post = None
        self.chat_last_id = 0
        self._busy = False
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 16, 20, 14)
        lay.setSpacing(10)
        head = hbox(8)
        t = QLabel('社区')
        t.setStyleSheet('font-size: 18px; font-weight: 700;')
        head.addWidget(t)
        self.host_label = QLabel('')
        self.host_label.setProperty('sub', True)
        head.addWidget(self.host_label)
        head.addStretch(1)
        self.state_label = QLabel('')
        self.state_label.setProperty('sub', True)
        head.addWidget(self.state_label)
        b_refresh = QPushButton('刷新')
        b_refresh.setFixedWidth(80)
        b_refresh.clicked.connect((lambda : self._reload()))
        head.addWidget(b_refresh)
        lay.addLayout(head)
        self.tabs = QTabWidget()
        self.tabs.addTab(self._forum_tab(), '论坛')
        self.tabs.addTab(self._chat_tab(), '聊天室')
        self.tabs.currentChanged.connect((lambda _i: self._reload()))
        lay.addWidget(self.tabs, 1)
        self.poll = QTimer(self)
        self.poll.setInterval(3000)
        self.poll.timeout.connect(self._poll_chat)
        self._refresh_head()

    
    def _forum_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 8, 0, 0)
        lay.setSpacing(8)
        row = hbox(8)
        b_new = QPushButton('发布新帖')
        b_new.setProperty('primary', True)
        b_new.setFixedWidth(110)
        b_new.clicked.connect(self._new_post)
        row.addWidget(b_new)
        self.post_tip = QLabel('')
        self.post_tip.setProperty('sub', True)
        row.addWidget(self.post_tip)
        row.addStretch(1)
        lay.addLayout(row)
        body = hbox(10)
        self.post_list = QListWidget()
        self.post_list.setFixedWidth(320)
        self.post_list.currentRowChanged.connect(self._select_post)
        body.addWidget(self.post_list)
        right = make_card()
        rl = vbox(12, 8, right)
        self.post_view = QTextBrowser()
        self.post_view.setOpenExternalLinks(True)
        rl.addWidget(self.post_view, 1)
        rrow = hbox(8)
        self.reply_edit = QLineEdit()
        self.reply_edit.setPlaceholderText('回复这个帖子…')
        self.reply_edit.returnPressed.connect(self._send_reply)
        rrow.addWidget(self.reply_edit, 1)
        b_reply = QPushButton('发送回复')
        b_reply.setFixedWidth(96)
        b_reply.clicked.connect(self._send_reply)
        rrow.addWidget(b_reply)
        rl.addLayout(rrow)
        body.addWidget(right, 1)
        lay.addLayout(body, 1)
        return w

    
    def _chat_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 8, 0, 0)
        lay.setSpacing(8)
        self.chat_view = QTextBrowser()
        lay.addWidget(self.chat_view, 1)
        self.chat_state = QLabel('')
        self.chat_state.setProperty('sub', True)
        lay.addWidget(self.chat_state)
        row = hbox(8)
        self.chat_edit = QLineEdit()
        self.chat_edit.setPlaceholderText('说点什么…（回车发送）')
        self.chat_edit.returnPressed.connect(self._send_chat)
        row.addWidget(self.chat_edit, 1)
        b_send = QPushButton('发送')
        b_send.setFixedWidth(88)
        b_send.setProperty('primary', True)
        b_send.clicked.connect(self._send_chat)
        row.addWidget(b_send)
        lay.addLayout(row)
        return w

    
    def _refresh_head(self):
        if not self.ctx.settings.host_url:
            self.ctx.settings.host_url
        self.host_label.setText('主机：%s' % '未设置')
        if account.token():
            self.state_label.setText('已登录：%s' % account.username())
        return None
        self.state_label.setText('未登录 —— 到「联机」页注册/登录后即可发帖聊天')

    
    def _need_login(self):
        if account.token():
            pass
        return True
        self.ctx.toast('请先到「联机」页注册或登录账号', 'warn')
        return False

    
    def on_show(self):
        self._refresh_head()
        self._reload()
        if self.tabs.currentIndex() == 1:
            self.poll.start()
        return None

    
    def on_hide(self):
        self.poll.stop()

    
    def _reload(self):
        self._refresh_head()
        if not account.token():
            self.post_list.clear()
            self.post_tip.setText('登录后可查看论坛')
        return None
        if self.tabs.currentIndex() == 0:
            self._load_posts()
        return None
        self._poll_chat(True)

    
    def _load_posts(self):
        tok = account.token()
        
        def work():
            return self.ctx.api.forum_posts(tok)

        self.post_tip.setText('加载中…')
        run_async(work, self._on_posts, (lambda e: self.post_tip.setText('加载失败：%s' % e)))

    
    def _on_posts(self, data):
        if not data:
            data
        if not { }.get('posts'):
            { }.get('posts')
        self.posts = []
        self.post_tip.setText('%d 个帖子' % len(self.posts))
        keep = self.post_list.currentRow()
        self.post_list.clear()
        for p in self.posts:
            if not p.get('title'):
                p.get('title')
            if not p.get('author'):
                p.get('author')
            if not p.get('replies'):
                p.get('replies')
            it = QListWidgetItem('%s\n%s · %s · %d 回复' % ('(无标题)', '?', _fmt_time(p.get('ts')), len([])))
            self.post_list.addItem(it)
        if self.posts:
            self.post_list.setCurrentRow(min(max(keep, 0), len(self.posts) - 1))
        return None
        self.post_view.setHtml("<div style='color:%s'>还没有帖子，点「发布新帖」开个头。</div>" % theme.SUBTEXT)

    
    def _select_post(self, row):
        if row < 0 or row >= len(self.posts):
            self.current_post = None
        return None
        p = self.posts[row]
        self.current_post = p
        html = [
            "<div style='font-size:15px;font-weight:700'>%s</div>" % _esc(p.get('title')),
            f'''<div style=\'color:;font-size:11px;margin:4px 0 10px\'> · </div>''',
            "<div style='line-height:160%%'>%s</div>" % _esc(p.get('body')).replace('\n', '<br/>')]
        if not p.get('replies'):
            p.get('replies')
        replies = []
        if replies:
            html.append("<hr style='border:none;border-top:1px solid %s;margin:12px 0'/>" % theme.CARD2)
            for r in replies:
                html.append(f'''<div style=\'margin-bottom:8px\'><span style=\'color:;font-size:11px\'> · </span><div></div></div>''')
        self.post_view.setHtml(''.join(html))

    
    def _new_post(self):
        if not self._need_login():
            pass
        return None
        dlg = NewPostDialog(self)
        if not dlg.exec():
            pass
        return None
        payload = dlg.payload()
        tok = account.token()
        
        def work():
            return self.ctx.api.forum_post(tok, payload['title'], payload['body'])

        run_async(work, (lambda r: (self.ctx.toast('已发布', 'ok'), self._load_posts())), (lambda e: self.ctx.toast('发布失败：%s' % e, 'err')))

    
    def _send_reply(self):
        if not self._need_login():
            pass
        return None
        if not self.current_post:
            self.ctx.toast('先选一个帖子', 'warn')
        return None
        text = self.reply_edit.text().strip()
        if not text:
            pass
        return None
        tok = account.token()
        if not self.current_post.get('id'):
            self.current_post.get('id')
        pid = int(0)
        self.reply_edit.clear()
        
        def work():
            return self.ctx.api.forum_reply(tok, pid, text)

        run_async(work, (lambda r: self._load_posts()), (lambda e: self.ctx.toast('回复失败：%s' % e, 'err')))

    
    def _send_chat(self):
        if not self._need_login():
            pass
        return None
        text = self.chat_edit.text().strip()
        if not text:
            pass
        return None
        tok = account.token()
        self.chat_edit.clear()
        
        def work():
            return self.ctx.api.chat_send(tok, text)

        run_async(work, (lambda r: self._poll_chat()), (lambda e: self.ctx.toast('发送失败：%s' % e, 'err')))

    
    def _poll_chat(self, reset):
        if not account.token():
            pass
        return None
        if self._busy:
            pass
        return None
        if reset:
            self.chat_last_id = 0
        self.chat_view.clear()
        self._busy = True
        tok = account.token()
        since = self.chat_last_id
        
        def work():
            return self.ctx.api.chat_messages(tok, since)

        
        def done(data):
            self._busy = False
            self.chat_state.setText('')
            if not data:
                data
            if not { }.get('messages'):
                { }.get('messages')
            self._append_chat([])

        
        def fail(e):
            self._busy = False
            self.chat_state.setText('连接失败：%s（主机可能没开，到「设置」点保存并应用可启动主机）' % e)

        run_async(work, done, fail)

    
    def _append_chat(self, msgs):
        if not msgs:
            pass
        return None
        parts = []
        for m in msgs:
            if not m.get('id'):
                m.get('id')
            self.chat_last_id = max(self.chat_last_id, int(0))
            parts.append(f'''<div style=\'margin-bottom:6px\'><span style=\'color:;font-size:11px\'> · </span><br/><span></span></div>''')
        bar = self.chat_view.verticalScrollBar()
        at_bottom = bar.value() >= bar.maximum() - 20
        self.chat_view.append(''.join(parts))
        if at_bottom:
            bar.setValue(bar.maximum())
        return None
        return None
        except Exception:
            continue




def _esc(s):
    if not s:
        s
    return html.escape(str(''))

