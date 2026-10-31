# Source Generated with Decompyle++
# File: websearch.pyc (Python 3.13)

'''联网搜索：给 AI 提供它训练数据里没有的实时资料。

Minecraft 的版本特性、Mod 适配情况每周都在变，纯离线模型必然答错或编造。
这里提供三个能力：

- search()     统一的多源搜索（Minecraft Wiki → Bing RSS → 360/搜狗 HTML）
- read_page()  抓取网页正文，作为 AI 的引用材料
- gather()     搜索 + 抓正文，打包成一段可以直接塞进 prompt 的上下文

所有数据源都无需 API Key。单个源失败自动回落到下一个。
'''
import html
import re
import time

ElementTree
from . import net
import xml.etree.ElementTree, etree
SEARCH_TIMEOUT = 12
READ_TIMEOUT = 15
MAX_PAGE_CHARS = 3500
MAX_SNIPPET = 300
SEARCH_BUDGET = 12
BROWSER_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 KHTML, like Gecko Chrome/120.0 Safari/537.36'
UA_POOL = (net.UA, BROWSER_UA, 'curl/8.4.0', 'Mozilla/5.0')
_MIN_GAP = 0.9
_LAST_HIT = { }
_TAG = re.compile('<[^>]+>')
_SCRIPT = re.compile('<(script|style)[\\s\\S]*?</\\1>', re.I)
_WS = re.compile('[ \\t\\u3000]+')
_NL = re.compile('\\n\\s*\\n+')
_PROVIDER_CACHE = {
    'ok': None,
    'ts': 0 }

def clean_text(s, limit):
    '''去 HTML 标签、反转义、压缩空白'''
    if not s:
        pass
    return ''
    s = _SCRIPT.sub(' ', s)
    s = _TAG.sub(' ', s)
    s = html.unescape(s)
    s = _WS.sub(' ', s)
    s = _NL.sub('\n\n', s)
    s = (lambda .0: pass)(s.splitlines()()).strip()
    if limit and len(s) > limit:
        pass
    s = s[:limit].rstrip() + '…'
    return s


def _strip_html(s):
    return clean_text(s)


def _throttle(url):
    '''同域请求节流：站点会在短时间内连续访问时直接断连'''
    host = ''
    
    try:
        urlparse = urlparse
        import urllib.parse
        host = urlparse(url).netloc
        now = time.time()
        wait = _MIN_GAP - now - _LAST_HIT.get(host, 0)
        if wait > 0:
            pass
        time.sleep(wait)
        _LAST_HIT[host] = time.time()
        return None
    except Exception:
        host = url
        continue


def get_text_multi(url, timeout = READ_TIMEOUT, min_len = 200, uas = UA_POOL, params = None):
    '''轮换 UA 抓取文本，返回第一个「看起来像正常内容」的结果'''
    for ua in uas:
        _throttle(url)
        t = net.get_text(*(url,), **{
            'timeout': timeout,
            'default': '',
            'headers': {
                'User-Agent': ua } })
        if not t:
            continue
        if not len(t) >= min_len:
            continue
        
        return uas, t
    return ''
    continue


def get_json_multi(url, timeout = READ_TIMEOUT, **params):
    '''同上，但取 JSON'''
    for ua in (net.UA, 'curl/8.4.0'):
        _throttle(url)
        d = net.get_json(url, timeout, None, params, {
            'User-Agent': ua })
        if not d:
            continue
        
        return (net.UA, 'curl/8.4.0'), d
    return None
    continue


def search_wiki(query, limit):
    '''Minecraft Wiki（官方 wiki，权威且无需 Key）'''
    data = None
    for attempt in (0, 1):
        data = get_json_multi('https://minecraft.wiki/api.php', SEARCH_TIMEOUT, 'query', 'search', query, limit, 'json')
        if not data and data.get('error'):
            (0, 1)
        elif not attempt == 0:
            continue
        time.sleep(1.2)
    out = []
    if not data:
        data
    if not { }.get('query'):
        { }.get('query')
    if not { }.get('search'):
        { }.get('search')
    for it in []:
        if not it.get('title'):
            it.get('title')
        title = clean_text('')
        if not title:
            continue
        if not it.get('snippet'):
            it.get('snippet')
        out.append({
            'title': title,
            'url': 'https://minecraft.wiki/w/%s' % title.replace(' ', '_'),
            'snippet': clean_text('', MAX_SNIPPET),
            'source': 'Minecraft Wiki' })
    return out


