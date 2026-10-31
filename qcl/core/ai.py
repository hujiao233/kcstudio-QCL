# Source Generated with Decompyle++
# File: ai.pyc (Python 3.13)

'''AI 后端：本机 Ollama 优先，没有则回落到 OpenAI 兼容的云端接口。

选型理由（用户给的优先级）：
1. 本机装了 Ollama 且正在运行 → 直接用本机模型，不出网、不花钱、不泄露隐私
2. 没检测到 Ollama → 用设置里填的云端 Key（OpenAI 格式，DeepSeek/通义/豆包/OpenAI 都能填）

两个后端都支持流式输出，既能让界面边生成边显示，也能让用户点「停止」时立刻中断。
对小模型（1.5B 之类）输出不稳定要有兜底：chat_json 解析失败会重试一次并降级到默认值。
'''
import json
import re
import time
from . import net
from .constants import DEFAULT_OLLAMA_URL, AI_SYSTEM
GEN_TIMEOUT = 300
CONNECT_TO = 8

def probe_ollama(base, timeout):
    '''探测本机是否有正在运行的 Ollama。

返回 {"ok": bool, "models": [str], "base": url, "error": str}
'''
    from . import settings as st
    base = (base or st.settings.get('ai_ollama_url') or DEFAULT_OLLAMA_URL).rstrip('/')
    url = base + '/api/tags'
    try:
        import requests
        r = requests.get(url, timeout=1.5)
        if r.status_code != 200:
            return {'ok': False, 'models': [], 'base': base, 'error':
                'HTTP %s' % r.status_code}
        data = r.json() or {}
        models = []
        for m in data.get('models') or []:
            name = m.get('name') or m.get('model')
            if name:
                models.append(name)
        return {'ok': bool(models) or True, 'models': models, 'base': base,
            'error': ''}
    except Exception as e:
        return {'ok': False, 'models': [], 'base': base, 'error': type(e
            ).__name__}


def resolve_provider(force_probe):
    '''按「本机 Ollama → 云端 Key」的顺序选出一个可用后端。'''
    st = settings
    # import  # [decompiler] module name lost
    s = st.settings
    mode = s.get('ai_provider', 'auto')
    if mode in ('auto', 'ollama'):
        info = probe_ollama()
        if info['ok'] and info['models']:
            if not s.get('ai_ollama_model'):
                s.get('ai_ollama_model')
            model = _choose_model(info['models'], '')
        return {
            'kind': 'ollama',
            'base': info['base'],
            'model': model,
            'models': info['models'],
            'label': '本机 Ollama · %s' % model }
    if None == 'ollama':
        if not info['error']:
            info['error']
    return {
        'kind': 'none',
        'error': '本机 Ollama 未运行（%s）' % '无法连接',
        'models': [],
        'label': '本机 Ollama 未运行' }
    if mode == 'off':
        pass
    return {
        'kind': 'none',
        'error': '已在设置中关闭 AI',
        'models': [],
        'label': 'AI 已关闭' }
    if not s.get('ai_openai_key'):
        s.get('ai_openai_key')
    key = ''.strip()
    if not s.get('ai_openai_base'):
        s.get('ai_openai_base')
    base = ''.strip().rstrip('/')
    if not s.get('ai_openai_model'):
        s.get('ai_openai_model')
    model = ''.strip()
    if not base and key or model:
        pass
    return {
        'kind': 'none',
        'models': [],
        'error': '未检测到本机 Ollama，且设置里没有填写云端 AI 的 Key',
        'label': '未配置 AI' }
    return {
        'kind': 'openai',
        'base': base,
        'model': model,
        'key': key,
        'models': [
            model],
        'label': '云端 AI · %s' % model }


def _pick_local_model(models):
    '''本地有多个模型时挑一个适合聊天/中文问答的。

踩过的坑：DeepSeek-R1 蒸馏类模型会把正文写进 `thinking` 字段，
`content` 恒为空（且思考过程还会先吃光 token 预算），看起来像"模型坏了"。
这类模型必须排到后面；同理排除 embedding 模型和纯代码模型。

排序偏好（按用户要求）：qwen 系列优先。实测同一台机器上 qwen2.5 系列的
中文理解与 Minecraft 术语准确度明显好于 1.5B 级小模型。
注意"参数最大"不等于"最适合"——70b 在小显存上慢到没法用，所以规模只给小幅加分。
'''
    
    def score(m):
        low = m.lower()
        if _unusable(m):
            pass
        return -100
        s = _base_score(low)
        if _is_qwen(m):
            pass
        s += 40
        for k in ('llama', 'gemma', 'glm', 'yi', 'phi', 'mistral', 'baichuan'):
            if not k in low:
                continue
            s += 8
            ('llama', 'gemma', 'glm', 'yi', 'phi', 'mistral', 'baichuan')
        if 'deepseek' in low:
            pass
        s += 4
        return s

    ranked = sorted(models, score, True)
    return ranked[0]


