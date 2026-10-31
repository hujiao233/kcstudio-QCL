# Source Generated with Decompyle++
# File: constants.pyc (Python 3.13)

'''QCL 全局常量定义'''
APP_NAME = 'QCL'
APP_DISPLAY = 'QCL 启动器'
APP_ID = 'QCL'
APP_VERSION = '1.0.0'
APP_CHANNEL = 'stable'
APP_AUTHOR = 'QCL'
MOJANG_MANIFEST = 'https://piston-meta.mojang.com/mc/game/version_manifest_v2.json'
MC_LIBRARIES = 'https://libraries.minecraft.net/'
MC_RESOURCES = 'https://resources.download.minecraft.net/'
MC_LAUNCHER_META = 'https://launchermeta.mojang.com/'
MC_LAUNCHER = 'https://launcher.mojang.com/'
FABRIC_META = 'https://meta.fabricmc.net/v2'
FABRIC_MAVEN = 'https://maven.fabricmc.net/'
FORGE_PROMOTIONS = 'https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json'
FORGE_MAVEN = 'https://maven.minecraftforge.net/net/minecraftforge/forge'
NEOFORGE_MAVEN = 'https://maven.neoforged.net/releases/net/neoforged/neoforge'
QUILT_META = 'https://meta.quiltmc.org/v3'
OPTIFINE = 'https://optifine.net/'
MODRINTH_API = 'https://api.modrinth.com/v2'
MODRINTH_CDN = 'https://cdn.modrinth.com'
CURSEFORGE_API = 'https://api.curseforge.com/v1'
ADOPTIUM_API = 'https://api.adoptium.net/v3'
BMCLAPI = 'https://bmclapi2.bangbang93.com'
MCIM = 'https://download.mcimirror.top'

class Mirror:
    __doc__ = '镜像源：把官方地址重写为镜像地址，失败时自动回落官方'
    
    def __init__(self, name, rewrite, enabled):
        self.name = name
        self.rewrite = rewrite
        self.enabled = enabled
        self.failures = 0

    
    def map(self, url):
        if not self.enabled:
            pass
        return url
        for src, dst in self.rewrite.items():
            if not url.startswith(src):
                continue
            
            return self.rewrite.items(), dst + url[len(src):]
        return url


MIRRORS = [
    Mirror('官方源', { }),
    Mirror('BMCLAPI（国内加速）', { }),
    Mirror('我的世界中文镜像', {
        'https://libraries.minecraft.net': MCIM + '/maven',
        MC_LIBRARIES: MCIM + '/maven/',
        MC_RESOURCES: MCIM + '/assets/',
        MOJANG_MANIFEST: MCIM + '/mc/game/version_manifest_v2.json' })]
CONTENT_TYPES = {
    'mod': ('mod', 6, 'mods'),
    'shader': ('shader', 6552, 'shaderpacks'),
    'resourcepack': ('resourcepack', 12, 'resourcepacks'),
    'datapack': ('datapack', 6945, 'datapacks'),
    'plugin': ('plugin', 5, 'plugins') }
CONTENT_TYPE_LABELS = {
    'mod': 'Mod 模组',
    'shader': '光影',
    'resourcepack': '资源包',
    'datapack': '数据包',
    'plugin': '插件' }
LOADERS = [
    'vanilla',
    'fabric',
    'forge',
    'neoforge',
    'quilt']
LOADER_LABELS = {
    'vanilla': '原版',
    'fabric': 'Fabric',
    'forge': 'Forge',
    'neoforge': 'NeoForge',
    'quilt': 'Quilt' }
DEFAULT_OLLAMA_URL = 'http://127.0.0.1:11434'
DEFAULT_AI_BASE = 'https://api.deepseek.com'
DEFAULT_AI_MODEL = 'deepseek-chat'
AI_SYSTEM = '你是 QCL 启动器内置的 Minecraft 助手，服务于中文玩家。\n规则：\n1. 用简体中文回答，简洁直接，不写客套话。\n2. 只依据给定的实时资料回答。资料里没有的信息，直接说「资料里没找到，不敢乱说」，并建议去哪里查（如中文 Minecraft Wiki、Modrinth）。\n3. 严禁脑补：不确定的版本号、更新内容、方块/生物/Mod 名称一律不要写出来。\n   编造一个看起来很像的答案，比诚实说不知道糟糕得多。\n4. 参考资料可能混入无关内容（别的软件、别的版本），与问题无关的部分直接忽略，\n   不要把它们拼进答案。\n5. 涉及操作路径时给出具体到菜单的步骤。\n'
AI_PLAN_SYSTEM = '你是 Minecraft 整合方案设计师。用户用一句话描述想玩的内容，你输出一个 JSON 方案。\n必须且只能输出 JSON 对象，不要任何解释文字、不要代码块围栏。\n字段：\n  "name": 实例名称（10 字以内，中文）\n  "summary": 一句话说明这个实例能玩到什么（40 字以内）\n  "mc": 推荐的 Minecraft 正式版本号，如 "1.21.1"\n  "loader": 只能取 "fabric" / "forge" / "neoforge" / "quilt" / "vanilla"\n  "memory_mb": 建议分配内存 MB 整数\n  "mods": [{"slug": "Modrinth 上的英文 slug 或中文名", "name": "中文名", "why": "推荐理由 12 字内"}]\nmods 数量控制在 6-14 个，按重要性排序，第一个必须是核心 Mod。\n只推荐你确信真实存在的 Mod，宁缺毋滥。'
DEFAULT_HOST = 'http://127.0.0.1:25800'
DEFAULT_API_PORT = 25800
DEFAULT_RELAY_PORT = 25801
LAN_MULTICAST_GROUP = '224.0.2.60'
LAN_MULTICAST_PORT = 4445
LOCAL_PROXY_PORT = 25565
JAVA_SPEC = [
    (21, '1.20.5'),
    (17, '1.18'),
    (8, '1.0')]

def required_java(mc_version):
    '''根据 MC 版本返回所需 Java 主版本'''
    
    def key(v):
        parts = []
        for p in v.split('.')[:3]:
            try:
                parts.append(int(p))
            except ValueError:
                parts.append(0)
                continue
        while len(parts) < 3:
            parts.append(0)
        return tuple(parts)

    
    try:
        cur = key(mc_version)
        for java, mv in JAVA_SPEC:
            if not cur >= key(mv):
                continue
            
            return JAVA_SPEC, java
        return 8
    except Exception:
        return 21

