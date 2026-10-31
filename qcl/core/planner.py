# Source Generated with Decompyle++
# File: planner.pyc (Python 3.13)

'''一句话生成实例：把自然语言描述翻译成可执行的整合方案。

设计要点 —— **AI 负责发散，Modrinth 负责保真**：

本地小模型（1.5B / 7B）很擅长理解"我想玩带机械和自动化的科技包"这种意图，
但极不擅长记住正确的 Mod 名字和版本，编造是常态。
所以流程是：

    用户一句话
      → 本地规则命中主题，产出候选 Mod 清单（离线可用）
      → 可选：让 AI 修饰命名、简介、补充点子
      → **每个 Mod 都拿去 Modrinth 校验**，确认存在且有适配 [mc+loader] 的版本
      → 只有校验通过的才进入最终方案，交给下载器安装

这样即使 AI 完全在胡说，用户看到的清单依然全部真实可装。
'''
import re
from . import ai, loaders, modrinth, vanilla, websearch
from .constants import AI_PLAN_SYSTEM, LOADER_LABELS
PREFERRED_MC = [
    '1.21.1',
    '1.20.1',
    '1.21.4',
    '1.20.4',
    '1.19.2',
    '1.18.2']
THEMES = [
    {
        'key': 'optimize',
        'label': '性能优化',
        'keys': [
            '优化',
            '流畅',
            '帧数',
            'fps',
            '低配',
            '卡顿',
            '卡',
            '顺滑',
            '帧率低',
            '性能',
            '垃圾配置',
            '老电脑',
            '提升帧率'],
        'loader': 'fabric',
        'mc': [],
        'mem': 4096,
        'desc': '让 Minecraft 在低配机器上也能跑满帧',
        'mods': [
            ('sodium', 'Sodium', '渲染重写，帧数起飞'),
            ('lithium', 'Lithium', '服务端/游戏逻辑优化'),
            ('ferrite-core', 'FerriteCore', '大幅降低内存占用'),
            ('immediatelyfast', 'ImmediatelyFast', 'UI 与实体渲染优化'),
            ('entityculling', 'EntityCulling', '跳过多余实体渲染'),
            ('memoryleakfix', 'MemoryLeakFix', '修复内存泄漏'),
            ('reeses-sodium-options', "Reese's Sodium Options", '让 Sodium 有正常设置界面'),
            ('noisium', 'Noisium', '地形生成加速'),
            ('krypton', 'Krypton', '网络包优化'),
            ('modmenu', 'Mod Menu', '查看已装 Mod 列表')] },
    {
        'key': 'tech',
        'label': '大型科技',
        'keys': [
            '科技',
            '自动化',
            '机械',
            '工业',
            'mod整合',
            '大型mod',
            '发电',
            '机械动力',
            '流水线',
            '工厂',
            '机器'],
        'loader': 'neoforge',
        'mc': [
            '1.21.1',
            '1.20.1'],
        'mem': 6144,
        'desc': '传送带、自动化流水线与成套工业体系',
        'mods': [
            ('create', 'Create 机械动力', '齿轮传动与自动化核心'),
            ('jei', 'JEI 物品管理器', '查合成表必备'),
            ('curios', 'Curios API', '饰品/扩展槽位支持库'),
            ('jade', 'Jade', '屏幕左上角方块信息'),
            ('appleskin', 'AppleSkin', '食物饱和度可视化'),
            ('xaeros-minimap', "Xaero's Minimap", '小地图与坐标标记'),
            ('mouse-tweaks', 'Mouse Tweaks', '批量整理物品'),
            ('shulkerboxtooltip', 'Shulker Box Tooltip', '潜影盒内容预览')] },
    {
        'key': 'magic',
        'label': '魔法冒险',
        'keys': [
            '魔法',
            '法术',
            '咒语',
            '魔导',
            '神秘',
            '炼金',
            '巫术'],
        'loader': 'neoforge',
        'mc': [
            '1.21.1',
            '1.20.1'],
        'mem': 6144,
        'desc': '法术、魔法植物与 Boss 挑战',
        'mods': [
            ('botania', 'Botania 植物魔法', '以花为核心的科技魔法'),
            ('ars-nouveau', 'Ars Nouveau 新生魔艺', '可自定义法术'),
            ('iron-spells-n-spellbooks', "Iron's Spellbooks", 'RPG 法术与法杖战斗'),
            ('curios', 'Curios API', '饰品槽位支持库'),
            ('jei', 'JEI 物品管理器', '查合成表必备'),
            ('jade', 'Jade', '方块信息提示'),
            ('appleskin', 'AppleSkin', '食物信息显示'),
            ('xaeros-minimap', "Xaero's Minimap", '小地图')] },
    {
        'key': 'adventure',
        'label': '探索冒险',
        'keys': [
            '冒险',
            '探索',
            '生物群系',
            '群系',
            '新生物',
            'boss',
            'rpg',
            '开荒',
            '新地形',
            '地牢',
            '遗迹'],
        'loader': 'forge',
        'mc': [
            '1.20.1',
            '1.21.1'],
        'mem': 6144,
        'desc': '新世界、新生物与丰富的地形结构',
        'mods': [
            ('biomesoplenty', "Biomes O' Plenty", '新增几十种生物群系'),
            ('alexsmobs', "Alex's Mobs", '新增大量生物'),
            ('waystones', 'Waystones 路标', '传送点，跑图神器'),
            ('natures-compass', "Nature's Compass", '定位任意群系'),
            ('jade', 'Jade', '方块信息提示'),
            ('jei', 'JEI 物品管理器', '查合成表必备'),
            ('xaeros-minimap', "Xaero's Minimap", '小地图'),
            ('xaeros-world-map', "Xaero's World Map", '全屏世界地图')] },
    {
        'key': 'building',
        'label': '建筑创造',
        'keys': [
            '建筑',
            '建造',
            '创造',
            '装修',
            '图纸',
            '蓝图',
            '方块',
            '房子',
            '建房',
            '投影',
            '搭建',
            '建家'],
        'loader': 'fabric',
        'mc': [
            '1.21.1',
            '1.20.1'],
        'mem': 4096,
        'desc': '批量建造、投影与精细装饰',
        'mods': [
            ('worldedit', 'WorldEdit 创世神', '批量编辑地形'),
            ('litematica', 'Litematica 投影', '按图纸施工'),
            ('jei', 'JEI 物品管理器', '随手取方块'),
            ('jade', 'Jade', '方块信息提示'),
            ('xaeros-minimap', "Xaero's Minimap", '小地图')] },
    {
        'key': 'qol',
        'label': '生存辅助',
        'keys': [
            '辅助',
            '便利',
            'qol',
            '实用',
            '小地图',
            '提示',
            '背包整理',
            '原版增强',
            '轻量',
            '原版向',
            '原味'],
        'loader': 'fabric',
        'mc': [],
        'mem': 4096,
        'desc': '小幅增强原版体验，不改变玩法核心',
        'mods': [
            ('jei', 'JEI 物品管理器', '查合成表必备'),
            ('jade', 'Jade', '方块信息提示'),
            ('xaeros-minimap', "Xaero's Minimap", '小地图'),
            ('appleskin', 'AppleSkin', '食物饱和度'),
            ('mouse-tweaks', 'Mouse Tweaks', '批量整理物品'),
            ('shulkerboxtooltip', 'Shulker Box Tooltip', '潜影盒预览'),
            ('modmenu', 'Mod Menu', '查看 Mod 列表')] }]
