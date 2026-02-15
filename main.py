#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OLM MASTER PRO - MAIN V1.0"""

import os, sys, time, json, requests, hashlib, base64, re, random, socket, uuid, pickle
from bs4 import BeautifulSoup
from datetime import datetime

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

KEY = b'OLM_MASTER_PRO_2026_SECRET_KEY_42'

class Tool:
    def __init__(self):
        self.session = None
        self.user_id = None
        self.user_name = None
        self.lic_file = None
        
    def dec(self, es):
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
    
    def enc(self, data):
        js = json.dumps(data)
        bd = js.encode()
        xd = bytearray(b ^ KEY[i % len(KEY)] for i, b in enumerate(bd))
        b85 = base64.b85encode(bytes(xd)).decode()
        chk = hashlib.sha256(b85.encode()).hexdigest()[:12]
        np = hashlib.md5(os.urandom(16)).hexdigest()[:8]
        return f"{np}{chk}{b85}{np[::-1]}"
    
    def load_f(self, fn):
        if os.path.exists(fn):
            with open(fn, 'r') as f:
                return self.dec(f.read())
        return None
    
    def save_f(self, fn, data):
        with open(fn, 'w') as f:
            f.write(self.enc(data))
    
    def vfy(self, d):
        if not d:
            return False
        sig = hashlib.sha256(f"{d.get('mode', '')}{d.get('expire', '')}{d.get('ip', '')}".encode()).hexdigest()
        return d.get('sig') == sig
    
    def load_sess(self, sess_file):
        if not os.path.exists(sess_file):
            return False
        try:
            with open(sess_file, 'rb') as f:
                d = pickle.load(f)
            
            self.session = requests.Session()
            for n, v in d.get('cookies', {}).items():
                self.session.cookies.set(n, v)
            self.session.headers.update(HEADERS)
            
            self.user_id = d.get('user_id')
            self.user_name = d.get('user_name')
            self.lic_file = d.get('license_file')
            
            return True
        except:
            return False
    
    def load_lic(self):
        if not self.lic_file:
            return None
        d = self.load_f(self.lic_file)
        if not d or not self.vfy(d):
            if os.path.exists(self.lic_file):
                os.remove(self.lic_file)
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
    
    def upd_lic(self, nr):
        d = self.load_lic()
        if d and d.get('mode') == 'FREE':
            d['remain'] = nr
            self.save_f(self.lic_file, d)
    
    def deduct(self):
        l = self.load_lic()
        if not l:
            return False
        if l.get('mode') == 'VIP':
            return True
        r = l.get('remain', 0)
        if r > 0:
            self.upd_lic(r - 1)
            if r - 1 > 0:
                print(f"\n{C.G}{I['d']} Còn: {r-1} lượt{C.E}")
            else:
                print(f"\n{C.R}⛔ HẾT LƯỢT{C.E}")
            return True
        return False
    
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def banner(self):
        self.clear()
        print(f"{C.B}{C.BOLD}╔══════════════════════════════════════════════════════════════╗{C.E}")
        print(f"{C.B}{C.BOLD}║               OLM MASTER PRO V1.0                            ║{C.E}")
        print(f"{C.B}{C.BOLD}║                  Created by: Tuấn Anh                        ║{C.E}")
        print(f"{C.B}{C.BOLD}╚══════════════════════════════════════════════════════════════╝{C.E}\n")
    
    def msg(self, t, ic='i', col=C.W):
        print(f"{I.get(ic, '•')} {col}{t}{C.E}")
    
    def get_assignments(self, pages=3):
        self.msg(f"Quét {pages} trang...", 'i', C.C)
        asn = []
        seen = set()
        
        for p in range(1, pages + 1):
            url = f"https://olm.vn/lop-hoc-cua-toi/page-{p}?action=login" if p > 1 else "https://olm.vn/lop-hoc-cua-toi?action=login"
            
            try:
                r = self.session.get(url, headers=HEADERS, timeout=10)
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
            self.msg(f"Tìm thấy {len(asn)} bài", 's', C.G)
        else:
            self.msg("Không tìm thấy bài", 'w', C.Y)
        return asn
    
    def disp_asn(self, asn):
        if not asn:
            return
        
        print(f"\n{C.M}╔{'═' * 60}╗{C.E}")
        print(f"{C.M}║{C.BOLD}{'DANH SÁCH BÀI TẬP'.center(60)}{C.E}{C.M}║{C.E}")
        print(f"{C.M}╠{'═' * 60}╣{C.E}")
        
        for i, it in enumerate(asn, 1):
            t = it['title'] if len(it['title']) <= 35 else it['title'][:32] + "..."
            
            if it['is_video']:
                ic, cl = I['video'], C.B
            elif it['is_ly_thuyet']:
                ic, cl = I['book'], C.C
            else:
                ic, cl = I['pencil'], C.G
            
            ln = f"{i:2}. {ic} {cl}{it['type']:<12}{C.E} {C.W}{t}{C.E}"
            print(f"{C.M}║{C.E} {ln:<54} {C.M}║{C.E}")
        
        print(f"{C.M}╚{'═' * 60}╝{C.E}\n")
    
    def extract_quiz(self, url, is_v=False):
        try:
            r = self.session.get(url, timeout=10)
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
    
    def create_log(self, tq, ts):
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
    
    def try_vid(self, a, ql, ic, icat):
        try:
            csrf = self.session.cookies.get('XSRF-TOKEN')
            if not csrf:
                r = self.session.get(a['url'], timeout=10)
                m = re.search(r'<meta name="csrf-token" content="([^"]+)"', r.text)
                csrf = m.group(1) if m else ""
            
            dl = [{
                "answer": '["0"]', "params": '{"js":""}', "result": [1],
                "wrong_skill": [], "correct_skill": [], "type": [11],
                "id": f"vid{random.randint(100000, 999999)}", "marker": 1
            }]
            
            pl = {
                '_token': csrf, 'id_user': self.user_id, 'id_cate': icat or '0',
                'id_grade': '10', 'id_courseware': ic or '0',
                'time_spent': str(random.randint(300, 900)),
                'score': '100', 'data_log': json.dumps(dl, separators=(',', ':')),
                'date_end': str(int(time.time())), 'ended': '1', 'cv_q': '1'
            }
            
            if ql:
                pl['quiz_list'] = ql
            
            h = HEADERS.copy()
            h['x-csrf-token'] = csrf
            
            r = self.session.post('https://olm.vn/course/teacher-static', data=pl, headers=h, timeout=10)
            return r.status_code in [200, 403]
        except:
            return False
    
    def submit(self, a, ts):
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
            
            ql, tq, ic, icat = self.extract_quiz(a['url'], a['is_video'])
            
            if a['is_video']:
                ok = self.try_vid(a, ql, ic, icat)
                return ok
            
            if not ql or tq == 0:
                print(f"{C.R}✗ Không lấy được quiz{C.E}")
                return False
            
            dl, tt, cr = self.create_log(tq, ts)
            
            csrf = self.session.cookies.get('XSRF-TOKEN')
            if not csrf:
                r = self.session.get(a['url'], timeout=10)
                m = re.search(r'<meta name="csrf-token" content="([^"]+)"', r.text)
                csrf = m.group(1) if m else ""
            
            ct = int(time.time())
            
            pl = {
                '_token': csrf, 'id_user': self.user_id, 'id_cate': icat or '0',
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
            
            r = self.session.post('https://olm.vn/course/teacher-static', data=pl, headers=h, timeout=15)
            
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
    
    def solve_spec(self):
        self.banner()
        
        pgs = input(f"{C.Y}Số trang (3): {C.E}").strip()
        pgs = 3 if not pgs.isdigit() else min(int(pgs), 10)
        
        asn = self.get_assignments(pgs)
        if not asn:
            input(f"\n{C.Y}Enter...{C.E}")
            return
        
        self.disp_asn(asn)
        
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
                self.msg("Định dạng sai", 'e', C.R)
                input(f"\n{C.Y}Enter...{C.E}")
                return
        else:
            try:
                idx = int(sel) - 1
                if 0 <= idx < len(asn):
                    seld = [asn[idx]]
            except:
                self.msg("Số sai", 'e', C.R)
                input(f"\n{C.Y}Enter...{C.E}")
                return
        
        if not seld:
            self.msg("Không có bài", 'e', C.R)
            input(f"\n{C.Y}Enter...{C.E}")
            return
        
        print(f"\n{C.C}⭐ ĐIỂM:{C.E} 1=100, 2=Tùy chọn\n")
        ts = 100
        if input(f"{C.Y}➤ Chọn: {C.E}").strip() == '2':
            try:
                ts = max(0, min(100, int(input(f"{C.Y}Điểm (0-100): {C.E}").strip())))
            except:
                ts = 100
        
        print(f"\n{C.C}Số bài: {len(seld)}, Điểm: {ts}{C.E}\n")
        
        if input(f"{C.Y}Xác nhận? (y/n): {C.E}").strip().lower() != 'y':
            self.msg("Hủy", 'i', C.C)
            input(f"\n{C.Y}Enter...{C.E}")
            return
        
        sc, tc = 0, len(seld)
        
        print(f"\n{C.G}{'═' * 60}{C.E}")
        print(f"{C.G}{C.BOLD}BẮT ĐẦU XỬ LÝ{C.E}")
        print(f"{C.G}{'═' * 60}{C.E}")
        
        for i, a in enumerate(seld, 1):
            print(f"\n{C.Y}[{i}/{tc}]{C.E}")
            
            l = self.load_lic()
            if not l or (l.get('mode') == 'FREE' and l.get('remain', 0) <= 0):
                self.msg("HẾT LƯỢT", 'e', C.R)
                break
            
            ok = self.submit(a, ts)
            
            if ok:
                sc += 1
                self.deduct()
            else:
                if a['is_ly_thuyet']:
                    print(f"{C.Y}⚠ Lý thuyết vẫn trừ{C.E}")
                    self.deduct()
            
            if i < tc:
                time.sleep(random.randint(2, 4))
        
        print(f"\n{C.G}{'═' * 60}{C.E}")
        print(f"{C.G}✓ Hoàn thành: {sc}/{tc}{C.E}")
        print(f"{C.G}{'═' * 60}{C.E}")
        
        input(f"\n{C.Y}Enter...{C.E}")
    
    def solve_link(self):
        self.banner()
        
        print(f"{C.C}╔{'═' * 60}╗{C.E}")
        print(f"{C.C}║{C.BOLD}{'GIẢI TỪ LINK'.center(60)}{C.E}{C.C}║{C.E}")
        print(f"{C.C}╚{'═' * 60}╝{C.E}\n")
        
        url = input(f"{C.Y}🔗 Link: {C.E}").strip()
        
        if not url.startswith('https://olm.vn/'):
            self.msg("Link không hợp lệ", 'e', C.R)
            input(f"\n{C.Y}Enter...{C.E}")
            return
        
        try:
            r = self.session.get(url, timeout=10)
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
                if input(f"{C.Y}➤ Chọn: {C.E}").strip() == '2':
                    try:
                        ts = max(0, min(100, int(input(f"{C.Y}Điểm (0-100): {C.E}").strip())))
                    except:
                        ts = 100
            
            print(f"\n{C.C}Loại: {a['type']}, Điểm: {ts}{C.E}\n")
            
            if input(f"{C.Y}Xác nhận? (y/n): {C.E}").strip().lower() == 'y':
                l = self.load_lic()
                if not l or (l.get('mode') == 'FREE' and l.get('remain', 0) <= 0):
                    self.msg("HẾT LƯỢT", 'e', C.R)
                    input(f"\n{C.Y}Enter...{C.E}")
                    return
                
                ok = self.submit(a, ts)
                
                if ok:
                    self.deduct()
                else:
                    if a['is_ly_thuyet']:
                        print(f"{C.Y}⚠ Lý thuyết vẫn trừ{C.E}")
                        self.deduct()
                
                input(f"\n{C.Y}Enter...{C.E}")
            else:
                self.msg("Hủy", 'i', C.C)
                input(f"\n{C.Y}Enter...{C.E}")
        
        except Exception as e:
            self.msg(f"Lỗi: {str(e)}", 'e', C.R)
            input(f"\n{C.Y}Enter...{C.E}")
    
    def menu(self):
        while True:
            self.banner()
            
            print(f"{C.W}👤 {self.user_name}{C.E}")
            
            l = self.load_lic()
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
                l = self.load_lic()
                if not l or (l.get('mode') == 'FREE' and l.get('remain', 0) <= 0):
                    print()
                    self.msg("HẾT LƯỢT", 'e', C.R)
                    print(f"\n{C.C}[1]{C.E} Quay launcher lấy key mới")
                    print(f"{C.C}[2]{C.E} Thoát\n")
                    if input(f"{C.Y}Chọn: {C.E}").strip() == '1':
                        self.msg("Thoát về launcher...", 'i', C.C)
                        time.sleep(1)
                        sys.exit(0)
                    else:
                        self.msg("Tạm biệt!", 'i', C.C)
                        time.sleep(1)
                        sys.exit(0)
            
            if ch == '1':
                self.solve_spec()
            elif ch == '2':
                self.solve_link()
            elif ch == '3':
                print()
                if input(f"{C.Y}Đổi tài khoản? (y/n): {C.E}").strip().lower() == 'y':
                    self.msg("License vẫn được giữ", 'i', C.C)
                    self.msg("Thoát về launcher...", 'i', C.C)
                    time.sleep(1)
                    sys.exit(0)
            elif ch == '4':
                self.msg("Tạm biệt!", 'i', C.C)
                time.sleep(1)
                sys.exit(0)
            else:
                self.msg("Lựa chọn sai", 'e', C.R)
                time.sleep(1)
    
    def run(self):
        sess_file = os.getenv('OLM_SESSION_FILE')
        if not sess_file:
            self.msg("Không tìm thấy session file", 'e', C.R)
            self.msg("Chạy lại launcher", 'i', C.C)
            input(f"\n{C.Y}Enter...{C.E}")
            return
        
        if not self.load_sess(sess_file):
            self.msg("Không load được session", 'e', C.R)
            self.msg("Chạy lại launcher", 'i', C.C)
            input(f"\n{C.Y}Enter...{C.E}")
            return
        
        l = self.load_lic()
        if not l:
            self.msg("Không tìm thấy license!", 'e', C.R)
            self.msg("Chạy lại launcher", 'i', C.C)
            input(f"\n{C.Y}Enter...{C.E}")
            return
        
        self.banner()
        print(f"{C.W}👤 {self.user_name}{C.E}")
        
        m = l.get('mode', 'FREE')
        if m == 'VIP':
            print(f"{C.G}⭐ VIP UNLIMITED{C.E}")
        else:
            r = l.get('remain', 0)
            print(f"{C.Y}💎 {r} lượt{C.E}")
        
        time.sleep(2)
        
        self.menu()

if __name__ == "__main__":
    try:
        tool = Tool()
        tool.run()
    except KeyboardInterrupt:
        print(f"\n\n{C.Y}👋 Tạm biệt!{C.E}\n")
        sys.exit(0)
    except Exception as e:
        print(f"{C.R}❌ Lỗi: {str(e)}{C.E}")
        input(f"\n{C.Y}Enter...{C.E}")