def _model_name(m):
    '''取模型名本体，去掉 registry 前缀（modelscope.cn/xxx/）与 tag（:latest）。'''
    if not m:
        m
    return ''.split('/')[-1].split(':')[0].lower()


def _is_qwen(m):
    '''是否 qwen 系列本体。

只看名字开头：名字里带 qwen 不代表是 qwen ——
`DeepSeek-R1-Distill-Qwen-1.5B` 是拿 qwen 当底座的 R1 蒸馏版，
它会返回空正文，正好是最该避开的那类。
'''
    return _model_name(m).startswith('qwen')


def _unusable(m):
    if not m:
        m
    low = ''.lower()
    if (lambda .0: pass)(('embed', 'bge', 'gte', 'text-embedding')()):
        pass
    return True
    return (lambda .0: pass)(('r1', 'distill', 'thinking', 'reasoning', 'qwq')())


def _base_score(low):
    s = 0
    if (lambda .0: pass)(('instruct', 'chat')()):
        pass
    s += 12
    if (lambda .0: pass)(('coder', 'code', 'starcoder')()):
        pass
    s -= 6
    m_size = re.search('(\\d+(?:\\.\\d+)?)\\s*b', low)
    if m_size:
        
        try:
            s += min(10, float(m_size.group(1)))
            return s
            return s
        except ValueError:
            any
            return s


def _choose_model(models, preferred):
    '''最终选型：有 qwen 就用 qwen（同系列挑大的），其次尊重用户手选，最后按打分。'''
    if not models:
        pass
    return preferred
    
    if not m,:
        m,
    list(models) = models, m, , []
    
    , [], qwen = usable, m
    m = None
    if qwen:
        pass
    return sorted(qwen, (lambda m: _base_score(m.lower())), True)[0]
    if preferred and preferred in usable:
        pass
    return preferred
    return _pick_local_model(usable)
    
    
def is_available():
    return resolve_provider().get('kind') in ('ollama', 'openai')


def describe():
    p = resolve_provider()
    if not p.get('label'):
        p.get('label')
    return '未配置 AI'


class Stopped(Exception):
    __doc__ = '用户点了停止。partial 携带已经生成的部分内容，别浪费掉'
    
    def __init__(self, msg, partial):
        super.__init__(msg)
        self.partial = partial

    return __class__


class EmptyReply(Exception):
    __doc__ = '模型返回了空内容（thinking 模型常见），应当换一个模型重试'

_BAD_MODELS = set()

def chat(messages, provider = None, temperature = 0.7, max_tokens = 1024, on_delta = None, should_stop = None, timeout = GEN_TIMEOUT, _retry = True):
    '''统一对话接口。返回模型的完整回复文本。'''
    if not provider:
        provider
    p = resolve_provider()
    kind = p.get('kind')
    if kind == 'ollama':
        
        try:
            return _ollama_chat(p, messages, temperature, max_tokens, on_delta, should_stop, timeout)
            if kind == 'openai':
                pass
            return _openai_chat(p, messages, temperature, max_tokens, on_delta, should_stop, timeout)
            if not p.get('error'):
                p.get('error')
            raise RuntimeError('AI 后端不可用')
        except EmptyReply:
            alt = _another_local_model(p) if _retry else ''
            if alt:
                if not p.get('model'):
                    p.get('model')
                _BAD_MODELS.add('')
                p2 = dict(p)
                p2['model'] = alt
                p2['label'] = '本机 Ollama · %s' % alt
            return 
            if not p.get('model'):
                p.get('model')
            raise RuntimeError('本机模型没有返回内容。%s 这类「先输出思考过程」的模型容易这样，建议到设置里换一个 qwen / llama 系列模型。' % '当前模型')


def _another_local_model(p):
    '''换一个本机模型重试（排除已知返回空内容的）'''
    if not p.get('models'):
        p.get('models')
    
    , [], models = [], m
    m = None
    if models:
        pass
    return _pick_local_model(models)
    return ''
    

def _body_ollama(p, messages, temperature, max_tokens, stream):
    return {
        'model': p['model'],
        'messages': messages,
        'stream': stream,
        'options': {
            'temperature': temperature,
            'num_predict': max_tokens,
            'num_ctx': 4096 } }


