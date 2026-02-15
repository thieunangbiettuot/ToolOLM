#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║               OLM MASTER PRO - ALL IN ONE                    ║
║                    Created by: Tuấn Anh                      ║
╚══════════════════════════════════════════════════════════════╝
"""

import os, sys, time, json, requests, hashlib, base64, re, random, socket, uuid
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path

# ==================== CONFIG ====================
API_TOKEN = "698b226d9150d31d216157a5"
URL_VIP = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://olm.vn',
    'referer': 'https://olm.vn/'
}

# ==================== COLORS ====================
class C:
    R = '\033[91m'
    G = '\033[92m'
    Y = '\033[93m'
    B = '\033[94m'
    M = '\033[95m'
    C = '\033[96m'
    W = '\033[97m'
    BOLD = '\033[1m'
    E = '\033[0m'

I = {'s': '✅', 'e': '❌', 'w': '⚠️', 'i': 'ℹ️', 'd': '💎', 'crown': '👑'}

# ==================== FILE PATHS ====================
def get_data_dir():
    import platform
    sp = platform.system().lower()
    if 'windows' in sp:
        d = Path(os.getenv('LOCALAPPDATA')) / 'Microsoft' / 'Windows' / 'INetCache' / 'IE'
    elif 'darwin' in sp:
        d = Path.home() / 'Library' / 'Application Support' / 'com.apple.Safari'
    elif 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ:
        d = Path.home() / '.cache' / 'google-chrome'
    else:
        d = Path.home() / '.cache' / 'mozilla' / 'firefox'
    d.mkdir(parents=True, exist_ok=True)
    return str(d)

DATA = get_data_dir()
HASH = hashlib.md5(f"{socket.gethostname()}{uuid.getnode()}".encode()).hexdigest()[:16]
LIC = os.path.join(DATA, f'.{HASH}sc')
ACC = os.path.join(DATA, f'.{HASH}ac')
KEY = b'OLM_MASTER_PRO_2026_SECRET_KEY_42'

# ==================== ENCRYPTION ====================
def enc(data):
    js = json.dumps(data)
    bd = js.encode()
    xd = bytearray(b ^ KEY[i % len(KEY)] for i, b in enumerate(bd))
    b85 = base64.b85encode(bytes(xd)).decode()
    chk = hashlib.sha256(b85.encode()).hexdigest()[:12]
    np = hashlib.md5(os.urandom(16)).hexdigest()[:8]
    return f"{np}{chk}{b85}{np[::-1]}"

def dec(es):
    try:
        p = es[:8]
        s = es[-8:]
        if s != p[::-1]:
            return None
        c = es[8:-8]
        chk, b85 = c[:12], c[12:]
        if hashlib.sha256(b85.encode()).hexdigest()[:12] != chk:
            return None
        xd = base64.b85decode(b85)
        bd = bytes(b ^ KEY[i % len(KEY)] for i, b in enumerate(xd))
        return json.loads(bd.decode())
    except:
        return None

def save_f(fn, data):
    with open(fn, 'w') as f:
        f.write(enc(data))

def load_f(fn):
    if os.path.exists(fn):
        with open(fn, 'r') as f:
            return dec(f.read())
    return None

# ==================== UI ====================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print(f"{C.B}{C.BOLD}╔══════════════════════════════════════════════════════════════╗{C.E}")
    print(f"{C.B}{C.BOLD}║               OLM MASTER PRO - ALL IN ONE                    ║{C.E}")
    print(f"{C.B}{C.BOLD}║                  Created by: Tuấn Anh                        ║{C.E}")
    print(f"{C.B}{C.BOLD}╚══════════════════════════════════════════════════════════════╝{C.E}\n")

def msg(t, ic='i', col=C.W):
    print(f"{I.get(ic, '•')} {col}{t}{C.E}")

def inp(p):
    return input(f"{C.Y}{p}{C.E}").strip()

# ==================== LICENSE ====================
def vfy(d):
    if not d:
        return False
    sig = hashlib.sha256(f"{d.get('mode', '')}{d.get('expire', '')}{d.get('ip', '')}".encode()).hexdigest()
    return d.get('sig') == sig

def get_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text
    except:
        return 'unknown'

def load_lic():
    d = load_f(LIC)
    if not d or not vfy(d):
        if os.path.exists(LIC):
            os.remove(LIC)
        return None
    try:
        exp = datetime.strptime(d['expire'], "%d/%m/%Y").date()
        if exp < datetime.now().date():
            return None
    except:
        return None
    if d.get('mode') == 'FREE':
        if d.get('ip') != get_ip():
            return None
        if d.get('remain', 0) <= 0:
            return None
    return d

def save_lic(mode, remain, expire, ip):
    d = {'mode': mode, 'remain': remain, 'expire': expire, 'ip': ip}
    d['sig'] = hashlib.sha256(f"{mode}{expire}{ip}".encode()).hexdigest()
    save_f(LIC, d)

def upd_lic(nr):
    d = load_lic()
    if d and d.get('mode') == 'FREE':
        d['remain'] = nr
        save_f(LIC, d)

def deduct():
    l = load_lic()
    if not l:
        return False
    if l.get('mode') == 'VIP':
        return True
    r = l.get('remain', 0)
    if r > 0:
        upd_lic(r - 1)
        if r - 1 > 0:
            print(f"\n{C.G}{I['d']} Còn: {r-1} lượt{C.E}")
        else:
            print(f"\n{C.R}⛔ HẾT LƯỢT{C.E}")
        return True
    return False

# ==================== ACCOUNT ====================
def load_acc():
    return load_f(ACC) or {}

def save_acc(name, user, pwd):
    accs = load_acc()
    accs[name] = {'username': user, 'password': pwd, 'saved_at': datetime.now().strftime("%d/%m/%Y %H:%M")}
    save_f(ACC, accs)

def select_acc():
    accs = load_acc()
    if not accs:
        return None, None
    print(f"{C.C}╔{'═' * 60}╗{C.E}")
    print(f"{C.C}║{C.BOLD}{' TÀI KHOẢN ĐÃ LƯU '.center(60)}{C.E}{C.C}║{C.E}")
    print(f"{C.C}╚{'═' * 60}╝{C.E}")
    al = list(accs.items())
    for i, (n, d) in enumerate(al, 1):
        print(f"{C.Y}[{i}]{C.E} {n} ({d.get('saved_at', '')})")
    print(f"{C.Y}[0]{C.E} Đăng nhập mới")
    ch = inp("Chọn: ")
    if ch == '0':
        return None, None
    try:
        idx = int(ch) - 1
        if 0 <= idx < len(al):
            return al[idx][1]['username'], al[idx][1]['password']
    except:
        pass
    return None, None

# ==================== CHECK VIP ====================
def check_vip(user):
    try:
        r = requests.get(URL_VIP, timeout=5)
        if r.status_code == 200:
            vips = [l.strip().lower() for l in r.text.splitlines() if l.strip() and not l.startswith('#')]
            return user.lower() in vips
    except:
        pass
    return False

# ==================== CREATE SHORT LINK ====================
def short_link(url):
    try:
        enc_url = requests.utils.quote(url)
        api = f"https://link4m.co/api-shorten/v2?api={API_TOKEN}&url={enc_url}"
        r = requests.get(api, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "success":
                return data.get("shortenedUrl")
    except:
        pass
    return url

# ==================== GENERATE KEY ====================
def gen_key():
    now = datetime.now()
    u = f"{HASH}{now.timestamp()}{random.randint(1000, 9999)}"
    h = hashlib.sha256(u.encode()).hexdigest()
    return f"OLM-{now:%d%m}-{h[:4].upper()}-{h[4:8].upper()}"

# ==================== GET FREE KEY ====================
def get_free_key():
    blog = "https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html"
    
    for _ in range(3):
        k = gen_key()
        url = f"{blog}?ma={k}"
        
        msg("Đang tạo link...", 'i', C.C)
        short = short_link(url)
        
        print(f"\n{C.G}╔{'═' * 60}╗{C.E}")
        print(f"{C.G}║{C.BOLD}{' VƯỢT LINK LẤY KEY '.center(60)}{C.E}{C.G}║{C.E}")
        print(f"{C.G}╠{'═' * 60}╣{C.E}")
        print(f"{C.G}║{C.E} {C.C}Link: {C.Y}{short[:50]}{C.E}")
        print(f"{C.G}║{C.E} {C.W}1. Vượt link trên{C.E}")
        print(f"{C.G}║{C.E} {C.W}2. Nhập key bên dưới{C.E}")
        print(f"{C.G}║{C.E} {C.Y}   (r = tạo link mới){C.E}")
        print(f"{C.G}╚{'═' * 60}╝{C.E}\n")
        
        for i in range(3):
            ki = inp("🔑 Key (r=mới): ")
            
            if ki.lower() == 'r':
                break
            
            if ki == k:
                exp = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
                ip = get_ip()
                save_lic('FREE', 4, exp, ip)
                msg("✓ Key hợp lệ! 4 lượt đã kích hoạt", 's', C.G)
                time.sleep(1)
                return True
            
            if i < 2:
                msg(f"✗ Sai key! Còn {2-i} lần", 'w', C.Y)
                time.sleep(1)
        
        if ki.lower() == 'r':
            continue
    
    msg("Hết lượt thử", 'e', C.R)
    return False

# ==================== LOGIN ====================
def login():
    banner()
    
    su, sp = select_acc()
    use_saved = False
    
    if su and sp:
        use_saved = inp("Dùng tài khoản đã lưu? (y/n): ").lower() == 'y'
    
    if use_saved:
        user, pwd = su, sp
    else:
        user = inp("👤 Username: ")
        pwd = inp("🔑 Password: ")
    
    if not user or not pwd:
        msg("Thông tin rỗng!", 'e', C.R)
        time.sleep(2)
        return None, None, None, False
    
    msg("Đang đăng nhập...", 'i', C.C)
    
    try:
        s = requests.Session()
        s.headers.update(HEADERS)
        
        s.get("https://olm.vn/dangnhap")
        csrf = s.cookies.get('XSRF-TOKEN')
        
        pl = {
            '_token': csrf, 'username': user, 'password': pwd,
            'remember': 'true', 'device_id': '0b48f4d6204591f83dc40b07f07af7d4', 'platform': 'web'
        }
        
        h = HEADERS.copy()
        h['x-csrf-token'] = csrf
        s.post("https://olm.vn/post-login", data=pl, headers=h)
        
        cr = s.get("https://olm.vn/thong-tin-tai-khoan/info")
        m = re.search(r'name="name".*?value="(.*?)"', cr.text)
        
        if m and m.group(1).strip():
            un = m.group(1).strip()
            
            uid = None
            for cn, cv in s.cookies.get_dict().items():
                if 'remember_web' in cn and '%7C' in cv:
                    pts = cv.split('%7C')
                    if pts and pts[0].isdigit():
                        uid = pts[0]
                        break
            
            if not uid:
                ids = re.findall(r'\b\d{10,}\b', cr.text)
                uid = ids[0] if ids else user
            
            vip = check_vip(user)
            
            msg(f"✓ Đăng nhập: {un}", 's', C.G)
            
            if vip:
                msg("VIP Unlimited", 'crown', C.M)
            else:
                msg("FREE Account", 'i', C.Y)
            
            if not use_saved:
                if inp("Lưu tài khoản? (y/n): ").lower() == 'y':
                    save_acc(un, user, pwd)
                    msg("✓ Đã lưu", 's', C.G)
            
            time.sleep(1)
            return s, uid, un, vip
        
        else:
            msg("Sai username/password", 'e', C.R)
            time.sleep(2)
            return None, None, None, False
    
    except Exception as e:
        msg(f"Lỗi: {str(e)}", 'e', C.R)
        time.sleep(2)
        return None, None, None, False

# ==================== GET ASSIGNMENTS ====================
def get_assignments(s, pages=3):
    msg(f"Quét {pages} trang...", 'i', C.C)
    asn = []
    seen = set()
    
    for p in range(1, pages + 1):
        url = f"https://olm.vn/lop-hoc-cua-toi/page-{p}?action=login" if p > 1 else "https://olm.vn/lop-hoc-cua-toi?action=login"
        
        try:
            r = s.get(url, headers=HEADERS, timeout=10)
            if r.status_code != 200:
                continue
            
            soup = BeautifulSoup(r.text, 'html.parser')
            rows = soup.find_all('tr', class_='my-gived-courseware-item')
            
            pc = 0
            for row in rows:
                lts = row.find_all('a', class_='olm-text-link')
                if not lts:
                    continue
                
                ml = lts[0]
                href = ml.get('href')
                lt = ml.get_text(strip=True)
                
                if href and ('(Toán' in lt or '(Ngữ văn' in lt):
                    continue
                
                if not href:
                    continue
                
                tds = row.find_all('td')
                if len(tds) < 2:
                    continue
                
                lr = tds[1].get_text(strip=True)
                
                is_v = "[Video]" in lr
                is_l = "[Lý thuyết]" in lr
                is_k = "[Kiểm tra]" in lr
                is_t = "[Tự luận]" in lr
                
                if is_k or is_t:
                    continue
                
                sp = False
                sts = ml.find_all('span', class_='message-static-item')
                
                if not sts:
                    sts = row.find_all('span', class_='message-static-item')
                
                if not sts:
                    sp = True
                else:
                    for span in sts:
                        st = span.get_text(strip=True).lower()
                        if "chưa" in st or "làm tiếp" in st:
                            sp = True
                            break
                        elif "điểm" in st or "đã xem" in st:
                            sp = False
                            break
                
                if sp and href not in seen:
                    seen.add(href)
                    fu = 'https://olm.vn' + href if not href.startswith('http') else href
                    
                    asn.append({
                        'title': re.sub(r'\([^)]*\)', '', lt).strip()[:50],
                        'type': lr.replace('[', '').replace(']', '').strip()[:15],
                        'url': fu,
                        'is_video': is_v,
                        'is_ly_thuyet': is_l,
                        'is_bai_tap': not (is_v or is_l)
                    })
                    pc += 1
            
            if pc > 0:
                print(f"{C.G}  Trang {p}: {pc} bài{C.E}")
        
        except:
            print(f"{C.R}  Lỗi trang {p}{C.E}")
            continue
    
    if asn:
        msg(f"Tìm thấy {len(asn)} bài", 's', C.G)
    else:
        msg("Không tìm thấy bài", 'w', C.Y)
    return asn

def disp_asn(asn):
    if not asn:
        return
    
    print(f"\n{C.M}╔{'═' * 60}╗{C.E}")
    print(f"{C.M}║{C.BOLD}{'DANH SÁCH BÀI TẬP'.center(60)}{C.E}{C.M}║{C.E}")
    print(f"{C.M}╠{'═' * 60}╣{C.E}")
    
    for i, it in enumerate(asn, 1):
        t = it['title'] if len(it['title']) <= 35 else it['title'][:32] + "..."
        
        if it['is_video']:
            ic, cl = '🎥', C.B
        elif it['is_ly_thuyet']:
            ic, cl = '📖', C.C
        else:
            ic, cl = '📝', C.G
        
        ln = f"{i:2}. {ic} {cl}{it['type']:<12}{C.E} {C.W}{t}{C.E}"
        print(f"{C.M}║{C.E} {ln:<54} {C.M}║{C.E}")
    
    print(f"{C.M}╚{'═' * 60}╝{C.E}\n")

# ==================== EXTRACT QUIZ ====================
def extract_quiz(s, url, is_v=False):
    try:
        r = s.get(url, timeout=10)
        h = r.text
        
        ql = None
        for pat in [
            r'quiz_list\s*[:=]\s*["\'](\d{6,}(?:,\d{6,})*)["\']',
            r'\b\d{9,}(?:,\d{9,})+\b',
            r'"quiz_list"\s*:\s*"(\d+(?:,\d+)*)"'
        ]:
            m = re.search(pat, h)
            if m:
                ql = m.group(1) if 'quiz_list' in pat else m.group(0)
                break
        
        ic = None
        for pat in [r'id_courseware\s*[:=]\s*["\']?(\d+)["\']?', r'data-courseware\s*=\s*["\'](\d+)["\']']:
            m = re.search(pat, h)
            if m:
                ic = m.group(1)
                break
        
        icat = None
        m = re.search(r'-(\d+)(?:\?|$)', url)
        if m:
            icat = m.group(1)
        
        if not ql:
            return ("", 0, ic, icat) if is_v else (None, 0, ic, icat)
        
        tq = len([q.strip() for q in ql.split(',') if q.strip()])
        return ql, tq, ic, icat
    except:
        return None, 0, None, None

# ==================== CREATE LOG ====================
def create_log(tq, ts):
    cr = round((ts / 100) * tq) if ts not in [0, 100] else (tq if ts == 100 else 0)
    cr = max(0, min(tq, cr))
    
    res = [1] * cr + [0] * (tq - cr)
    random.shuffle(res)
    
    dl, tt = [], 0
    for i, ic in enumerate(res):
        tsp = random.randint(10, 30) + (i % 5)
        tt += tsp
        ord = [0, 1, 2, 3]
        random.shuffle(ord)
        
        dl.append({
            "q_params": json.dumps([{"js": "", "order": ord}]),
            "a_params": json.dumps([f'["{0 if ic else random.randint(1, 3)}"]']),
            "result": ic,
            "correct": ic,
            "wrong": 0 if ic else 1,
            "a_index": i,
            "time_spent": tsp
        })
    
    return dl, tt, cr

# ==================== TRY VIDEO ====================
def try_vid(s, uid, a, ql, ic, icat):
    try:
        csrf = s.cookies.get('XSRF-TOKEN')
        if not csrf:
            r = s.get(a['url'], timeout=10)
            m = re.search(r'<meta name="csrf-token" content="([^"]+)"', r.text)
            csrf = m.group(1) if m else ""
        
        dl = [{
            "answer": '["0"]', "params": '{"js":""}', "result": [1],
            "wrong_skill": [], "correct_skill": [], "type": [11],
            "id": f"vid{random.randint(100000, 999999)}", "marker": 1
        }]
        
        pl = {
            '_token': csrf, 'id_user': uid, 'id_cate': icat or '0',
            'id_grade': '10', 'id_courseware': ic or '0',
            'time_spent': str(random.randint(300, 900)),
            'score': '100', 'data_log': json.dumps(dl, separators=(',', ':')),
            'date_end': str(int(time.time())), 'ended': '1', 'cv_q': '1'
        }
        
        if ql:
            pl['quiz_list'] = ql
        
        h = HEADERS.copy()
        h['x-csrf-token'] = csrf
        
        r = s.post('https://olm.vn/course/teacher-static', data=pl, headers=h, timeout=10)
        return r.status_code in [200, 403]
    except:
        return False

# ==================== SUBMIT ====================
def submit(s, uid, a, ts):
    print(f"\n{C.C}{'─' * 60}{C.E}")
    print(f"{C.W}📝 {a['title'][:45]}{C.E}")
    
    if a['is_video']:
        print(f"{C.B}🎥 Video{C.E}")
    elif a['is_ly_thuyet']:
        print(f"{C.C}📖 Lý thuyết{C.E}")
    else:
        print(f"{C.G}📝 Bài tập{C.E}")
    
    try:
        time.sleep(0.5)
        
        ql, tq, ic, icat = extract_quiz(s, a['url'], a['is_video'])
        
        if a['is_video']:
            ok = try_vid(s, uid, a, ql, ic, icat)
            if ok:
                print(f"{C.G}✓ Thành công!{C.E}")
            else:
                print(f"{C.R}✗ Thất bại{C.E}")
            return ok
        
        if not ql or tq == 0:
            print(f"{C.R}✗ Không lấy được quiz{C.E}")
            return False
        
        dl, tt, cr = create_log(tq, ts)
        
        csrf = s.cookies.get('XSRF-TOKEN')
        if not csrf:
            r = s.get(a['url'], timeout=10)
            m = re.search(r'<meta name="csrf-token" content="([^"]+)"', r.text)
            csrf = m.group(1) if m else ""
        
        ct = int(time.time())
        
        pl = {
            '_token': csrf, 'id_user': uid, 'id_cate': icat or '0',
            'id_grade': '10', 'id_courseware': ic or '0', 'id_group': '6148789559',
            'id_school': '0', 'time_init': str(ct - tt if tt > 0 else ct - 600),
            'name_user': '', 'type_vip': '0', 'time_spent': str(tt),
            'data_log': json.dumps(dl, separators=(',', ':')), 'score': str(ts),
            'answered': str(tq), 'correct': str(cr), 'count_problems': str(tq),
            'missed': str(tq - cr), 'time_stored': str(ct), 'date_end': str(ct),
            'ended': '1', 'save_star': '0', 'cv_q': '1', 'quiz_list': ql or '',
            'choose_log': json.dumps(dl, separators=(',', ':')),
            'user_ans': json.dumps(["0"] * tq), 'list_quiz': ql or '',
            'list_ans': ','.join(["0"] * tq), 'result': '[]', 'ans': '[]'
        }
        
        h = HEADERS.copy()
        h['x-csrf-token'] = csrf
        
        r = s.post('https://olm.vn/course/teacher-static', data=pl, headers=h, timeout=15)
        
        if r.status_code == 200:
            print(f"{C.G}✓ Thành công!{C.E}")
            return True
        elif r.status_code == 403:
            print(f"{C.Y}⚠ Đã nộp trước{C.E}")
            return True
        else:
            print(f"{C.R}✗ Lỗi {r.status_code}{C.E}")
            return False
    except Exception as e:
        print(f"{C.R}✗ Lỗi: {str(e)}{C.E}")
        return False

# ==================== SOLVE SPECIFIC ====================
def solve_spec(s, uid):
    banner()
    
    pgs = inp("Số trang (3): ")
    pgs = 3 if not pgs.isdigit() else min(int(pgs), 10)
    
    asn = get_assignments(s, pgs)
    if not asn:
        input(f"\n{C.Y}Enter...{C.E}")
        return
    
    disp_asn(asn)
    
    print(f"{C.C}Chọn:{C.E} 0=tất cả, 1,3,5=nhiều, 1=1 bài\n")
    sel = inp("➤ Chọn: ")
    
    seld = []
    if sel == '0':
        seld = asn
    elif ',' in sel:
        try:
            ids = [int(x.strip()) - 1 for x in sel.split(',')]
            seld = [asn[i] for i in ids if 0 <= i < len(asn)]
        except:
            msg("Định dạng sai", 'e', C.R)
            input(f"\n{C.Y}Enter...{C.E}")
            return
    else:
        try:
            idx = int(sel) - 1
            if 0 <= idx < len(asn):
                seld = [asn[idx]]
        except:
            msg("Số sai", 'e', C.R)
            input(f"\n{C.Y}Enter...{C.E}")
            return
    
    if not seld:
        msg("Không có bài", 'e', C.R)
        input(f"\n{C.Y}Enter...{C.E}")
        return
    
    print(f"\n{C.C}⭐ ĐIỂM:{C.E} 1=100, 2=Tùy chọn\n")
    ts = 100
    if inp("➤ Chọn: ") == '2':
        try:
            ts = max(0, min(100, int(inp("Điểm (0-100): "))))
        except:
            ts = 100
    
    print(f"\n{C.C}Số bài: {len(seld)}, Điểm: {ts}{C.E}\n")
    
    if inp("Xác nhận? (y/n): ").lower() != 'y':
        msg("Hủy", 'i', C.C)
        input(f"\n{C.Y}Enter...{C.E}")
        return
    
    sc, tc = 0, len(seld)
    
    print(f"\n{C.G}{'═' * 60}{C.E}")
    print(f"{C.G}{C.BOLD}BẮT ĐẦU XỬ LÝ{C.E}")
    print(f"{C.G}{'═' * 60}{C.E}")
    
    for i, a in enumerate(seld, 1):
        print(f"\n{C.Y}[{i}/{tc}]{C.E}")
        
        l = load_lic()
        if not l or (l.get('mode') == 'FREE' and l.get('remain', 0) <= 0):
            msg("HẾT LƯỢT", 'e', C.R)
            break
        
        ok = submit(s, uid, a, ts)
        
        if ok:
            sc += 1
            deduct()
        else:
            if a['is_ly_thuyet']:
                print(f"{C.Y}⚠ Lý thuyết vẫn trừ{C.E}")
                deduct()
        
        if i < tc:
            time.sleep(random.randint(2, 4))
    
    print(f"\n{C.G}{'═' * 60}{C.E}")
    print(f"{C.G}✓ Hoàn thành: {sc}/{tc}{C.E}")
    print(f"{C.G}{'═' * 60}{C.E}")
    
    input(f"\n{C.Y}Enter...{C.E}")

# ==================== SOLVE FROM LINK ====================
def solve_link(s, uid):
    banner()
    
    print(f"{C.C}╔{'═' * 60}╗{C.E}")
    print(f"{C.C}║{C.BOLD}{'GIẢI TỪ LINK'.center(60)}{C.E}{C.C}║{C.E}")
    print(f"{C.C}╚{'═' * 60}╝{C.E}\n")
    
    url = inp("🔗 Link: ")
    
    if not url.startswith('https://olm.vn/'):
        msg("Link không hợp lệ", 'e', C.R)
        input(f"\n{C.Y}Enter...{C.E}")
        return
    
    try:
        r = s.get(url, timeout=10)
        is_v = 'video' in url.lower() or '[Video]' in r.text
        is_l = 'ly-thuyet' in url.lower() or '[Lý thuyết]' in r.text
        
        a = {
            'title': "Bài từ link",
            'type': "Video" if is_v else ("Lý thuyết" if is_l else "Bài tập"),
            'url': url,
            'is_video': is_v,
            'is_ly_thuyet': is_l,
            'is_bai_tap': not (is_v or is_l)
        }
        
        ts = 100
        if not is_v:
            print(f"\n{C.C}⭐ ĐIỂM:{C.E} 1=100, 2=Tùy chọn\n")
            if inp("➤ Chọn: ") == '2':
                try:
                    ts = max(0, min(100, int(inp("Điểm (0-100): "))))
                except:
                    ts = 100
        
        print(f"\n{C.C}Loại: {a['type']}, Điểm: {ts}{C.E}\n")
        
        if inp("Xác nhận? (y/n): ").lower() == 'y':
            l = load_lic()
            if not l or (l.get('mode') == 'FREE' and l.get('remain', 0) <= 0):
                msg("HẾT LƯỢT", 'e', C.R)
                input(f"\n{C.Y}Enter...{C.E}")
                return
            
            ok = submit(s, uid, a, ts)
            
            if ok:
                deduct()
            else:
                if a['is_ly_thuyet']:
                    print(f"{C.Y}⚠ Lý thuyết vẫn trừ{C.E}")
                    deduct()
            
            input(f"\n{C.Y}Enter...{C.E}")
        else:
            msg("Hủy", 'i', C.C)
            input(f"\n{C.Y}Enter...{C.E}")
    
    except Exception as e:
        msg(f"Lỗi: {str(e)}", 'e', C.R)
        input(f"\n{C.Y}Enter...{C.E}")

# ==================== MENU ====================
def menu(s, uid, un):
    while True:
        banner()
        
        print(f"{C.W}👤 {un}{C.E}")
        
        l = load_lic()
        if l:
            m = l.get('mode', 'FREE')
            if m == 'VIP':
                print(f"{C.G}⭐ VIP - UNLIMITED{C.E}")
            else:
                r = l.get('remain', 0)
                if r > 0:
                    print(f"{C.Y}💎 FREE - {r} lượt{C.E}")
                else:
                    print(f"{C.R}⛔ HẾT LƯỢT{C.E}")
        else:
            print(f"{C.R}⛔ Không có license{C.E}")
        
        print(f"\n{C.C}╔{'═' * 60}╗{C.E}")
        print(f"{C.C}║{C.BOLD}{'MENU'.center(60)}{C.E}{C.C}║{C.E}")
        print(f"{C.C}╠{'═' * 60}╣{C.E}")
        print(f"{C.C}║{C.E}  {C.Y}[1]{C.E} 📝 Giải bài cụ thể{' ' * 38} {C.C}║{C.E}")
        print(f"{C.C}║{C.E}  {C.Y}[2]{C.E} 🔗 Giải từ link{' ' * 41} {C.C}║{C.E}")
        print(f"{C.C}║{C.E}  {C.Y}[3]{C.E} 🔄 Đổi tài khoản{' ' * 40} {C.C}║{C.E}")
        print(f"{C.C}║{C.E}  {C.Y}[4]{C.E} 🚪 Thoát{' ' * 48} {C.C}║{C.E}")
        print(f"{C.C}╚{'═' * 60}╝{C.E}\n")
        
        ch = inp("➤ Chọn (1-4): ")
        
        if ch in ['1', '2']:
            l = load_lic()
            if not l or (l.get('mode') == 'FREE' and l.get('remain', 0) <= 0):
                print()
                msg("HẾT LƯỢT", 'e', C.R)
                print(f"\n{C.C}[1]{C.E} Chạy lại tool lấy key mới")
                print(f"{C.C}[2]{C.E} Thoát\n")
                if inp("Chọn: ") == '1':
                    return True  # Signal to restart
                else:
                    sys.exit(0)
        
        if ch == '1':
            solve_spec(s, uid)
        elif ch == '2':
            solve_link(s, uid)
        elif ch == '3':
            print()
            if inp("Đổi tài khoản? (y/n): ").lower() == 'y':
                msg("License vẫn được giữ", 'i', C.C)
                msg("Khởi động lại...", 'i', C.C)
                time.sleep(1)
                return True  # Signal to restart
        elif ch == '4':
            msg("Tạm biệt!", 'i', C.C)
            time.sleep(1)
            sys.exit(0)
        else:
            msg("Lựa chọn sai", 'e', C.R)
            time.sleep(1)

# ==================== MAIN ====================
def main():
    while True:
        # Check license
        lic = load_lic()
        
        # Login
        sess, uid, uname, vip = login()
        if not sess:
            sys.exit(0)
        
        # Handle license
        if vip:
            # VIP unlimited
            exp = (datetime.now() + timedelta(days=365)).strftime("%d/%m/%Y")
            save_lic('VIP', -1, exp, '')
            msg("VIP License kích hoạt", 'crown', C.M)
            time.sleep(1)
        elif not lic:
            # Need FREE key
            if not get_free_key():
                sys.exit(0)
        else:
            # Has license
            remain = lic.get('remain', 0)
            msg(f"License còn {remain} lượt", 'd', C.G)
            time.sleep(1)
        
        # Run menu (returns True if need restart)
        restart = menu(sess, uid, uname)
        if not restart:
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.Y}👋 Tạm biệt!{C.E}\n")
        sys.exit(0)
    except Exception as e:
        msg(f"Lỗi: {str(e)}", 'e', C.R)
        input(f"\n{C.Y}Enter...{C.E}")
        sys.exit(1)