MC_IN_TEXT = re.compile('\\b(\\d{1,2}\\.\\d{1,2}(?:\\.\\d{1,2})?)\\b')

def parse(text):
    '''离线解析用户描述 → 命中的主题、显式提到的版本/加载器'''
    if not text:
        text
    t = ''.lower()
    hits = []
    for th in THEMES:
        for k in th['keys']:
            if not k in t:
                continue
            hits.append(th)
            th['keys']
    themes = []
    seen = set()
    for h in hits:
        if not h['key'] not in seen:
            continue
        seen.add(h['key'])
        themes.append(h)
    mc = ''
    for m in MC_IN_TEXT.finditer(t):
        cand = m.group(1)
        if not cand.count('.') >= 1:
            continue
        mc = cand
        MC_IN_TEXT.finditer(t)
    loader = ''
    for key, names in (('fabric', [
        'fabric',
        '法布里克',
        ' Fabric']), ('forge', [
        'forge',
        '佛吉',
        'forge 模组']), ('neoforge', [
        'neoforge',
        'neo',
        '新forge',
        '新佛吉']), ('quilt', [
        'quilt',
        '奎尔特']), ('vanilla', [
        '原版',
        '纯净',
        '无mod'])):
        for n in names:
            if not n.lower() in t:
                continue
            loader = key
            names
    if not loader:
        continue
    mem = 0
    mm = re.search('(\\d{1,2})\\s*[gG][bB]?', t)