def search_bing(query, limit):
    '''Bing RSS：返回结构化 XML，比解析 HTML 稳定得多'''
    text = get_text_multi('https://www.bing.com/search', SEARCH_TIMEOUT, 80, {
        'q': query,
        'format': 'rss',
        'count': limit })
    if (text or '<rss' not in text) and '<feed' not in text:
        pass
    return []
    out = []
    
    try:
        root = ET.fromstring(text.encode('utf-8'))
        items = root.findall('.//item')
        if not items:
            ns = '{http://www.w3.org/2005/Atom}'
            for e in root.findall('.//%sentry' % ns):
                link = e.find('%slink' % ns)
                if not e.findtext('%stitle' % ns):
                    e.findtext('%stitle' % ns)
                if not link.get('href') if link is not None else '':
                    link.get('href') if link is not None else ''
                if not e.findtext('%ssummary' % ns):
                    e.findtext('%ssummary' % ns)
                out.append({
                    'title': clean_text(''),
                    'url': '',
                    'snippet': clean_text('', MAX_SNIPPET),
                    'source': 'Bing' })
            , []
        return o,[:limit]
        for None in items:
            if not it.findtext('title'):
                it.findtext('title')
            title = clean_text('')
            if not it.findtext('link'):
                it.findtext('link')
            url = ''.strip()
            if not title or url:
                continue
            if not it.findtext('description'):
                it.findtext('description')
            out.append({
                'title': title,
                'url': url,
                'snippet': clean_text('', MAX_SNIPPET),
                'source': 'Bing' })
        return out[:limit]
    except Exception:
        return 
        

def _search_html(url_tpl, query, limit, link_re):
    
    try:
        quote = quote
        import urllib.parse
        text = get_text_multi(url_tpl % quote(query), SEARCH_TIMEOUT, 300)
        if not text:
            pass
        return []
        seen = set()
        out = []
        for m in link_re.finditer(text):
            title = clean_text(m.group('title'))
            href = m.group('url')
            if href and title and href in seen or len(title) < 4:
                continue
            seen.add(href)
            out.append({
                'title': title[:120],
                'url': href,
                'snippet': '',
                'source': '网页搜索' })
            if not len(out) >= limit:
                continue
            link_re.finditer(text)
            return out
        return out
    except Exception:
        return 


def search_360(query, limit):
    pat = re.compile('<a[^>]+href="(?P<url>https?://[^"]+)"[^>]*>(?P<title>[^<]{4,})</a>')
    raw = _search_html('https://www.so.com/s?q=%s', query, limit * 6, pat)
    out = []
    for r in raw:
        u = r['url']
        if 'so.com' in u and '360' in u or 'javascript' in u:
            continue
        out.append(r)
        if not len(out) >= limit:
            continue
        raw
        return out
    return out


def search_sogou(query, limit):
    pat = re.compile('<a[^>]+href="(?P<url>https?://[^"]+)"[^>]*>(?P<title>[^<]{4,})</a>')
    raw = _search_html('https://www.sogou.com/web?query=%s', query, limit * 6, pat)
    out = []
    for r in raw:
        u = r['url']
        if 'sogou' in u or 'javascript' in u:
            continue
        out.append(r)
        if not len(out) >= limit:
            continue
        raw
        return out
    return out

PROVIDERS = (('Minecraft Wiki', search_wiki), ('Bing', search_bing), ('360 搜索', search_360), ('搜狗', search_sogou))

