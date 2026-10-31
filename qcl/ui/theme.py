# Source Generated with Decompyle++
# File: theme.pyc (Python 3.13)

'''QCL 蓝白浅色主题'''
from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
BG = '#eef3f9'
PANEL = '#ffffff'
CARD = '#ffffff'
CARD2 = '#e8eef6'
BORDER = '#d3dee9'
TEXT = '#1f2937'
SUBTEXT = '#6b7a90'
ACCENT = '#2f6bff'
ACCENT_HOVER = '#5588ff'
ACCENT_DARK = '#2457d6'
DANGER = '#e5484d'
WARN = '#f08c00'
INFO = '#2f6bff'
QSS = '\nQWidget { background: %(bg)s; color: %(text)s; font-family: "Microsoft YaHei UI", "Segoe UI", sans-serif; font-size: 13px; }\nQMainWindow, QDialog { background: %(bg)s; }\nQToolTip { background: %(card2)s; color: %(text)s; border: 1px solid %(border)s; padding: 4px 8px; }\n\nQFrame#card { background: %(card)s; border: 1px solid %(border)s; border-radius: 10px; }\nQFrame#card2 { background: %(card2)s; border: 1px solid %(border)s; border-radius: 10px; }\nQFrame#panel { background: %(panel)s; border-radius: 12px; }\nQFrame#sep { background: %(border)s; max-height: 1px; min-height: 1px; }\n\nQPushButton {\n    background: %(card2)s; color: %(text)s; border: 1px solid %(border)s;\n    border-radius: 8px; padding: 7px 14px; font-weight: 500;\n}\nQPushButton:hover { background: %(accentdark)s; border-color: %(accent)s; color: #ffffff; }\nQPushButton:pressed { background: %(accent)s; }\nQPushButton:disabled { background: %(card2)s; color: %(subtext)s; border-color: %(border)s; }\nQPushButton[primary="true"] {\n    background: %(accent)s; color: #ffffff; border: none; font-weight: 700;\n}\nQPushButton[primary="true"]:hover { background: %(accent_hover)s; color: #ffffff; }\nQPushButton[primary="true"]:disabled { background: %(card2)s; color: %(subtext)s; }\nQPushButton[danger="true"] { color: %(danger)s; border-color: %(danger)s; }\nQPushButton[danger="true"]:hover { background: %(danger)s; color: #fff; }\nQPushButton[flat="true"] { background: transparent; border: none; padding: 6px; }\nQPushButton[flat="true"]:hover { background: %(card2)s; border: none; color: %(text)s; }\nQPushButton[chip="true"] {\n    background: %(panel)s; color: %(subtext)s; border: 1px solid %(border)s;\n    border-radius: 12px; padding: 4px 12px; font-size: 12px; font-weight: 400;\n}\nQPushButton[chip="true"]:hover { background: %(card2)s; color: %(text)s; border-color: %(accent)s; }\nQPushButton:checked { background: %(accentdark)s; color: #ffffff; border-color: %(accent)s; }\n\nQLineEdit, QTextEdit, QPlainTextEdit {\n    background: %(card2)s; border: 1px solid %(border)s; border-radius: 8px;\n    padding: 7px 10px; selection-background-color: %(accent)s;\n}\nQLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus { border-color: %(accent)s; }\n\nQComboBox {\n    background: %(card2)s; border: 1px solid %(border)s; border-radius: 8px;\n    padding: 6px 10px; min-height: 20px;\n}\nQComboBox:focus { border-color: %(accent)s; }\nQComboBox QAbstractItemView {\n    background: %(card)s; border: 1px solid %(border)s; selection-background-color: %(accent)s;\n    selection-color: #ffffff; outline: 0px;\n}\nQComboBox::drop-down { border: none; width: 18px; }\nQComboBox::down-arrow { image: none; border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid %(subtext)s; margin-right: 6px; }\n\nQListWidget, QTreeWidget { background: %(panel)s; border: 1px solid %(border)s; border-radius: 10px; outline: 0px; padding: 4px; }\nQListWidget::item, QTreeWidget::item { padding: 8px 10px; border-radius: 8px; }\nQListWidget::item:selected, QTreeWidget::item:selected { background: %(accentdark)s; color: #ffffff; }\nQListWidget::item:hover, QTreeWidget::item:hover { background: %(card2)s; }\n\nQTabWidget::pane { border: 1px solid %(border)s; border-radius: 10px; background: %(panel)s; top: -1px; }\nQTabBar::tab { background: transparent; color: %(subtext)s; padding: 8px 16px; border-radius: 8px; margin-right: 4px; }\nQTabBar::tab:selected { background: %(card2)s; color: %(text)s; }\nQTabBar::tab:hover { color: %(text)s; }\n\nQProgressBar { background: %(card2)s; border: none; border-radius: 5px; height: 10px; text-align: center; color: %(text)s; }\nQProgressBar::chunk { background: %(accent)s; border-radius: 5px; }\n\nQScrollArea { background: transparent; border: none; }\nQScrollBar:vertical { background: transparent; width: 10px; margin: 0; }\nQScrollBar::handle:vertical { background: %(border)s; border-radius: 5px; min-height: 30px; }\nQScrollBar::handle:vertical:hover { background: %(subtext)s; }\nQScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }\nQScrollBar:horizontal { background: transparent; height: 10px; }\nQScrollBar::handle:horizontal { background: %(border)s; border-radius: 5px; min-width: 30px; }\nQScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }\n\nQCheckBox::indicator { width: 16px; height: 16px; border-radius: 4px; border: 1px solid %(border)s; background: %(card2)s; }\nQCheckBox::indicator:checked { background: %(accent)s; border-color: %(accent)s; }\nQSpinBox { background: %(card2)s; border: 1px solid %(border)s; border-radius: 8px; padding: 5px 8px; }\n\nQMenu { background: %(card)s; border: 1px solid %(border)s; border-radius: 8px; padding: 4px; }\nQMenu::item { padding: 8px 20px; border-radius: 6px; }\nQMenu::item:selected { background: %(accentdark)s; color: #ffffff; }\n\nQLabel, QCheckBox, QRadioButton { background: transparent; }\nQLabel[title="true"] { font-size: 20px; font-weight: 700; }\nQLabel[sub="true"] { color: %(subtext)s; }\nQLabel[accent="true"] { color: %(accent)s; }\nQLabel[mono="true"] { font-family: Consolas, "Courier New", monospace; }\n' % {
    'bg': BG,
    'panel': PANEL,
    'card': CARD,
    'card2': CARD2,
    'border': BORDER,
    'text': TEXT,
    'subtext': SUBTEXT,
    'accent': ACCENT,
    'accent_hover': ACCENT_HOVER,
    'accentdark': ACCENT_DARK,
    'danger': DANGER,
    'warn': WARN,
    'info': INFO }

def apply(app):
    app.setStyle('Fusion')
    pal = QPalette()
    pal.setColor(QPalette.Window, QColor(BG))
    pal.setColor(QPalette.WindowText, QColor(TEXT))
    pal.setColor(QPalette.Base, QColor(CARD2))
    pal.setColor(QPalette.AlternateBase, QColor(CARD))
    pal.setColor(QPalette.ToolTipBase, QColor(CARD2))
    pal.setColor(QPalette.ToolTipText, QColor(TEXT))
    pal.setColor(QPalette.Text, QColor(TEXT))
    pal.setColor(QPalette.Button, QColor(CARD2))
    pal.setColor(QPalette.ButtonText, QColor(TEXT))
    pal.setColor(QPalette.Highlight, QColor(ACCENT))
    pal.setColor(QPalette.HighlightedText, QColor('#ffffff'))
    pal.setColor(QPalette.Link, QColor(ACCENT))
    app.setPalette(pal)
    app.setStyleSheet(QSS)
    app.setFont(QFont('Microsoft YaHei UI', 9))

