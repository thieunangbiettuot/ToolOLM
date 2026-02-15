#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OLM MASTER PRO - MAIN V1.0"""

import os, sys, time, json, requests, hashlib, base64, re, random, socket, uuid
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path

URL_VIP = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://olm.vn',
    'referer': 'https://olm.vn/'
}

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

I = {'s': '✅', 'e': '❌', 'w': '⚠️', 'i': 'ℹ️', 'd': '💎', 'video': '🎥', 'book': '📖', 'pencil': '📝'}

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
LIC = os.getenv('OLM_LICENSE_FILE', os.path.join(DATA, f'.{HASH}sc'))
SESS = os.getenv('OLM_SESSION_FILE', os.path.join(DATA, f'.{HASH}ss'))
KEY = b'OLM_MASTER_PRO_2026_SECRET_KEY_42'

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

def enc(data):
    js = json.dumps(data)
    bd = js.encode()
    xd = bytearray(b ^ KEY[i % len(KEY)] for i, b in enumerate(bd))
    b85 = base64.b85encode(bytes(xd)).decode()
    chk = hashlib.sha256(b85.encode()).hexdigest()[:12]
    np = hashlib.md5(os.urandom(16)).hexdigest()[:8]
    return f"{np}{chk}{b85}{np[::-1]}"

def load_f(fn):
    if os.path.exists(fn):
        with open(fn, 'r') as f:
            return dec(f.read())
    return None

def save_f(fn, data):
    with open(fn, 'w') as f:
        f.write(enc(data))

def vfy(d):
    if not d:
        return False
    sig = hashlib.sha256(f"{d.get('mode', '')}{d.get('expire', '')}{d.get('ip', '')}".encode()).hexdigest()
    return d.get('sig') == sig

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print(f"{C.B}{C.BOLD}╔══════════════════════════════════════════════════════════════╗{C.E}")
    print(f"{C.B}{C.BOLD}║               OLM MASTER PRO V1.0                            ║{C.E}")
    print(f"{C.B}{C.BOLD}║                  Created by: Tuấn Anh                        ║{C.E}")
    print(f"{C.B}{C.BOLD}╚══════════════════════════════════════════════════════════════╝{C.E}\n")

def msg(t, ic='i', col=C.W):
    print(f"{I.get(ic, '•')} {col}{t}{C.E}")

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
    if d.get('mode') == 'FREE' and d.get('remain', 0) <= 0:
        return None
    return d

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

