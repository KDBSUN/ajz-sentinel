#!/usr/bin/env python3
# 聚合「数据上报」Issue 中的匿名检测 JSON，生成 community/leaderboard.json
# 仅接受脱敏 schema（ajz-board v1）：host 只能是域名、model 必填、total 0-100。
import json, os, re, sys, datetime
import urllib.request
from urllib.parse import quote

REPO = os.environ.get('GITHUB_REPOSITORY', '')
TOKEN = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN', '')
API = 'https://api.github.com'
LABEL = '数据上报'
MAX_PAGES = 5

def gh(path):
    req = urllib.request.Request(API + path, headers={
        'Authorization': 'Bearer ' + TOKEN,
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'ajz-sentinel-aggregator'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

def extract_jsons(body):
    out = []
    for m in re.finditer(r'```(?:json)?\s*(\{.*?\})\s*```', body or '', re.S):
        try:
            out.append(json.loads(m.group(1)))
        except Exception:
            pass
    if not out and body:
        m = re.search(r'\{[^{}]*"v"\s*:\s*1.*\}', body, re.S)
        if m:
            try:
                out.append(json.loads(m.group(0)))
            except Exception:
                pass
    return out

def valid(d):
    try:
        if d.get('v') != 1:
            return None
        host = str(d.get('host', '')).strip()[:100]
        if '/' in host or ' ' in host or '@' in host:
            return None
        model = str(d.get('model', '')).strip()[:80]
        if not model:
            return None
        total = float(d.get('total'))
        if not (0 <= total <= 100):
            return None
        per_dim = {}
        for k, v in (d.get('perDim') or {}).items():
            if isinstance(v, (int, float)) and 0 <= v <= 100:
                per_dim[str(k)[:20]] = float(v)
        return {'host': host, 'model': model, 'mode': str(d.get('mode', ''))[:20],
                'total': total, 'perDim': per_dim,
                'judged': int(d.get('judged', 0)), 'count': int(d.get('count', 0)),
                'ts': int(d.get('ts', 0))}
    except Exception:
        return None

def main():
    if not REPO or not TOKEN:
        print('missing GITHUB_REPOSITORY or GH_TOKEN')
        sys.exit(1)
    issues = []
    for page in range(1, MAX_PAGES + 1):
        batch = gh('/repos/%s/issues?labels=%s&state=all&per_page=100&page=%d'
                   % (REPO, quote(LABEL), page))
        if not batch:
            break
        issues += batch
        if len(batch) < 100:
            break
    entries = {}
    skipped = 0
    for it in issues:
        if it.get('state') == 'closed':
            continue
        for raw in extract_jsons(it.get('body')):
            d = valid(raw)
            if not d:
                skipped += 1
                continue
            key = d['host'] + '|' + d['model']
            e = entries.setdefault(key, {'host': d['host'], 'model': d['model'],
                                         'n': 0, 'sumTotal': 0.0, 'ts': 0, 'perDim': {}})
            e['n'] += 1
            e['sumTotal'] += d['total']
            e['ts'] = max(e['ts'], d['ts'])
            for k, v in d['perDim'].items():
                pd = e['perDim'].setdefault(k, [0.0, 0])
                pd[0] += v
                pd[1] += 1
    rows = []
    for e in entries.values():
        rows.append({'host': e['host'], 'model': e['model'], 'n': e['n'],
                     'avgTotal': round(e['sumTotal'] / e['n'], 1),
                     'perDim': {k: round(v[0] / v[1], 1) for k, v in e['perDim'].items()},
                     'ts': e['ts']})
    rows.sort(key=lambda r: -r['avgTotal'])
    out = {'schema': 'ajz-board-v1',
           'updated': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
           'entries': rows}
    os.makedirs('community', exist_ok=True)
    with open('community/leaderboard.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('aggregated %d entries from %d issues (skipped %d invalid payloads)'
          % (len(rows), len(issues), skipped))

if __name__ == '__main__':
    main()
