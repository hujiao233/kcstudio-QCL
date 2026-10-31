# 字节码基线

这里是 `qcl.*` 模块的 **CPython 3.13 字节码**，是从发行包里提取出来的**真实程序**。

## 为什么需要它

原始安装包 `QCL-Setup-2.0.0.exe`（44 MB）已在一次误删中永久丢失，
`Desktop\Dev_\` 部署目录之后也被清理。这两份字节码现在是**孤本**：
仓库里的 `qcl/` 源码是从它反编译来的，而反编译产物无法运行，
所以这里才是唯一可运行的、与原始发行版一致的东西。

## 两份构建的关系

| 目录 | 来源 | 说明 |
| --- | --- | --- |
| `dev/` | `Desktop\Dev_\QCL.exe`（onedir 部署） | **与仓库 `qcl/` 源码同源** —— 5 个差异模块的字符串命中率全部指向它 |
| `zip/` | `Downloads\QCL.zip` 里的 `QCL.exe` | 较新版本，5 个模块代码不同 |

两份各 42 个模块，其中 5 个模块代码不同（命中率比对：dev 均高于 zip）：

| 模块 | dev | zip |
| --- | --- | --- |
| `core/paths` | 0.836 | 0.821 |
| `core/server` | 0.872 | 0.772 |
| `ui/pages/community` | 0.658 | 0.608 |
| `ui/pages/multiplayer` | 0.793 | 0.701 |
| `ui/pages/settings_page` | 0.841 | 0.762 |

`zip` 版多出的特性（可作为将来同步新版的依据）：

- `core/server`：`DualStackHTTPServer`（双栈 IPv4/IPv6）、`/assets/`、`/screens/`、内嵌 HTML 页面
- `ui/pages/multiplayer` / `community`：IPv6 地址解析与相关提示文案

> 注意 `Downloads\QCL.zip` 里的 `QCL.exe` **不能独立运行**：它是 PyInstaller
> onedir 的引导器，CArchive 只有 14 个条目，不含 PySide6 / Qt / Python DLL，
> 必须配 `_internal/` 才行。

## 使用方法

反汇编某个函数，用它来判断反编译结果里含糊的地方：

```bat
python tools\bytecode_dis.py dev qcl.core.paths _desktop
```

重新提取（拿到新的发行包时）：

```bat
python tools\extract_pyz.py <QCL.exe 或含它的 zip> <输出目录>
```

## 说明

- 文件按模块路径组织：`dev/qcl/core/net.pyc`
- 文件头 16 字节是提取时补的（4 字节魔数 + 12 字节占位），读取时用
  `marshal.loads(open(p,'rb').read()[16:])`
- PyInstaller 的 PYZ 里有 5 个 `length == 0` 的别名条目（同一代码对象登记
  多个模块名），没有自己的数据，提取时跳过