def search(query, limit, budget):
    '''多源搜索，任一源成功即返回。结果按源去重。

budget 是整体时间预算（秒）。必须给：几个源遇到连不通的站点时会各自
慢慢超时，串起来能把"生成方案"拖到几分钟，用户只看到一直转圈。
'''
    if not query:
        query
    query = ''.strip()
    if not query:
        pass
    return []
    if budget is None:
        pass
    budget = SEARCH_BUDGET
    started = time.time()
    seen = set()
    out = []
    for name, fn in PROVIDERS:
        if out and time.time() - started > budget:
            PROVIDERS
        else:
            got = []
            if time.time() - started <= budget * 2:
                pass
            got = fn(query, limit)
            if not got:
                got
            for r in []:
                if not r.get('url'):
                    r.get('url')
                url = ''.rstrip('/')
                if not url:
                    url
                key = r.get('title')
                if key or key in seen:
                    continue
                seen.add(key)
                r.setdefault('source', name)
                out.append(r)
            PROVIDERS
            if len(out) >= limit and name not in ('Minecraft Wiki',):
                pass
            elif not len(out) >= limit * 2:
                continue
            if not name in ('Minecraft Wiki',):
                continue
    return out[:limit * 2]
    except Exception:
        got = []
    continue


def read_page(url, limit = MAX_PAGE_CHARS):
    '''抓取网页正文（去标签），失败返回空串'''
    if not url or url.startswith('http'):
        pass
    return ''
    hit = _PAGE_CACHE.get(url)
    if hit and time.time() - hit[0] < _PAGE_TTL:
        pass
    return hit[1][:limit]
    body = ''
    wikitext = _read_mediawiki(url)
    if wikitext:
        body = wikitext
    else:
        text = get_text_multi(url, READ_TIMEOUT, 200)
        if text:
            pass
        body = scrub_page_noise(clean_text(text, limit * 3))
    if not body:
        pass
    return ''
    if len(body) > limit:
        pass
    body = body[:limit].rstrip() + '…'
    _PAGE_CACHE[url] = (time.time(), body)
    return body

_MW_HOSTS = ('minecraft.wiki', 'zh.minecraft.wiki', 'wikipedia.org')
_PAGE_CACHE = { }
_PAGE_TTL = 300

def scrub_page_noise(text):
    '''去掉 MediaWiki 页面里对回答无用的噪声。

正常情况下走 extracts 拿到的就是干净正文；但接口被限流时会退回抓 HTML，
里面混着模板展开残渣 ``(link to Foo article, displayed as Bar)``
和信息框的 JSON 片段。模型会把这些原样抄进答案，看起来就是一屏乱码。
'''
    if not text:
        text
    t = ''
    t = re.sub('\\(link to [^)]*?displayed as ([^)]*)\\)', '\\1', t)
    t = re.sub('\\(link to [^)]*\\)', '', t)
    for junk in ('Jump to navigation Jump to search', 'From Minecraft Wiki'):
        t = t.replace(junk, ' ')
    t = re.sub('"(?:field|label|rows|images|title|data)"\\s*:\\s*"[^"]*"[,\\s]*', ' ', t)
    t = re.sub('[{}]', ' ', t)
    t = re.sub('[ \\t]{2,}', ' ', t)
    return t.strip()


def _read_mediawiki(url):
    for host in _MW_HOSTS:
        if host not in url:
            continue
        base = None
        if 'minecraft.wiki' in url:
            base = 'https://minecraft.wiki'
        elif 'wikipedia.org' in url:
            pass
        base = 'https://%s' % url.split('/')[2]
        if not base:
            continue
        title = ''
        for sep in ('/wiki/', '/w/'):
            if not sep in url:
                continue
            title = url.split(sep, 1)[1]
            ('/wiki/', '/w/')
    title = title.split('?')[0].split('#')[0]
    if not title:
        continue
    unquote = unquote
    import urllib.parse
    title = unquote(title)
    for attempt in (0, 1):
        data = get_json_multi(base + '/api.php', READ_TIMEOUT, 'query', 'extracts', 1, title, 1, 'json')
        if not data:
            data
        if not { }.get('query'):
            { }.get('query')
        if not { }.get('pages'):
            { }.get('pages')
        pages = { }
        for _pid, p in pages.items():
            if not p.get('extract'):
                p.get('extract')
            ex = clean_text('')
            if not ex:
                continue
            
            
            return None, (0, 1), pages.items(), scrub_page_noise(ex)
        if not attempt == 0:
            continue
        time.sleep(1)
    continue
    return ''
    continue

_VERSION_RE = re.compile('(\\d+\\.\\d+(?:\\.\\d+)?)')
_FILLER = ('更新了什么', '更新内容', '加入了哪些', '有什么新内容', '新增了什么', '有哪些新', '介绍一下', '讲讲', '说说', '是什么', '什么是', '怎么', '如何', '为什么', '新特性', '怎么玩', '?', '？', '呢', '啊', '呀', '的', '了', '和', '与')

