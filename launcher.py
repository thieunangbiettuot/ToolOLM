#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║               OLM MASTER PRO - LAUNCHER V1.0                 ║
║                    Created by: Tuấn Anh                      ║
╚══════════════════════════════════════════════════════════════╝
"""

import os, sys, time, json, hashlib, platform, tempfile, subprocess
import requests, re, pickle, socket, base64, random, uuid
from datetime import datetime, timedelta
from pathlib import Path

# ========== CONFIG ==========
API_TOKEN = "698b226d9150d31d216157a5"
URL_VIP = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"
URL_MAIN = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
}

class C:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

I = {
    'success': '✅', 'error': '❌', 'warning': '⚠️', 'info': 'ℹ️',
    'user': '👤', 'key': '🔑', 'star': '⭐', 'rocket': '🚀',
    'diamond': '💎', 'crown': '👑', 'exit': '🚪', 'link': '🔗'
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate(text, color=C.WHITE, delay=0.03):
    for char in text:
        sys.stdout.write(f"{color}{char}{C.END}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def spinner(msg, dur=1.5, color=C.CYAN):
    sp = ['|', '/', '-', '\\']
    end = time.time() + dur
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r{color}{msg} {sp[i % 4]}{C.END}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.15)
    print("\r" + " " * (len(msg) + 3) + "\r", end='')

def banner():
    clear()
    animate("╔══════════════════════════════════════════════════════════════╗", delay=0.01, color=C.BLUE + C.BOLD)
    animate("║               OLM MASTER PRO V1.0                            ║", delay=0.01, color=C.BLUE + C.BOLD)
    animate("║                  Created by: Tuấn Anh                        ║", delay=0.01, color=C.BLUE + C.BOLD)
    animate("╚══════════════════════════════════════════════════════════════╝", delay=0.01, color=C.BLUE + C.BOLD)
    print()

def msg(text, icon='info', color=C.WHITE):
    print(f"{I.get(icon, '•')} {color}{text}{C.END}")

def inp(prompt, color=C.YELLOW):
    return input(f"{color}{prompt}{C.END}").strip()

def is_android():
    return 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ

def get_data_dir():
    sp = platform.system().lower()
    if 'windows' in sp:
        d = Path(os.getenv('LOCALAPPDATA')) / 'Microsoft' / 'Windows' / 'INetCache' / 'IE'
    elif 'darwin' in sp:
        d = Path.home() / 'Library' / 'Application Support' / 'com.apple.Safari'
    elif is_android():
        d = Path.home() / '.cache' / 'google-chrome'
    else:
        d = Path.home() / '.cache' / 'mozilla' / 'firefox'
    d.mkdir(parents=True, exist_ok=True)
    return str(d)

DATA = get_data_dir()
HASH = hashlib.md5(f"{socket.gethostname()}{uuid.getnode()}".encode()).hexdigest()[:16]
LIC = os.path.join(DATA, f'.{HASH}sc')
SESS = os.path.join(DATA, f'.{HASH}ss')
ACC = os.path.join(DATA, f'.{HASH}ac')

KEY = b'OLM_MASTER_PRO_2026_SECRET_KEY_42'

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

def save_lic(mode, remain, expire, ip, sig):
    save_f(LIC, {'mode': mode, 'remain': remain, 'expire': expire, 'ip': ip, 'sig': sig})

def sig(d):
    return hashlib.sha256(f"{d['mode']}{d['expire']}{d['ip']}".encode()).hexdigest()

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
    print(f"{C.CYAN}╔{'═' * 60}╗{C.END}")
    print(f"{C.CYAN}║{C.BOLD}{' TÀI KHOẢN ĐÃ LƯU '.center(60)}{C.END}{C.CYAN}║{C.END}")
    print(f"{C.CYAN}╚{'═' * 60}╝{C.END}")
    al = list(accs.items())
    for i, (n, d) in enumerate(al, 1):
        print(f"{C.YELLOW}[{i}]{C.END} {n} ({d.get('saved_at', '')})")
    print(f"{C.YELLOW}[0]{C.END} Đăng nhập mới")
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

def check_vip(user):
    try:
        spinner("Kiểm tra VIP...", 1, C.MAGENTA)
        r = requests.get(URL_VIP, timeout=5)
        if r.status_code == 200:
            vips = [l.strip().lower() for l in r.text.splitlines() if l.strip() and not l.startswith('#')]
            return user.lower() in vips
    except:
        pass
    return False

def gen_key():
    now = datetime.now()
    u = f"{HASH}{now.timestamp()}{random.randint(1000, 9999)}"
    h = hashlib.sha256(u.encode()).hexdigest()
    return f"OLM-{now:%d%m}-{h[:4].upper()}-{h[4:8].upper()}"

def short_link(url):
    """Tạo link rút gọn - FIXED API"""
    try:
        # URL encode
        enc_url = requests.utils.quote(url)
        # API call
        api = f"https://link4m.co/api-shorten/v2?api={API_TOKEN}&url={enc_url}"
        r = requests.get(api, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "success":
                return data.get("shortenedUrl")
    except:
        pass
    return url

def get_free_key():
    """Flow vượt link FREE - Simplified"""
    blog = "https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html"
    
    for _ in range(3):
        k = gen_key()
        url = f"{blog}?ma={k}"
        
        # Tạo short link
        msg("Đang tạo link...", 'info', C.CYAN)
        short = short_link(url)
        
        # Display
        print(f"\n{C.GREEN}╔{'═' * 60}╗{C.END}")
        print(f"{C.GREEN}║{C.BOLD}{' VƯỢT LINK LẤY KEY '.center(60)}{C.END}{C.GREEN}║{C.END}")
        print(f"{C.GREEN}╠{'═' * 60}╣{C.END}")
        print(f"{C.GREEN}║{C.END} {C.CYAN}Link: {C.YELLOW}{short[:50]}{C.END}")
        print(f"{C.GREEN}║{C.END} {C.WHITE}1. Vượt link trên{C.END}")
        print(f"{C.GREEN}║{C.END} {C.WHITE}2. Nhập key bên dưới{C.END}")
        print(f"{C.GREEN}║{C.END} {C.YELLOW}   (Nhập 'r' để tạo link mới){C.END}")
        print(f"{C.GREEN}╚{'═' * 60}╝{C.END}\n")
        
        # Input
        for i in range(3):
            ki = inp(f"{I['key']} Key (r=mới): ")
            
            if ki.lower() == 'r':
                break
            
            if ki == k:
                exp = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
                ip = get_ip()
                s = sig({'mode': 'FREE', 'expire': exp, 'ip': ip})
                save_lic('FREE', 4, exp, ip, s)
                msg("✓ Key hợp lệ! 4 lượt đã kích hoạt", 'success', C.GREEN)
                time.sleep(1)
                return True
            
            if i < 2:
                msg(f"✗ Sai key! Còn {2-i} lần", 'warning', C.YELLOW)
                time.sleep(1)
        
        if ki.lower() == 'r':
            continue
    
    msg("Hết lượt thử", 'error', C.RED)
    return False

def login():
    banner()
    
    su, sp = select_acc()
    use_saved = False
    
    if su and sp:
        use_saved = inp("Dùng tài khoản đã lưu? (y/n): ").lower() == 'y'
    
    if use_saved:
        user, pwd = su, sp
    else:
        user = inp(f"{I['user']} Username: ")
        pwd = inp(f"{I['key']} Password: ")
    
    if not user or not pwd:
        msg("Thông tin rỗng!", 'error', C.RED)
        time.sleep(2)
        return None, None, None
    
    spinner("Đang đăng nhập...", 2, C.GREEN)
    
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
            
            # Get user_id
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
            
            # Check VIP
            vip = check_vip(user)
            
            msg(f"✓ Đăng nhập: {un}", 'success', C.GREEN)
            
            if vip:
                msg("VIP Unlimited", 'crown', C.MAGENTA)
            else:
                msg("FREE Account", 'info', C.YELLOW)
            
            # Save account
            if not use_saved:
                if inp("Lưu tài khoản? (y/n): ").lower() == 'y':
                    save_acc(un, user, pwd)
                    msg("✓ Đã lưu", 'success', C.GREEN)
            
            time.sleep(1)
            return s, uid, un
        
        else:
            msg("Sai username/password", 'error', C.RED)
            time.sleep(2)
            return None, None, None
    
    except Exception as e:
        msg(f"Lỗi: {str(e)}", 'error', C.RED)
        time.sleep(2)
        return None, None, None

def run_main(sess, uid, uname):
    td = tempfile.mkdtemp()
    mp = os.path.join(td, 'main.py')
    
    try:
        spinner("Tải main.py...", 1.5, C.BLUE)
        r = requests.get(URL_MAIN, timeout=15)
        
        if r.status_code == 200:
            with open(mp, 'w', encoding='utf-8') as f:
                f.write(r.text)
        else:
            msg("Không tải được main.py", 'error', C.RED)
            return
    except:
        msg("Lỗi tải main.py", 'error', C.RED)
        return
    
    # Save session
    sd = {'cookies': sess.cookies.get_dict(), 'user_id': uid, 'user_name': uname}
    st = os.path.join(td, 'session.pkl')
    with open(st, 'wb') as f:
        pickle.dump(sd, f)
    
    # Set env
    os.environ['OLM_SESSION_FILE'] = st
    os.environ['OLM_LICENSE_FILE'] = LIC
    
    msg("Khởi động tool...", 'rocket', C.GREEN)
    time.sleep(1)
    
    # Run
    try:
        subprocess.call([sys.executable, mp])
    except Exception as e:
        msg(f"Lỗi: {str(e)}", 'error', C.RED)
    finally:
        try:
            os.remove(mp)
            os.remove(st)
            os.rmdir(td)
        except:
            pass

def main():
    try:
        # Check license
        lic = load_lic()
        
        # Login
        sess, uid, uname = login()
        if not sess:
            sys.exit(0)
        
        # Check VIP
        vip = check_vip(uname)
        
        if vip:
            # VIP unlimited
            exp = (datetime.now() + timedelta(days=365)).strftime("%d/%m/%Y")
            s = sig({'mode': 'VIP', 'expire': exp, 'ip': ''})
            save_lic('VIP', -1, exp, '', s)
            msg("VIP License kích hoạt", 'crown', C.MAGENTA)
            time.sleep(1)
        elif not lic:
            # Need FREE key
            if not get_free_key():
                sys.exit(0)
        else:
            # Has license
            remain = lic.get('remain', 0)
            msg(f"License còn {remain} lượt", 'diamond', C.GREEN)
            time.sleep(1)
        
        # Run main
        run_main(sess, uid, uname)
        sys.exit(0)
    
    except KeyboardInterrupt:
        print(f"\n{I['exit']} {C.YELLOW}Tạm biệt!{C.END}")
        sys.exit(0)
    except Exception as e:
        msg(f"Lỗi: {str(e)}", 'error', C.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()