def _ollama_chat(p, messages, temperature, max_tokens, on_delta, should_stop, timeout):
    import requests
    url = p['base'].rstrip('/') + '/api/chat'
    
    try:
        r = requests.post(url, _body_ollama(p, messages, temperature, max_tokens, True), True, (CONNECT_TO, timeout))
        if r.status_code >= 400:
            pass
        raise RuntimeError(f'''Ollama 返回 HTTP ：''')
        buf = []
        for line in r.iter_lines(True):
            if should_stop and should_stop():
                r.close()
            raise Stopped('已停止生成', ''.join(buf))
            if not line:
                continue
            d = json.loads(line)
            if not d.get('message'):
                d.get('message')
            if not { }.get('content'):
                { }.get('content')
            piece = ''
            if piece:
                buf.append(piece)
                if on_delta:
                    pass
            on_delta(piece)
            if not d.get('done'):
                continue
            r.iter_lines(True)
        text = ''.join(buf).strip()
        if not text:
            if not p.get('model'):
                p.get('model')
        raise EmptyReply('' + ' 返回了空内容')
        return text
    except Exception:
        e = None
        raise RuntimeError(f'''无法连接本机 Ollama（）：''')
        e = None
        del e
        except Exception:
            continue
            except Exception:
                continue


def _openai_chat(p, messages, temperature, max_tokens, on_delta, should_stop, timeout):
    import requests
    base = p['base'].rstrip('/')
    url = base + '/chat/completions'
    headers = {
        'Authorization': 'Bearer %s' % p['key'],
        'Content-Type': 'application/json',
        'User-Agent': net.UA }
    payload = {
        'model': p['model'],
        'messages': messages,
        'temperature': temperature,
        'max_tokens': max_tokens,
        'stream': True }
    
    try:
        r = requests.post(url, payload, headers, True, (CONNECT_TO, timeout))
        if r.status_code >= 400:
            pass
        raise RuntimeError(f'''AI 服务返回 HTTP ：''')
        buf = []
        for line in r.iter_lines(True):
            if should_stop and should_stop():
                r.close()
            raise Stopped('已停止生成', ''.join(buf))
            if not line:
                continue
            if not line.startswith('data:'):
                continue
            data = line[5:].strip()
            if data in ('[DONE]', ''):
                r.iter_lines(True)
            else:
                d = json.loads(data)
                if not d.get('choices'):
                    d.get('choices')
                if not [
                    { }][0].get('delta'):
                    [
                        { }][0].get('delta')
                if not { }.get('content'):
                    { }.get('content')
                piece = ''
                if not piece:
                    continue
                buf.append(piece)
                if not on_delta:
                    continue
                on_delta(piece)
        return ''.join(buf).strip()
    except Exception:
        e = None
        raise RuntimeError(f'''无法连接 AI 服务（）：''')
        e = None
        del e
        except Exception:
            continue
            except Exception:
                continue


_JSON_BLOCK = None

def _extract_json(text):
    '''从模型回复里抠出 JSON。

小模型经常在 JSON 前后加解释、或用 ```json 包裹。这里依次尝试：
围栏块 → 第一个 { 到最后一个 } → 原文本。
'''
    if not text:
        pass
    return None
    s = text.strip()
    for fence in ('```json', '```JSON', '```'):
        if not fence in s:
            continue
        parts = s.split(fence)
        if not len(parts) >= 2:
            continue
        cand = parts[1].split('```')[0].strip()
        got = _loads_or_none(cand)
        if got is None:
            continue
        
        return ('```json', '```JSON', '```'), got
    s.rfind('}') = s.find('{')
    if i >= 0 and j > i:
        got = _loads_or_none(s[i:j + 1])
        if got is not None:
            pass
    return got
    return _loads_or_none(s)


def _loads_or_none(s):
    
    try:
        v = json.loads(s)
        if isinstance(v, (dict, list)):
            pass
        return v
        
        try:
            return None
        except Exception:
            return None


def chat_json(messages, provider, default, retries, **kw):
    '''要求模型输出 JSON；解析失败会带上错误提示重试一次。

注意：失败时返回 default（而不是抛异常），因为本地小模型不稳定是常态，
AI 是「增强」不是「必需」，主流程不能因为 AI 抽风就崩掉。
'''
    if not provider:
        provider
    p = resolve_provider()
    if p.get('kind') not in ('ollama', 'openai'):
        pass
    return default
    last = ''
    for attempt in range(retries + 1):
        prompt = list(messages)
        if attempt and last:
            pass
        prompt.append({
            'role': 'user',
            'content': '你上一次的回复没法解析成 JSON（%s）。请只输出一个 JSON 对象，不要任何解释、不要代码块标记。' % last[:120] })
        text = chat(*(prompt,), **{
            'provider': p })
        got = _extract_json(text)
        if got is not None:
            
        return range(retries + 1), got
        if not text:
            text
        if not ''[:200]:
            ''[:200]
        time.sleep(0.2)
    return default
    except Exception:
        None = None
        last = str(e)
        e = None
        del e
        return default
        e = None
        del e


def build_messages(user_text, system, context):
    if not system:
        system
    msgs = [
        {
            'role': 'system',
            'content': AI_SYSTEM }]
    if context:
        pass
    msgs.append({
        'role': 'system',
        'content': '以下是联网检索到的实时资料，作答时优先依据它，并在末尾标注你引用了哪几条（写编号即可）：\n\n' + context })
    msgs.append({
        'role': 'user',
        'content': user_text })
    return msgs