def condense_question(text, max_len):
    '''把口语长句压成搜索引擎吃得住的短查询。

实测对比：
  「Minecraft 1.21 加入了哪些新内容？」直搜 → 只回官网首页、百度百科；
  「Minecraft 1.21 新内容」→ 真正相关的资料页。
搜索引擎做的是关键词匹配，不是阅读理解，整句问句反而拖累结果质量。
'''
    if not text:
        text
    q = _VERSION_RE.sub(' ', '')
    for w in _FILLER:
        q = q.replace(w, ' ')
    q = re.sub('\\s+', ' ', q).strip(' ，,。.？?、!！~:： ')
    return q[:max_len]


def english_query(text, max_len):
    '''把中文提问翻译成给搜索引擎用的英文关键词。

为什么要转英文（实测结论）：
  「Minecraft Fabric 和 Forge 有什么区别？」→ 官网首页、百度百科；
  「Minecraft Fabric Forge difference」→ 真正讲得清区别的资料页。
中文 Minecraft Wiki 已停止维护、接口返回 0 条，
能查到的权威资料几乎全是英文的，中文长句直搜命中率极低。
这里只做「术语级」对照，不追求整句通顺 —— 搜索引擎本来就不看句子太语法。
'''
    if not text:
        text
    raw = ''
    used = set()
    toks = []
    for cn, en in _CN2EN:
        if not cn in raw:
            continue
        if not cn not in used:
            continue
        used.add(cn)
        if not en:
            continue
        toks.append(en)
    for t in _ascii_terms(raw).split():
        tl = t.lower()
        if tl in ('minecraft', 'mc'):
            continue
    , []
    if not tl, toks, x not in x,:
        continue
    toks.append(t)
    continue
    return re.sub('\\s+', ' ', ('Minecraft ' + ' '.join(toks)).strip())[:max_len]
    

def version_page_url(version):
    '''版本更新说明的权威条目页（英文站，中文站已停止维护）。'''
    return 'https://minecraft.wiki/w/Java_Edition_%s' % version

_CN2EN = (('优化整合包', 'modpack optimization'), ('失败了', 'failed'), ('新内容', 'new features'), ('新特性', 'new features'), ('更新了什么', 'changes'), ('有什么改动', 'changes'), ('怎么办', 'fix'), ('是什么原因', 'reason'), ('区别', 'difference'), ('对比', 'comparison'), ('哪个好', 'vs'), ('推荐', 'best'), ('教程', 'tutorial'), ('报错', 'error'), ('闪退', 'crash'), ('崩溃', 'crash crash-report'), ('黑屏', 'black screen'), ('卡顿', 'lag stutter'), ('掉帧', 'low FPS'), ('帧数', 'FPS'), ('内存', 'memory RAM'), ('显卡', 'GPU'), ('驱动', 'driver'), ('优化', 'optimization'), ('光影', 'shader'), ('材质包', 'resource pack'), ('资源包', 'resource pack'), ('数据包', 'data pack'), ('皮肤', 'skin'), ('模组', 'mod'), ('整合包', 'modpack'), ('加载器', 'mod loader'), ('服务器', 'server'), ('联机', 'multiplayer'), ('局域网', 'LAN'), ('存档', 'world save'), ('种子', 'seed'), ('指令', 'command'), ('红石', 'redstone'), ('电路', 'redstone circuit'), ('附魔', 'enchanting'), ('酿造', 'brewing'), ('村民', 'villager'), ('交易', 'trading'), ('下界', 'nether'), ('地狱', 'nether'), ('末地', 'the end'), ('末影龙', 'ender dragon'), ('凋灵', 'wither'), ('监守者', 'warden'), ('刷怪塔', 'mob farm'), ('生物', 'mob'), ('怪物', 'mob'), ('群系', 'biome'), ('遗迹', 'structure'), ('要塞', 'stronghold'), ('地形', 'terrain generation'), ('挖矿', 'mining'), ('建筑', 'building'), ('自动', 'automation'), ('机械', 'mechanism'), ('魔法', 'magic'), ('安装', 'install'), ('卸载', 'uninstall'), ('启动', 'launch'), ('版本', 'version'), ('怎么', ''), ('如何', ''), ('为什么', ''))

