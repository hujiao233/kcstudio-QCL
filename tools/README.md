# 提取 / 还原工具

本目录下的脚本用于从 `QCL-Setup-2.0.0.exe` 还原出仓库根目录的 `qcl/` 源码。

## 依赖

```bash
pip install pyinstxtractor-ng xdis
```

反编译器使用 [pycdc](https://github.com/zrax/pycdc)，**必须应用 `pycdc_python313.patch`**（Python 3.13 支持补丁）后才能正确反编译：

```bash
git clone https://github.com/zrax/pycdc
cd pycdc && git apply /path/to/pycdc_python313.patch
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build          # 产出 build/pycdc
```

## 步骤

```bash
# 1~2. 解包外层 PyInstaller（setup_gui），得到 payload.zip
python -m pyinstxtractor_ng QCL-Setup-2.0.0.exe
# 输出目录：QCL-Setup-2.0.0.exe_extracted/

# 3. 取出软件本体
python extract.py --exe QCL-Setup-2.0.0.exe --out work/
#   work/payload/QCL.exe + work/payload/_internal/

# 4. 解包本体，提取 qcl 包的 .pyc
python extract.py --app work/payload/QCL.exe --pyc-out work/pyc/

# 5. 反编译
python decompile.py --pyc work/pyc --pycdc /path/to/pycdc --out ..

# 6. 后处理（相对导入修复、噪声清理）
python postprocess.py --root ..

# 7. 语法体检
python check_syntax.py --root .. --python313 /path/to/python3.13
```

## pycdc 补丁内容

`pycdc_python313.patch` 修正了以下 3.13 相关问题：

1. **调用约定变更**：3.13 中 `PUSH_NULL` 位于被调函数之上（栈由 `NULL, callable, args…` 变为 `callable, NULL, args…`），影响 `CALL` / `CALL_FUNCTION_EX` / 类创建 / `LOAD_ATTR` / `LOAD_GLOBAL`。
2. `MAKE_FUNCTION` 在 3.13 起不再带操作数，默认值/注解改由 `SET_FUNCTION_ATTRIBUTE` 附加。
3. 补齐 `TO_BOOL`、`CALL_KW`、`UNPACK_EX`、`MAP_ADD`、`SET_ADD`、`DICT_MERGE/UPDATE`、`FORMAT_SIMPLE/WITH_SPEC`、`LOAD_FAST_CHECK`、`STORE_FAST_LOAD_FAST/STORE_FAST_STORE_FAST/MAYBE_NULL`、`YIELD_VALUE`、intrinsics 等缺失分支。
4. `with` 语句：3.11+ 依据异常表 `push_lasti` 表项确定块范围。
5. PEP 709 内联推导式的识别。

> 注意：即便打了补丁，pycdc 对 3.11+ 的零成本异常机制支持仍不完整，
> `try/except` 与推导式的还原结果仍需人工校正。
