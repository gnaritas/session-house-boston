# Session House pitch: guards + asserts + window + send + read-back + registry append + lane.db event (abort-on-any-gate)
# Adapted from the proven copa-cafe / threemonkeys send_pitch.py (2026-11-22). Resume-safe: existing registry pitch row = skip.
import json, re, subprocess, sys, os, sqlite3, datetime, time
from zoneinfo import ZoneInfo

DRAFT = '/Users/rleon/sites/session-house-boston/PITCH-DRAFT.md'
REG = '/Users/rleon/.hermes/projects/websites/pitch_registry.jsonl'
LANEDB = '/Users/rleon/.hermes/projects/websites/lane.db'
ENVOUT = '/Users/rleon/sites/session-house-boston/send-envelope.json'
TO = 'info@sessionhouseboston.com'
SUBJ = 'Website demo for Session House'
TOKEN = 'session-house-boston-t1'
SLUG = 'session-house-boston'
CARD = 't_737649d7'
body = open(DRAFT, encoding='utf-8').read()
assert '\u2026' not in body, 'U+2026 mangled token in draft'

def norm(s): return re.sub(r'[^a-z0-9]', '', (s or '').lower())
rows = [json.loads(l) for l in open(REG) if l.strip()]
nto = norm(TO)

# 0) resume predicate
if any(r.get('type') == 'pitch' and r.get('slug') == SLUG for r in rows):
    sys.exit('SKIP: registry already has a pitch row for this slug — never re-send')

# 1) never-pitch-twice guards
email_hits = [r for r in rows if norm(r.get('email', '')) == nto]
nameq = norm('session house')
name_hits = [r for r in rows if any(nameq == norm(a) or nameq in norm(a) or norm(a) in nameq
              for a in ([r.get('business', '')] + list(r.get('name_aliases', []) or [])) if norm(a))]
print('GUARD email rows:', [(r.get('type'), r.get('slug'), r.get('email')) for r in email_hits])
print('GUARD name rows:', [(r.get('type'), r.get('slug'), r.get('business')) for r in name_hits])
pitched_emails = {norm(r['email']) for r in rows if r.get('type') == 'pitch' and r.get('email')}
blocking_names = [r for r in name_hits if r.get('type') in ('pitch', 'no', 'optout', 'has_site', 'sent')]
if any(norm(r.get('email', '')) in pitched_emails for r in email_hits) or blocking_names:
    sys.exit('ABORT: already pitched/known on this email-or-name key')

# 2) inbox cap (2 businesses max per inbox)
inbox_alias = 'sessionhouseboston'
n_same_inbox = sum(1 for r in rows if r.get('type') == 'pitch' and (r.get('alias') == inbox_alias or norm(r.get('email', '')) == nto))
print(f'inbox cap check ({inbox_alias}):', n_same_inbox, '(cap 2)')
assert n_same_inbox < 2, 'ABORT: inbox cap'

# 3) optout suppression (email is globally suppressed)
opt_emails = {norm(r.get('email', '')) for r in rows if r.get('type') == 'optout'}
assert nto not in opt_emails, 'ABORT: opted-out address'
try:
    sup = open('/Users/rleon/.hermes/projects/websites/optout_list.txt').read()
    assert nto not in norm(sup), 'ABORT: optout_list.txt'
except FileNotFoundError:
    pass

# 4) copy form asserts (proven formula; ABORT before send) — URLs derived from the draft itself
assert body.count('](http') == 2, f'links {body.count("](http")}'
assert body.count('<img') == 1, 'img count'
demo = re.search(r'\]\((https://session-house-boston-demo[^)]+)\)', body).group(1)
pay = re.search(r'\]\((https://buy\.stripe[^)]+)\)', body).group(1)
pixel = re.search(r'<img src="([^"]+)"', body)
for need in ('utm_medium=email', 'utm_campaign=websites', f'utm_content={TOKEN}'):
    assert need in demo, 'demo missing ' + need
    assert need in pay, 'pay missing ' + need