def _ascii_terms(text):
    '''挑出提问里的英文/数字词。

中文玩家习惯把 Mod 名、加载器名、报错关键词直接写成英文，
这部分恰恰是搜索引擎唯一能好好理解的内容，要优先保留。
'''
    if not text:
        text
    return ' '.join(re.findall('[A-Za-z][A-Za-z0-9._+-]{1,}', ''))

_BING_JUNK_HOSTS = ('minecraft.net', 'mc.163.com', 'apps.microsoft.com', 'baike.baidu.com', 'zh.minecraft.wiki')
_NOISE_EN = frozenset(('difference', 'comparison', 'install', 'uninstall', 'launch', 'fix', 'tutorial', 'best', 'vs', 'failed', 'reason', 'changes', 'features', 'update', 'new'))

def looks_like_canned(results):
    '''判断结果是否只是 Bing 的实体卡片，跟真正要问的话题无关。'''
    if not results:
        results
    rs = list([])
    if len(rs) < 3:
        pass
    return False
    junk = (lambda .0: 1continue.0)(rs())
    return junk >= max(2, len(rs) - 1)


def relevant_subset(results, terms):
    '''丢掉和问题实体无关的结果。

Bing 在拿不到匹配时常退回到「词典解释」：问 Fabric/Forge 的区别，
它给剑桥词典的 difference 词条。这些结果照样写得对出一个词，
但读进去只会让 AI 说废话，不如直接不要。
'''
    if not terms:
        terms
    
    , [], keys = ''.split(), t
    t = None
    if not keys:
        if not results:
            results
    return list([])
    keep = []
    if not results:
        results
    for r in []:
        if not r.get('title'):
            r.get('title')
        if not r.get('url'):
            r.get('url')
        hay = ('' + ' ' + '').lower()
        if not (lambda .0: pass)(keys()):
            continue
        keep.append(r)
    any
    return keep
    

def search_bing_checked(query, limit, terms):
    '''带双重过滤的 Bing 搜索：先挡罐头结果，再砍掉无关的词典解释。

拿到废结果一律返回空列表，宁缺勿滥 —— 错误的参考资料比没有更糟，
AI 会拿着它一本正经地胡说。
'''
    
    try:
        got = search_bing(query, limit)
        if got or looks_like_canned(got):
            pass
        return []
        return relevant_subset(got, terms)
    except Exception:
        return 


def _bing_variants(text, short):
    '''生成几组 Bing 查询，按靠谱程度排序（都不含 "Minecraft"）。'''
    core = re.sub('\\bMinecraft\\b', '', english_query(text), re.I).strip()
    out = []
    for cand in (core, (core + ' mod').strip(), short):
        c = re.sub('\\s+', ' ', cand).strip()
        if not len(c) >= 4:
            continue
        if not c.lower() not in out:
            continue
        out.append(c)
    return out[:3]

_OFFTOPIC = re.compile('windows|apple|\\bios\\b|android|iphone|macos|linux|chrome|office|nvidia|driver update|firmware', re.I)
_MC_HINT = re.compile('minecraft|modrinth|mcmod|curseforge|\\bmod\\b|wiki|java edition', re.I)

def drop_offtopic(results):
    '''砍掉明显属于别的软件的条目。

实测：搜「1.21 新内容」会被当成 Windows 的 21H2、iOS 27 之类的版本号，
返回一堆系统更新文章。这些内容一旦进上下文，小模型会一本正经地
把它们当成 Minecraft 的内容讲出来 —— 比没资料更糟。
'''
    keep = []
    if not results:
        results
    for r in []:
        if not r.get('title'):
            r.get('title')
        if not r.get('url'):
            r.get('url')
        hay = '' + ' ' + ''
        if not _OFFTOPIC.search(hay) and _MC_HINT.search(hay):
            continue
        keep.append(r)
    return keep


def topic_terms(text, max_n):
    '''抽实体词，用来直接检索英文 Wiki 的条目名（如 "Ender Dragon"）。'''
    raw = re.sub('\\bMinecraft\\b', '', english_query(text, 200), re.I)
    out = []
    for t in raw.split():
        tl = t.lower()
        if tl in _NOISE_EN or tl in ('mc',):
            continue
    , []
    if tl, out, x not in x,:
        pass
    out.append(t)
    if not len(out) >= max_n:
        continue
    raw.split()
    return ' '.join(out)
    