def _looks_cn(s):
    '''是否像中文（含一定比例 CJK 字符）'''
    if not s:
        pass
    return False
    cn = (lambda .0: .0continue1continue)(s())
    return cn >= max(2, len(s) * 0.3)


def _good_name(name):
    '''AI 起的实例名是否可用。

除了"必须是中文"，还要挡掉一类退化输出：把主题词直接复读一遍当名字，
比如「科技科技」。内置方案库起的「大型科技整合包」反而更像回事。
'''
    if _looks_cn(name) or len(name) > 20:
        pass
    return False
    half = len(name) // 2
    if half >= 2 and name[:half] == name[half:]:
        pass
    return False
    return True


def default_mc(loader):
    '''没指定版本时挑一个：优先加载器支持且 Mod 生态成熟的版本'''
    
    try:
        , []
        
        try:
            vanilla.releases(), v, rel, v = None
            if not rel:
                pass
            return PREFERRED_MC[0]
            rel_set = set(rel)
            for cand in PREFERRED_MC:
                if not cand in rel_set:
                    continue
                
                return PREFERRED_MC, cand
            if rel:
                pass
            return rel[0]
            return PREFERRED_MC[0]
            
            try:
                
            except Exception:
                [] = None
                continue


_LOOKUP_CACHE = { }

def lookup_mod(slug, name, mc, loader, strict):
    '''按 slug（失败则按名搜索）在 Modrinth 上定位 Mod，并取适配 (mc, loader) 的版本。

strict=True 时**只允许精确 slug 命中，不做模糊搜索**。AI 补充的 Mod 必须走这条路：
模型经常给出不存在或张冠李戴的名字，模糊搜索会替它"找到"一个不相干的 Mod，
结果就是用户实例里多一个来路不明的东西。宁可丢掉，也不能装错。
'''
    if not slug:
        slug
    key = (name, mc, loader, strict)
    if key in _LOOKUP_CACHE:
        pass
    return _LOOKUP_CACHE[key]
    proj = { }
    pid = ''
    if slug:
        if not modrinth.project(slug):
            modrinth.project(slug)
        proj = { }
        if not proj.get('id'):
            proj.get('id')
            if not proj.get('slug'):
                proj.get('slug')
    pid = ''
    if not pid and strict:
        if name or slug:
            if not name:
                name
            (hits, _total) = modrinth.search(slug, 'mod', mc, loader, 0, 5)
            , []
            hits, h, exact, h = None
            if not exact:
                exact
            cand = hits[:1]
            if cand:
                if not cand[0].get('id'):
                    cand[0].get('id')
                pid = cand[0].get('slug')
                if not modrinth.project(str(pid)):
                    modrinth.project(str(pid))
    proj = { }
    if not name:
        name
    out = {
        'ok': False,
        'id': pid,
        'slug': slug,
        'title': slug,
        'description': '',
        'downloads': 0,
        'icon': '',
        'version': None,
        'reason': 'Modrinth 上没找到' }
    if not pid:
        _LOOKUP_CACHE[key] = out
    return out
    if not proj.get('slug'):
        proj.get('slug')
    if not proj.get('title'):
        proj.get('title')
        if not name:
            name
    if not proj.get('description'):
        proj.get('description')
    if not proj.get('downloads'):
        proj.get('downloads')
    if not proj.get('icon_url'):
        proj.get('icon_url')
    out.update({
        'id': pid,
        'slug': slug,
        'title': slug,
        'description': '',
        'downloads': 0,
        'icon': '' })
    vs = []
    
    try:
        vs = modrinth.versions(str(pid), mc, loader, 5)
        if mc and vs:
            , []
            vs, v, good, v = None
            if good:
                pass
        vs = good
        if not vs:
            if not mc:
                mc
            if not loader:
                loader
            out['reason'] = f'''暂无适配 当前版本 +  的版本'''
        elif loader and loader != 'vanilla':
            , []
            vs, v, matched, v = None
            if matched:
                vs = matched
            else:
                vs = []
                out['reason'] = '该版本不支持 %s 加载器' % LOADER_LABELS.get(loader, loader)
        if not vs:
            if not out['reason']:
                out['reason']
            out['reason'] = '暂无适配版本'
        else:
            out['ok'] = True
            out['version'] = vs[0]
            out['version']['project_id'] = pid
            out['version']['platform'] = 'modrinth'
            out['reason'] = ''
        _LOOKUP_CACHE[key] = out
        return out
        
    except Exception:
        [] = None
        continue
        
        