assert f'client_reference_id={TOKEN}' in pay, 'pay missing client_reference_id'
assert pixel and pixel.group(1) == f'https://session-house-boston-demo.up.railway.app/open?t={TOKEN}', 'pixel token'
t = re.sub(r'\*\*', '', body)
t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)
t = re.sub(r'<img[^>]*>', '', t)
lines = [l for l in t.splitlines() if l.strip()]
lines = [l for l in lines if not l.startswith('Hi ') and not l.startswith('— Jarvis')
         and not l.startswith('OnSmalltalk Media ·') and not l.startswith('<img')]
n = len(re.findall(r'\S+', ' '.join(lines)))
print(f'ASSERT core words: {n} (limit 110); links 2; utm+pixel token {TOKEN} OK')
assert n <= 110, f'ABORT words {n}'

# 4b) send window: 07:00-17:00 RECIPIENT local (Boston = ET/PT America/New_York)
now_et = datetime.datetime.now(ZoneInfo('America/New_York'))
if os.environ.get('DRY'):
    print(f'DRY: window check skipped-notice; ET now {now_et:%Y-%m-%d %H:%M}')
else:
    assert 7 <= now_et.hour < 17, f'ABORT send window: recipient-local {now_et:%H:%M} ET outside 07:00-17:00'
    assert now_et.weekday() < 5, 'ABORT send window: weekend'

# 5) ladder dates computed from send date (business days; US holidays shifted)
HOLIDAYS = {datetime.date(2026, 11, 26), datetime.date(2026, 11, 27), datetime.date(2026, 12, 25)}
def business_after(start, n):
    d = start
    while n > 0:
        d += datetime.timedelta(days=1)
        if d.weekday() < 5 and d not in HOLIDAYS:
            n -= 1
    return d
send_date = now_et.date()
t2 = business_after(send_date, 5); t3 = business_after(send_date, 10); t4 = business_after(send_date, 15)
ladder = (f't2 {t2.isoformat()} / t3 {t3.isoformat()} / t4 {t4.isoformat()} '
          f'(weekday ladder, US-holiday shift); teardown recheck >= {(t4 + datetime.timedelta(days=5)).isoformat()}')
print('LADDER:', ladder)

if os.environ.get('DRY'):
    sys.exit(f'GUARDS+ASSERTS PASS (dry, not sent); words={n}')

# 6) send (body on stdin, --json envelope; message_id from the envelope JSON)
res = subprocess.run(['email', 'send', '--account', 'jarvis', '--as', 'websites',
                      '--to', TO, '--subject', SUBJ, '--json'],
                     input=body.encode(), capture_output=True, timeout=120)
try:
    env = json.loads(res.stdout.decode())
except Exception:
    open(ENVOUT, 'w').write(res.stdout.decode() + '\n---STDERR---\n' + res.stderr.decode())
    sys.exit('ABORT: unparseable send envelope — do NOT resend, read back Sent Mail first')
json.dump({'ok': env.get('ok'), 'env': env}, open(ENVOUT, 'w'))
ok = env.get('ok')
mid = (env.get('data') or {}).get('message_id') or (env.get('data') or {}).get('msg_id')
print('SEND ok=', ok, 'msg:', mid if ok else env)
if not ok or not mid:
    sys.exit('ABORT send — read back [Gmail]/Sent Mail before any retry')

# 7) sent read-back (raw imaplib): Message-ID equality + identity header pair
conf = {}
for l in open(os.path.expanduser('~/.hermes/config/jarvis-email.conf')):
    if '=' in l: k, v = l.split('=', 1); conf[k.strip()] = v.strip()
    elif ':' in l: k, v = l.split(':', 1); conf[k.strip()] = v.strip()