def load_sess():
    if not os.path.exists(SESS):
        return None, None, None
    try:
        import pickle
        with open(SESS, 'rb') as f:
            d = pickle.load(f)
        s = requests.Session()
        for n, v in d.get('cookies', {}).items():
            s.cookies.set(n, v)
        s.headers.update(HEADERS)
        return s, d.get('user_id'), d.get('user_name')
    except:
        return None, None, None

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
                    
                    mon = row.find('span', class_='alert')
                    mt = mon.get_text(strip=True) if mon else "Khác"
                    
                    tb = re.sub(r'\([^)]*\)', '', lt).strip()
                    
                    fu = 'https://olm.vn' + href if not href.startswith('http') else href
                    
                    asn.append({
                        'title': tb[:50],
                        'subject': mt[:15],
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
        return asn
    else:
        msg("Không tìm thấy bài", 'w', C.Y)
        return []

def disp_asn(asn):
    if not asn:
        return
    
    print(f"\n{C.M}╔{'═' * 60}╗{C.E}")
    print(f"{C.M}║{C.BOLD}{'DANH SÁCH BÀI TẬP'.center(60)}{C.E}{C.M}║{C.E}")
    print(f"{C.M}╠{'═' * 60}╣{C.E}")
    
    for i, it in enumerate(asn, 1):
        t = it['title']
        if len(t) > 35:
            t = t[:32] + "..."
        
        if it['is_video']:
            ic = I['video']
            cl = C.B
        elif it['is_ly_thuyet']:
            ic = I['book']
            cl = C.C
        else:
            ic = I['pencil']
            cl = C.G
        
        ln = f"{i:2}. {ic} {cl}{it['type']:<12}{C.E} {C.W}{t}{C.E}"
        print(f"{C.M}║{C.E} {ln:<54} {C.M}║{C.E}")
    
    print(f"{C.M}╚{'═' * 60}╝{C.E}\n")

def extract_quiz(s, url, is_v=False):
    try:
        r = s.get(url, timeout=10)
        h = r.text
        
        ql = None
        p1 = r'quiz_list\s*[:=]\s*["\'](\d{6,}(?:,\d{6,})*)["\']'
        m1 = re.search(p1, h)
        if m1:
            ql = m1.group(1)
        
        if not ql:
            p2 = r'\b\d{9,}(?:,\d{9,})+\b'
            ms = re.findall(p2, h)
            if ms:
                ql = max(ms, key=len)
        
        if not ql:
            p3 = r'"quiz_list"\s*:\s*"(\d+(?:,\d+)*)"'
            m3 = re.search(p3, h)
            if m3:
                ql = m3.group(1)
        
        ic = None
        cwm = re.search(r'id_courseware\s*[:=]\s*["\']?(\d+)["\']?', h)
        if cwm:
            ic = cwm.group(1)
        else:
            cwm = re.search(r'data-courseware\s*=\s*["\'](\d+)["\']', h)
            if cwm:
                ic = cwm.group(1)
        
        icat = None
        cm = re.search(r'-(\d+)(?:\?|$)', url)
        if cm:
            icat = cm.group(1)
        
        if not ql:
            if is_v:
                return "", 0, ic, icat
            else:
                return None, 0, ic, icat
        
        qs = [q.strip() for q in ql.split(',') if q.strip()]
        tq = len(qs)
        
        return ql, tq, ic, icat
    except:
        return None, 0, None, None

def create_log(tq, ts):
    if ts == 100:
        cr = tq
    elif ts == 0:
        cr = 0
    else:
        cr = round((ts / 100) * tq)
        cr = max(0, min(tq, cr))
    
    wr = tq - cr
    res = [1] * cr + [0] * wr
    random.shuffle(res)
    
    dl = []
    tt = 0
    
    for i, ic in enumerate(res):
        tsp = random.randint(10, 30) + (i % 5)
        tt += tsp
        ord = [0, 1, 2, 3]
        random.shuffle(ord)
        ca = "0" if ic else str(random.randint(1, 3))
        
        dl.append({
            "q_params": json.dumps([{"js": "", "order": ord}]),
            "a_params": json.dumps([f'["{ca}"]']),
            "result": ic,
            "correct": ic,
            "wrong": 0 if ic else 1,
            "a_index": i,
            "time_spent": tsp
        })
    
    return dl, tt, cr

def try_vid(s, a, uid, ql, tq, ic, icat):
    try:
        csrf = s.cookies.get('XSRF-TOKEN')
        if not csrf:
            r = s.get(a['url'], timeout=10)
            cm = re.search(r'<meta name="csrf-token" content="([^"]+)"', r.text)
            csrf = cm.group(1) if cm else ""
        
        ct = int(time.time())
        tsp = random.randint(300, 900)
        
        dl = [{
            "answer": '["0"]',
            "params": '{"js":""}',
            "result": [1],
            "wrong_skill": [],
            "correct_skill": [],
            "type": [11],
            "id": f"vid{random.randint(100000, 999999)}",
            "marker": 1
        }]
        
        pl = {
            '_token': csrf,
            'id_user': uid,
            'id_cate': icat or '0',
            'id_grade': '10',
            'id_courseware': ic or '0',
            'time_spent': str(tsp),
            'score': '100',
            'data_log': json.dumps(dl, separators=(',', ':')),
            'date_end': str(ct),
            'ended': '1',
            'cv_q': '1'
        }
        
        if ql:
            pl['quiz_list'] = ql
        
        h = HEADERS.copy()
        h['x-csrf-token'] = csrf
        
        r = s.post('https://olm.vn/course/teacher-static', data=pl, headers=h, timeout=10)
        
        if r.status_code in [200, 403]:
            return True
    except:
        pass
    return False

def handle_vid(s, a, uid, ql, tq, ic, icat):
    return try_vid(s, a, uid, ql, tq, ic, icat)

def submit(s, a, uid, ts):
    print(f"\n{C.C}{'─' * 60}{C.E}")
    print(f"{C.W}📝 {a['title'][:45]}{C.E}")
    
    if a['is_video']:
        print(f"{C.B}🎬 Video{C.E}")
    elif a['is_ly_thuyet']:
        print(f"{C.C}📖 Lý thuyết{C.E}")
    else:
        print(f"{C.G}📝 Bài tập{C.E}")
    
    try:
        time.sleep(0.5)
        
        ql, tq, ic, icat = extract_quiz(s, a['url'], a['is_video'])
        
        if a['is_video']:
            ok = handle_vid(s, a, uid, ql, tq, ic, icat)
            return ok
        
        if not ql or tq == 0:
            print(f"{C.R}✗ Không lấy được quiz{C.E}")
            return False
        
        dl, tt, cr = create_log(tq, ts)
        
        csrf = s.cookies.get('XSRF-TOKEN')
        if not csrf:
            r = s.get(a['url'], timeout=10)
            cm = re.search(r'<meta name="csrf-token" content="([^"]+)"', r.text)
            csrf = cm.group(1) if cm else ""
        
        ct = int(time.time())
        st = ct - tt if tt > 0 else ct - 600
        
        ua = ["0"] * tq
        la = ["0"] * tq
        
        pl = {
            '_token': csrf,
            'id_user': uid,
            'id_cate': icat or '0',
            'id_grade': '10',
            'id_courseware': ic or '0',
            'id_group': '6148789559',
            'id_school': '0',
            'time_init': str(st),
            'name_user': '',
            'type_vip': '0',
            'time_spent': str(tt),
            'data_log': json.dumps(dl, separators=(',', ':')),
            'score': str(ts),
            'answered': str(tq),
            'correct': str(cr),
            'count_problems': str(tq),
            'missed': str(tq - cr),
            'time_stored': str(ct),
            'date_end': str(ct),
            'ended': '1',
            'save_star': '0',
            'cv_q': '1',
            'quiz_list': ql or '',
            'choose_log': json.dumps(dl, separators=(',', ':')),
            'user_ans': json.dumps(ua),
            'list_quiz': ql or '',
            'list_ans': ','.join(la),
            'result': '[]',
            'ans': '[]'
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

def solve_spec(s, uid):
    banner()
    
    pgs = input(f"{C.Y}Số trang (3): {C.E}").strip()
    pgs = 3 if not pgs.isdigit() else min(int(pgs), 10)
    
    asn = get_assignments(s, pgs)
    if not asn:
        input(f"\n{C.Y}Enter...{C.E}")
        return
    
    disp_asn(asn)
    
    print(f"{C.C}Chọn:{C.E} 0=tất cả, 1,3,5=nhiều, 1=1 bài\n")
    sel = input(f"{C.Y}➤ Chọn: {C.E}").strip()
    
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
    sc = input(f"{C.Y}➤ Chọn: {C.E}").strip()
    
    if sc == '2':
        try:
            ts = int(input(f"{C.Y}Điểm (0-100): {C.E}").strip())
            ts = max(0, min(100, ts))
        except:
            ts = 100
    
    print(f"\n{C.C}Số bài: {len(seld)}, Điểm: {ts}{C.E}\n")
    
    if input(f"{C.Y}Xác nhận? (y/n): {C.E}").strip().lower() != 'y':
        msg("Hủy", 'i', C.C)
        input(f"\n{C.Y}Enter...{C.E}")
        return
    
    sc = 0
    tc = len(seld)
    
    print(f"\n{C.G}{'═' * 60}{C.E}")
    print(f"{C.G}{C.BOLD}BẮT ĐẦU XỬ LÝ{C.E}")
    print(f"{C.G}{'═' * 60}{C.E}")
    
    for i, a in enumerate(seld, 1):
        print(f"\n{C.Y}[{i}/{tc}]{C.E}")
        
        l = load_lic()
        if not l:
            msg("HẾT LƯỢT", 'e', C.R)
            break
        
        if l.get('mode') == 'FREE' and l.get('remain', 0) <= 0:
            msg("HẾT LƯỢT", 'e', C.R)
            break
        
        ok = submit(s, a, uid, ts)
        
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

def solve_link(s, uid):
    banner()
    
    print(f"{C.C}╔{'═' * 60}╗{C.E}")
    print(f"{C.C}║{C.BOLD}{'GIẢI TỪ LINK'.center(60)}{C.E}{C.C}║{C.E}")
    print(f"{C.C}╚{'═' * 60}╝{C.E}\n")
    
    url = input(f"{C.Y}🔗 Link: {C.E}").strip()
    
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
            'subject': "Tự chọn",
            'type': "Video" if is_v else ("Lý thuyết" if is_l else "Bài tập"),
            'url': url,
            'is_video': is_v,
            'is_ly_thuyet': is_l,
            'is_bai_tap': not (is_v or is_l)
        }
        
        ts = 100
        if not is_v:
            print(f"\n{C.C}⭐ ĐIỂM:{C.E} 1=100, 2=Tùy chọn\n")
            sc = input(f"{C.Y}➤ Chọn: {C.E}").strip()
            
            if sc == '2':
                try:
                    ts = int(input(f"{C.Y}Điểm (0-100): {C.E}").strip())
                    ts = max(0, min(100, ts))
                except:
                    ts = 100
        
        print(f"\n{C.C}Loại: {a['type']}, Điểm: {ts}{C.E}\n")
        
        if input(f"{C.Y}Xác nhận? (y/n): {C.E}").strip().lower() == 'y':
            l = load_lic()
            if not l:
                msg("HẾT LƯỢT", 'e', C.R)
                input(f"\n{C.Y}Enter...{C.E}")
                return
            
            if l.get('mode') == 'FREE' and l.get('remain', 0) <= 0:
                msg("HẾT LƯỢT", 'e', C.R)
                input(f"\n{C.Y}Enter...{C.E}")
                return
            
            ok = submit(s, a, uid, ts)
            
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
        
        ch = input(f"{C.Y}➤ Chọn (1-4): {C.E}").strip()
        
        if ch in ['1', '2']:
            l = load_lic()
            if not l:
                print()
                msg("HẾT LƯỢT", 'e', C.R)
                print(f"\n{C.C}[1]{C.E} Quay launcher lấy key mới")
                print(f"{C.C}[2]{C.E} Thoát\n")
                sc = input(f"{C.Y}Chọn: {C.E}").strip()
                if sc == '1':
                    msg("Thoát về launcher...", 'i', C.C)
                    time.sleep(1)
                    sys.exit(0)
                else:
                    msg("Tạm biệt!", 'i', C.C)
                    time.sleep(1)
                    sys.exit(0)
            
            if l.get('mode') == 'FREE' and l.get('remain', 0) <= 0:
                print()
                msg("HẾT LƯỢT", 'e', C.R)
                print(f"\n{C.C}[1]{C.E} Quay launcher lấy key mới")
                print(f"{C.C}[2]{C.E} Thoát\n")
                sc = input(f"{C.Y}Chọn: {C.E}").strip()
                if sc == '1':
                    msg("Thoát về launcher...", 'i', C.C)
                    time.sleep(1)
                    sys.exit(0)
                else:
                    msg("Tạm biệt!", 'i', C.C)
                    time.sleep(1)
                    sys.exit(0)
        
        if ch == '1':
            solve_spec(s, uid)
        elif ch == '2':
            solve_link(s, uid)
        elif ch == '3':
            print()
            if input(f"{C.Y}Đổi tài khoản? (y/n): {C.E}").strip().lower() == 'y':
                msg("License vẫn được giữ", 'i', C.C)
                msg("Thoát về launcher...", 'i', C.C)
                time.sleep(1)
                sys.exit(0)
        elif ch == '4':
            msg("Tạm biệt!", 'i', C.C)
            time.sleep(1)
            sys.exit(0)
        else:
            msg("Lựa chọn sai", 'e', C.R)
            time.sleep(1)

def main():
    s, uid, un = load_sess()
    
    if not s or not uid or not un:
        msg("Không load được session", 'e', C.R)
        msg("Chạy lại launcher", 'i', C.C)
        input(f"\n{C.Y}Enter...{C.E}")
        return
    
    l = load_lic()
    if not l:
        msg("Không có license", 'e', C.R)
        msg("Chạy lại launcher", 'i', C.C)
        input(f"\n{C.Y}Enter...{C.E}")
        return
    
    banner()
    print(f"{C.W}👤 {un}{C.E}")
    
    m = l.get('mode', 'FREE')
    if m == 'VIP':
        print(f"{C.G}⭐ VIP UNLIMITED{C.E}")
    else:
        r = l.get('remain', 0)
        print(f"{C.Y}💎 {r} lượt{C.E}")
    
    time.sleep(2)
    
    menu(s, uid, un)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.Y}👋 Tạm biệt!{C.E}\n")
        sys.exit(0)
    except Exception as e:
        msg(f"Lỗi: {str(e)}", 'e', C.R)
        input(f"\n{C.Y}Enter...{C.E}")