def check_theme_health(theme, mc, loader):
    '''某主题在某版本上的可用率，用于自动挑最优 MC 版本'''
    ok = 0
    total = len(theme['mods'])
    for slug, _n, _w in theme['mods']:
        r = lookup_mod(slug, '', mc, loader)
        if not r['ok']:
            continue
        ok += 1
    return (ok, total)


def _merge_plan(intents, mc, loader):
    if not intents['themes']:
        intents['themes']
    themes = [
        THEMES[5]]
    labels = []
    mods = []
    seen = set()
    picked_mc = mc
    for th in themes:
        if picked_mc and th['mc']:
            pass
        picked_mc = th['mc'][0]
        labels.append(th['label'])
        for slug, name, why in th['mods']:
            if slug in seen:
                continue
            seen.add(slug)
            mods.append({
                'slug': slug,
                'name': name,
                'why': why })
        themes
    if not loader:
        loader
    loader = themes[0]['loader']
    None, themes, t(t,) if themes else 4096 = max
    if not picked_mc:
        picked_mc
    return {
        'name': None,
        'summary': (lambda .0: pass)(themes[:2]()),
        'mc': '',
        'loader': loader,
        'memory_mb': mem,
        'mods': mods,
        'source': 'local' }
    

def build_plan(text, use_ai, web_search, provider, on_status):
    '''把一句话变成完整方案（含已联网校验过的真实 Mod 列表）'''
    
    def say(msg):
        if on_status:
            on_status(msg)
        return None

    intents = parse(text)
    loader = intents['loader']
    if not intents['themes']:
        intents['themes']
    themes = [
        THEMES[5]]
    if not loader:
        pass
    loader = themes[0]['loader']
    cands = []
    if not themes[0].get('mc'):
        themes[0].get('mc')
    for c in [
        intents['mc']] if intents['mc'] else [] + list([]) + PREFERRED_MC:
        if not c:
            continue
        if not c not in cands:
            continue
        cands.append(c)
    if not cands:
        pass
    cands = [
        default_mc(loader)]
    ai_suggest = None
    if use_ai:
        if not provider:
            provider
        p = ai.resolve_provider()
        if p.get('kind') in ('ollama', 'openai'):
            say('正在让 AI 设计方案…')
            
            try:
                ctx = ''
                if web_search:
                    say('正在联网查找相关资料…')
                    
                    try:
                        g = websearch.gather(f'''Minecraft   modpack''', 3, 0)
                        if not g.get('context'):
                            g.get('context')
                        ctx = ''
                        
                        try:
                            msgs = [
                                {
                                    'role': 'system',
                                    'content': AI_PLAN_SYSTEM }]
                            if ctx:
                                pass
                            msgs.append({
                                'role': 'system',
                                'content': '参考资料：\n' + ctx[:2500] })
                            msgs.append({
                                'role': 'user',
                                'content': '我想玩的是：%s\n请给出整合方案 JSON。' % text })
                            ai_suggest = ai.chat_json(msgs, p, None, 0.8, 700)
                            plan = _merge_plan(intents, '', loader)
                            local_name = plan['name']
                            if ai_suggest and isinstance(ai_suggest, dict):
                                if not ai_suggest.get('name'):
                                    ai_suggest.get('name')
                                ai_name = str('').strip()
                                plan['name'] = ai_name if _good_name(ai_name) else local_name
                                if not ai_suggest.get('summary'):
                                    ai_suggest.get('summary')
                                ai_summary = str('').strip()
                                if _looks_cn(ai_summary):
                                    plan['summary'] = ai_summary[:80]
                                if ai_suggest.get('loader') in ('fabric', 'forge', 'neoforge', 'quilt', 'vanilla'):
                                    plan['loader'] = ai_suggest['loader']
                                
                                try:
                                    if not ai_suggest.get('memory_mb'):
                                        ai_suggest.get('memory_mb')
                                    m = int(0)
                                    if  <= 1024, m or 1024, m <= 32768:
                                        pass
                                    
                                try:
                                    if ai_suggest.get('mc'):
                                        pass
                                    cands.insert(0, str(ai_suggest['mc']))
                                    if not ai_suggest.get('mods'):
                                        ai_suggest.get('mods')
                                    [] = min(m, 32768)
                                    
                                    , {}, known = plan['mods'], m
                                    m = None
                                    for am in ai_mods:
                                        if not isinstance(am, dict):
                                            continue
                                        if not am.get('slug'):
                                            am.get('slug')
                                        slug = str('').strip()
                                        if not am.get('name'):
                                            am.get('name')
                                        nm = str('').strip()
                                        if not slug and nm:
                                            continue
                                        if slug in known:
                                            continue
                                        known.add(slug)
                                        if not nm:
                                            nm
                                        if not am.get('why'):
                                            am.get('why')
                                        plan['mods'].append({
                                            'slug': slug,
                                            'name': slug,
                                            'why': str('AI 推荐')[:20],
                                            'from_ai': True })
                                    plan['source'] = 'local+ai'
                                    if not plan.get('loader'):
                                        plan.get('loader')
                                    plan['loader'] = loader
                                    loader = loader
                                    best_score = -1
                                    best_mc = cands[0]
                                    say('正在挑选合适的游戏版本…')
                                    for mc in cands[:3]:
                                        (ok, tot) = check_theme_health(themes[0], mc, loader)
                                        score = ok
                                        if score > best_score:
                                            best_mc = mc
                                        best_score = score
                                        if not ok == tot:
                                            continue
                                        cands[:3]
                                    plan['mc'] = best_mc
                                    say('正在校验 Mod 可用性…')
                                    dropped = []
                                    checked = []
                                    for i, m in enumerate(plan['mods']):
                                        if not m.get('name'):
                                            m.get('name')
                                        say('校验 Mod %d/%d：%s' % (i + 1, len(plan['mods']), m.get('slug')))
                                        r = lookup_mod(m.get('slug'), m.get('name'), best_mc, loader, bool(m.get('from_ai')))
                                        item = dict(m)
                                        if not r.get('title'):
                                            r.get('title')
                                            if not m.get('name'):
                                                m.get('name')
                                        if not r.get('description'):
                                            r.get('description')
                                        if not r.get('downloads'):
                                            r.get('downloads')
                                        if not r.get('icon'):
                                            r.get('icon')
                                        if not r.get('id'):
                                            r.get('id')
                                        if not r.get('reason'):
                                            r.get('reason')
                                        item.update({
                                            'ok': r.get('ok', False),
                                            'title': m.get('slug'),
                                            'description': '',
                                            'downloads': 0,
                                            'icon': '',
                                            'project_id': '',
                                            'reason': '',
                                            'version': r.get('version') })
                                        checked if item['ok'] else dropped.append(item)
                                    plan['mods'] = checked
                                    plan['dropped'] = dropped
                                    plan['availability'] = '%d/%d' % (len(checked), len(checked) + len(dropped))
                                    if checked and dropped:
                                        plan['notes'] = [
                                            f'''没能找到适配  +  的 Mod，可试试在方案里换一个游戏版本''']
                                    return plan
                                    except Exception:
                                        ctx = ''
                                        
                                        try:
                                            continue
                                            
                                            try:
                                                pass
                                            except Exception:
                                                ai_suggest = None
                                                continue
                                                except Exception:
                                                    continue
                                                    
                                                    except Exception:
                                                        None, None, None, e = None
                                                        r = {
                                                            'ok': False,
                                                            'reason': '查询失败：%s' % e,
                                                            'slug': m.get('slug'),
                                                            'title': m.get('name') }
                                                        e = None
                                                        del e
                                                        continue
                                                        e = None
                                                        del e