def ask_context(text, limit, read_count, on_status):
    '''问答专用检索：多角度精简查询 + 优先读权威条目。

和通用 gather() 的区别：
  1. 长句先压成关键词再搜（见 condense_question）；
  2. 问到具体版本时，直接去读该版本的官方更新条目，
     不问搜索引擎——它给出来的往往只是官网首页。
返回 {"results": [...], "context": str, "sources": [url...]}
'''
    if not text:
        text
    text = ''.strip()
    short = condense_question(text)
    ver = ''
    m = _VERSION_RE.search(text)
    if m:
        pass
    ver = m.group(1)
    plan = []
    if ver:
        pass
    plan.append(('Minecraft Wiki', search_wiki, 'Java Edition ' + ver))
    topics = topic_terms(text)
    if topics and topics.lower() != 'java edition ' + ver if ver else '':
        pass
    plan.append(('Minecraft Wiki', search_wiki, topics))
    results, seen = [], set()
    
    def add(items, default_src):
        if not items:
            items
        for r in []:
            if not r.get('url'):
                r.get('url')
            u = ''.rstrip('/')
            if not u:
                u
            key = r.get('title')
            if key or key in seen:
                continue
            seen.add(key)
            r.setdefault('source', default_src)
            results.append(r)

    if ver:
        homepage = version_page_url(ver)
    add([
        {
            'title': 'Minecraft Wiki：Java Edition %s' % ver,
            'url': homepage,
            'snippet': '官方版本更新条目',
            'source': 'Minecraft Wiki' }], 'Minecraft Wiki')
    for name, fn, q in plan:
        if not q.strip():
            continue
        got = fn(q, limit)
        add(got, name)
    if not ver:
        for v in _bing_variants(text, short):
            got = search_bing_checked(v, limit, topics)
            if not got:
                continue
            add(got, 'Bing')
            _bing_variants(text, short)
    results = drop_offtopic(results)
    if ver:
        exact = version_page_url(ver).rstrip('/')
        
    r, results = results, r, , []
    return _pack_context(results[:limit * 2], read_count, on_status)
    except Exception:
        got = []
        continue
        

def _pack_context(results, read_count, on_status):
    parts = []
    for i, r in enumerate(results):
        if not r.get('snippet'):
            r.get('snippet')
        parts.append('[%d] %s\n    %s\n    %s' % (i + 1, r.get('title'), r.get('url'), ''[:MAX_SNIPPET]))
    bodies = []
    for r in results[:max(1, read_count)]:
        if on_status:
            if not r.get('title'):
                r.get('title')
        on_status('正在读取 %s' % '网页'[:40])
        if not r.get('url'):
            r.get('url')
        body = read_page('')
        if not body:
            continue
        bodies.append(f'''### \n\n''')
    ctx = '\n\n'.join(parts)
    if bodies:
        pass
    ctx += '\n\n---- 参考资料正文 ----\n\n' + '\n\n'.join(bodies)
    , []
    return {
        'results': results,
        'context': ctx, results, r,
        'sources': r, }
    

def gather(query, limit, read_count, on_status, budget):
    '''搜索 + 抓正文，打包成 AI 可直接使用的上下文。

返回 {"results": [...], "context": str, "sources": [url...]}
'''
    results = search(query, limit, budget)
    return _pack_context(results, read_count, on_status)


def available(timeout):
    '''联网搜索是否可用（结果缓存 60 秒，避免反复试探）'''
    now = time.time()
    cached = _PROVIDER_CACHE.get('ok')
    if cached is not None and now - _PROVIDER_CACHE.get('ts', 0) < 60:
        pass
    return cached
    ok = False
    
    try:
        ok = bool(search_bing('Minecraft', 3))
        if not ok:
            
            try:
                ok = bool(search_wiki('Minecraft', 3))
                _PROVIDER_CACHE['ok'] = ok
                _PROVIDER_CACHE['ts'] = now
                return ok
                except Exception:
                    ok = False
                continue
            except Exception:
                ok = False
                continue

