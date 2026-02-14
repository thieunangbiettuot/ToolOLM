#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OLM Master Pro - Launcher"""

import os, sys, time, json, requests, hashlib, uuid, socket, base64, subprocess, tempfile
from datetime import datetime, timedelta
from pathlib import Path

# ========== CẤU HÌNH ==========
API_TOKEN = "698b226d9150d31d216157a5"
URL_BLOG = "https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html"
URL_MAIN = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"

# ========== DATA ==========
def get_data_dir():
    p = sys.platform
    if p == 'win32':
        base = os.getenv('LOCALAPPDATA') or os.getenv('APPDATA') or os.path.expanduser('~')
        d = Path(base) / 'Microsoft' / 'Windows' / 'INetCache' / 'IE'
    elif p == 'darwin':
        d = Path.home() / 'Library' / 'Application Support' / 'com.apple.Safari'
    elif p.startswith('linux'):
        if 'ANDROID_ROOT' in os.environ:
            d = Path(os.getenv('HOME', '/data/data/com.termux/files/home')) / '.cache' / 'google-chrome'
        else:
            d = Path.home() / '.cache' / 'mozilla' / 'firefox'
    else:
        d = Path.home() / '.config' / 'systemd'
    d.mkdir(parents=True, exist_ok=True)
    return str(d)

DATA = get_data_dir()
_h = hashlib.md5(f"{socket.gethostname()}{uuid.getnode()}".encode()).hexdigest()[:8]
LIC = os.path.join(DATA, f'.{_h}sc')

# ========== MÃ HÓA ==========
KEY = b'OLM_ULTRA_SECRET_2026'

def enc(obj):
    txt = json.dumps(obj, separators=(',', ':')).encode()
    xor = bytearray(txt[i] ^ KEY[i % len(KEY)] for i in range(len(txt)))
    b85 = base64.b85encode(bytes(xor)).decode()
    chk = hashlib.sha256(b85.encode()).hexdigest()[:12]
    noise = hashlib.md5(chk.encode()).hexdigest()[:8]
    return f"{noise}{chk}{b85}{noise[::-1]}"

# ========== MÀU ==========
C = type('C', (), {'R':'\033[91m','G':'\033[92m','Y':'\033[93m','B':'\033[94m','C':'\033[96m','W':'\033[97m','E':'\033[0m'})()

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    cls()
    print(f"\n{C.C}═══════════════════════════════{C.E}")
    print(f"{C.B}  OLM MASTER PRO v3.0{C.E}")
    print(f"{C.C}═══════════════════════════════{C.E}\n")

# ========== SYSTEM ==========
def ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        return "0.0.0.0"

def gen_key():
    import random
    now = datetime.now()
    dev = hashlib.md5(f"{socket.gethostname()}{uuid.getnode()}".encode()).hexdigest()[:16]
    unique = f"{dev}{now.timestamp()}{random.randint(1000, 9999)}"
    h = hashlib.sha256(unique.encode()).hexdigest()
    return f"OLM-{now:%d%m}-{h[:4].upper()}-{h[4:8].upper()}"

def save_lic(mode, n):
    d = {
        'mode': mode, 'remain': n,
        'expire': (datetime.now() + timedelta(days=3650)).strftime("%d/%m/%Y"),
        'ip': ip(), 'dev': '', 'hw': ''
    }
    d['sig'] = hashlib.sha256(f"{d['mode']}{d['expire']}{d['ip']}".encode()).hexdigest()[:16]
    with open(LIC, 'w') as f:
        f.write(enc(d))

# ========== GET KEY ==========
def get_key():
    while True:
        k = gen_key()
        
        # Tạo link
        try:
            url = f"{URL_BLOG}?ma={k}"
            api = f"https://link4m.co/api-shorten/v2?api={API_TOKEN}&url={requests.utils.quote(url)}"
            r = requests.get(api, timeout=8)
            link = r.json().get('shortenedUrl') if r.json().get('status') == 'success' else None
        except:
            link = None
        
        if not link:
            print(f"{C.R}  • Lỗi tạo link!{C.E}")
            retry = input(f"{C.Y}Thử lại? (y/n): {C.E}").lower().strip()
            if retry != 'y':
                return False
            continue
        
        print(f"\n{C.C}───────────────────────────────{C.E}")
        print(f"{C.G}Link: {link}{C.E}")
        print(f"{C.C}───────────────────────────────{C.E}\n")
        
        # Nhập mã
        for i in range(3):
            inp = input(f"{C.Y}Mã (r=đổi link): {C.E}").strip()
            
            if inp.lower() == 'r':
                break
            
            if inp == k or inp.upper() == "ADMIN_VIP_2026":
                is_vip = inp.upper() == "ADMIN_VIP_2026"
                save_lic("VIP" if is_vip else "FREE", 999999 if is_vip else 4)
                print(f"{C.G}  • OK{C.E}")
                time.sleep(1)
                return True
            
            if i < 2:
                print(f"{C.R}  • Sai ({2-i} lần){C.E}")
            time.sleep(i + 1)
        
        if inp.lower() != 'r':
            retry = input(f"\n{C.Y}Link mới? (y/n): {C.E}").lower().strip()
            if retry != 'y':
                return False

# ========== RUN ==========
def run():
    banner()
    print(f"{C.C}  • Đang tải...{C.E}")
    
    try:
        r = requests.get(URL_MAIN, timeout=15)
        r.raise_for_status()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w', encoding='utf-8') as f:
            f.write(r.text)
            temp = f.name
        
        env = os.environ.copy()
        env['OLM_LICENSE_FILE'] = LIC
        
        subprocess.run([sys.executable, temp], env=env)
        
        try:
            os.remove(temp)
        except:
            pass
    except Exception as e:
        print(f"{C.R}  • Lỗi: {e}{C.E}")
        input("\nEnter...")

# ========== MAIN ==========
if __name__ == "__main__":
    try:
        while True:
            banner()
            print(f"{C.Y}[1] Key FREE (4 lượt){C.E}")
            print(f"{C.G}[2] VIP Info{C.E}")
            print(f"{C.R}[0] Thoát{C.E}\n")
            
            ch = input(f"{C.Y}Chọn: {C.E}").strip()
            
            if ch == '1':
                if get_key():
                    run()
            elif ch == '2':
                banner()
                print(f"{C.G}═══════════════════════════════{C.E}")
                print(f"{C.G}  VIP: Unlimited{C.E}")
                print(f"{C.G}  Zalo: zalo.me/g/olmmaster{C.E}")
                print(f"{C.G}═══════════════════════════════{C.E}\n")
                input(f"{C.Y}Enter...{C.E}")
            elif ch == '0':
                sys.exit(0)
    except KeyboardInterrupt:
        print(f"\n{C.Y}Bye!{C.E}")