M = imaplib.IMAP4_SSL(conf.get('IMAP_SERVER', 'imap.gmail.com'))
M.login(conf['EMAIL'], conf['APP_PASSWORD'])
M.select('"[Gmail]/Sent Mail"')
typ, m = M.uid('search', None, 'SUBJECT', f'"{SUBJ}"')
ids = [i.decode() for i in m[0].split()]
hit = None
for uid in ids[-3:]:
    typ, d = M.uid('fetch', uid, '(BODY.PEEK[HEADER])')
    hdr = d[0][1].decode(errors='replace')
    if mid in hdr:
        orp = bool(re.search(r'X-Google-Original-From:[^>]*jarvis\+websites', hdr, re.I))
        rto = bool(re.search(r'Reply-To:\s*\S*jarvis\+websites', hdr, re.I))
        hit = {'uid': uid, 'ogf': orp, 'reply_to': rto}
        break
M.logout()
print('READBACK:', hit)
assert hit and hit['ogf'] and hit['reply_to'], 'ABORT READBACK — mail out but unproven; append registry only after proof, never re-send'

# 8) registry append AT SEND (type IN the dict), then recount-verify
row = {
    'type': 'pitch', 'date': send_date.isoformat(),
    'ts': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
    'slug': SLUG, 'business': 'Session House (Dorchester Boston MA)',
    'name_aliases': ['Session House', 'Session House Boston', 'session-house-boston',
                     'Session House Dorchester', 'sessionhouse', 'Session House Adams Village'],
    'email': TO, 'alias': inbox_alias, 'card': CARD,
    'msg_id': mid, 'preview': 'https://session-house-boston-demo.up.railway.app',
    'subject': SUBJ, 'subject_arm': 'v7', 'cohort': 'A',
    'shot': False, 'pixel': True, 'utm_content': TOKEN,
    'followup_due': t2.isoformat(), 'ladder': ladder,
    'feed_id': 'press-dorchester', 'shop_id': 'session-house-dorchester-boston',
    'note': ('owner email self-published on the shop\'s own FB Page intro block (found 2026-11-22 logged-out at card creation); '
             'press: whatnow.com feature + dotnews 2026-09-24 licensing + boston.com 11-03 "Opens: Mid-November"; '
             'no-site evidence: brand-SERP press-only, sessionhouseboston.com = Squarespace private placeholder (RDAP 2026-10-14, Wayback contentless), '
             'GBP place card unresolved (address embed returns former tenant Scobie\'s); '
             'founder bundle T1 $249+$39/mo 31d trial; v7 subject arm; 10-page site, _verify PASS, curl 14/14, Brevo relay proven, render-sweep PASS '
             '(OOPIF-capture limitation documented: harness renders zero cross-origin iframes, control-proven; map DOM-verified)'),
}
with open(REG, 'a') as f:
    f.write(json.dumps(row, ensure_ascii=False) + '\n')
pitches = 0; mine = 0; line_no = 0
for i, l in enumerate(open(REG), 1):
    try: d = json.loads(l)
    except Exception: continue
    if d.get('type') == 'pitch':
        pitches += 1
        if d.get('slug') == SLUG: mine += 1
    line_no = i
print(f'RECOUNT after append: total pitch rows={pitches}, this slug={mine}, registry lines={line_no}')
assert mine == 1, 'ABORT recount: this slug must appear exactly once'

# 9) lane.db events mirror row (real schema: line=registry line pk)
db = sqlite3.connect(LANEDB)
db.execute("""INSERT INTO events (line,type,feed_id,shop_id,slug,business,email,msg_id,followup_due,date_txt,ts,note)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
 (line_no, 'pitch', 'press-dorchester', 'session-house-dorchester-boston', SLUG,
  'Session House (Dorchester Boston MA)', TO, mid, t2.isoformat(), send_date.isoformat(),
  int(time.time()),
  'pitched via websites desk; demo session-house-boston-demo.up.railway.app; founder bundle T1 $249+$39/mo 31d trial; v7 subject arm; card t_737649d7; read-back proof uid=' + hit['uid']))
db.commit()
print('EVENT_ROW_OK', db.execute("SELECT line,type,slug,msg_id FROM events WHERE slug=?", (SLUG,)).fetchall())
print(f'PITCHED {SLUG} {send_date} | msg {mid} | sent uid {hit["uid"]} | ladder t2={t2} t3={t3} t4={t4}')
print('ALL_DONE', mid)
