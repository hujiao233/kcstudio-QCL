# Source Generated with Decompyle++
# File: __init__.pyc (Python 3.13)

'''页面基类'''
from PySide6.QtWidgets import QWidget
from ..widgets import vbox, hbox

class Page(QWidget):
    title = ''
    
    def __init__(self, ctx, parent):
        super.__init__(parent)
        self.ctx = ctx
        self._listeners = []

    
    def listen(self, name, fn):
        '''订阅事件并登记，页面隐藏时由基类自动反注册。

以前各页面在 __init__ 里直接 ctx.on(...)，订阅会永远挂在总线上：
页面切走后旧页面仍被回调（打到不可见控件上），反复进出也不会清理。
现在统一走这里：显示时绑定、隐藏时解绑，每次进出都是干净的一份。
'''
        self.ctx.on(name, fn)
        self._listeners.append((name, fn))
        return fn

    
    def bind_events(self):
        '''子类在这里用 self.listen(...) 订阅事件。

注意：不要写在 __init__ 里。__init__ 只在创建时执行一次，
而订阅应该在"每次显示"时重建，这样隐藏期间才不会继续收到回调。
'''
        pass

    
    def on_show(self):
        pass

    
    def on_hide(self):
        pass

    
    def is_current_page(self):
        '''本页是否是主窗口当前显示的那一页。

比 isVisible() 可靠：窗口被最小化、或另一个顶层窗口挡住时，
isVisible() 会给 False，但页面其实还是"当前页"，
迟到的异步回调不该因为这种临时状态就把结果丢掉。
'''
        
        try:
            mw = getattr(self.ctx, 'main_window', None)
            stack = getattr(mw, 'stack', None)
            if stack is None:
                pass
            return self.isVisible()
            
            try:
                return stack.currentWidget() is self
            except Exception:
                return True


    def _drop_listeners(self):
        for name, fn in self._listeners:
            self.ctx.off(name, fn)
        self._listeners = []
        return None
        except Exception:
            continue

    
    def showEvent(self, e):
        super.showEvent(e)
        self._drop_listeners()
        
        try:
            self.bind_events()
            return None
        except Exception:
            return None


    def hideEvent(self, e):
        self._drop_listeners()
        
        try:
            self.on_hide()
            super.hideEvent(e)
            return None
        except Exception:
            continue




