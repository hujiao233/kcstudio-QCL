# kcstudio-QCL

QCL（KcStudio QCL）—— 一个基于 **Python 3.13 + PySide6 (Qt6)** 的 Minecraft 启动器。

本仓库中的源码是**从发行版 `QCL-Setup-2.0.0.exe` 中提取并还原**得到的，并非原作者直接提交的版本。
还原方法与已知缺陷见 [还原说明](#还原说明)。

---

## 1. 软件本体在哪儿

`QCL-Setup-2.0.0.exe`（44,482,072 字节）虽然名字叫 "Setup"，但它**不是**安装程序，而是一个**双层 PyInstaller 打包**的自解压启动器：

```
QCL-Setup-2.0.0.exe                     ← PyInstaller onefile (Python 3.13, 入口 setup_gui.py)
├── setup_gui.py                        ← 外壳：Tkinter 写的解压/安装界面（属于"安装包"，已剔除）
├── payload.zip                 33 MB   ← 真正的软件本体
│   ├── QCL.exe                         ← PyInstaller onedir 引导器 (Python 3.13, 入口 qcl_entry.py)
│   ├── _internal/                      ← Python 运行时 + PySide6/Qt6 + requests 等依赖
│   │   └── tools/remove.cmd
│   └── remove.cmd
└── (tcl/tk、OpenSSL 等外壳依赖)
```

**软件本体 = `payload.zip` 里的 `QCL.exe`**，其 Python 代码分为：

| 内容 | 说明 |
| --- | --- |
| `qcl_entry.py` | 启动入口 |
| `qcl/` | 应用包（42 个模块） |
| `qcl/core/` | 业务逻辑：账号认证、版本/加载器、Modrinth/CurseForge、下载、Java 探测、启动、实例、设置、更新、AI 助手、联机中继、本地 HTTP 服务等 |
| `qcl/ui/` | PySide6 界面：`app` / `main_window` / `dialogs` / `widgets` / `theme` / `pages/*` |

## 2. 目录结构

```
.
├── qcl_entry.py          启动入口
├── qcl/
│   ├── __init__.py
│   ├── main.py           CLI 入口与启动流程
│   ├── core/             业务核心（不依赖 Qt，服务端可用）
│   └── ui/               PySide6 界面层
├── requirements.txt
└── tools/                本次"提取—还原"所使用的脚本
```

## 3. 运行

```bash
pip install -r requirements.txt
python qcl_entry.py
```

## 4. 依赖

- Python **3.13**
- PySide6 (Qt6: Core / Gui / Widgets / Network / Svg)
- requests、urllib3、certifi、charset-normalizer、idna

---

## 还原说明

### 提取流程

1. **识别外壳**：读取 PE 头，`.reloc` 节结束于 `0x4D200`，其后 44 MB 是 PyInstaller 的 CArchive（尾部 cookie `MEI\014\013\012\013\016`，`pyvers=0x0DF3` → Python 3.13）。
2. **解包外壳**：使用 `pyinstxtractor-ng` 解出 `setup_gui.pyc` 与 `payload.zip`。
3. **取出本体**：解压 `payload.zip` 得到 `QCL.exe` + `_internal/`。
4. **解包本体**：`QCL.exe` 同样是 PyInstaller（onedir），其 PYZ 中含有 498 个模块，其中 `qcl.*` 共 42 个即为应用源码（其余为 CPython 标准库与第三方依赖）。
5. **反编译**：使用 [Decompyle++ (pycdc)](https://github.com/zrax/pycdc)，并针对 Python 3.13 打了补丁（见下）。
6. **后处理**：修复相对导入、清理 3.13 编译器产物。

复现脚本见 `tools/`。

### 针对 Python 3.13 对 pycdc 做的修复

上游 pycdc 对 3.13 支持不全（几乎所有模块都只能反编译出前几行）。本次修复：

- **调用约定**：3.13 把 `PUSH_NULL` 移到被调函数**之上**（栈布局由 `NULL, callable, args…` 变为 `callable, NULL, args…`）。修复 `CALL` / `CALL_FUNCTION_EX` / 类创建 / `LOAD_ATTR` / `LOAD_GLOBAL` 的出入栈顺序。
- `MAKE_FUNCTION`（3.13 起无操作数）与新增的 `SET_FUNCTION_ATTRIBUTE`。
- 新增/补齐：`TO_BOOL`、`CALL_KW`、`UNPACK_EX`、`MAP_ADD`、`DICT_MERGE`、`DICT_UPDATE`、`FORMAT_SIMPLE/WITH_SPEC`、`LOAD_FAST_CHECK`、`STORE_FAST_LOAD_FAST`、`STORE_FAST_STORE_FAST`、`YIELD_VALUE`、intrinsics 等。
- `with` 语句：3.11+ 取消了 `SETUP_WITH`，改为依据异常表（`push_lasti` 表项）确定代码块范围。
- PEP 709 内联推导式的识别。

### 已知缺陷（重要）

反编译器对 **CPython 3.11 起的"零成本异常"机制**支持不完整（该问题在 3.12 上同样存在，非本次引入），因此还原结果中以下结构**不可直接运行**，需要人工校正：

- `try / except` 块的缩进与分支可能错乱（会出现"缺 except"或 `except` 缩进错误）；
- 列表/字典/集合推导式、生成器表达式可能输出为 `(lambda .0: …)` 或残缺片段；
- `with` 块体可能缺失；
- 少量残留 `None(...)`、`# import`（模块名丢失）、`__firstlineno__` 等噪声。

`tools/check_syntax.py` 可用于统计仍然无法被 Python 3.13 解析的文件。建议把本仓库内容视为**可读的参考实现**，而不是可直接运行的副本。

### 未纳入本仓库的部分

- 外壳 `setup_gui.py`（Tkinter 安装界面）与 PyInstaller 运行时 —— 属于"安装包"，按要求已剔除。
- `_internal/` 中的 Python 解释器、Qt6/Qt DLL、OpenSSL 等二进制依赖。