def explain_mc_update(text, provider, use_search, on_status, on_delta, should_stop):
    '''问答：回答 Minecraft 相关提问（版本特性、Mod 用法、报错排查等）'''
    
    def say(msg):
        if on_status:
            on_status(msg)
        return None

    if not provider:
        provider
    p = ai.resolve_provider()
    if p.get('kind') not in ('ollama', 'openai'):
        if not p.get('error'):
            p.get('error')
    return {
        'ok': False,
        'answer': '',
        'sources': [],
        'error': 'AI 后端不可用，请到设置里配置' }
    sources = []
    ctx = ''
    if use_search:
        say('正在联网搜索…')
        
        try:
            sources = []
            ctx = ''
            g = websearch.ask_context(text, 5, 2, say)
            if not g.get('context'):
                g.get('context')
            if not g.get('sources'):
                g.get('sources')
            sources = []
            ctx = ''
            say('AI 正在思考…')
            msgs = ai.build_messages(text, ctx)
            
            try:
                answer = ai.chat(msgs, p, 0.6, 1400, on_delta, should_stop)
                return {
                    'ok': True,
                    'answer': answer,
                    'sources': sources }
                except Exception:
                    e = None
                    say('搜索失败：%s' % e)
                    e = None
                    del e
                    continue
                    e = None
                    del e
            except ai.Stopped:
                e = None
                if not getattr(e, 'partial', ''):
                    getattr(e, 'partial', '')
                del e
                return None
                None = 
                del e
                except Exception:
                    e = None
                    del e
                    return None
                    None = 
                    del e

