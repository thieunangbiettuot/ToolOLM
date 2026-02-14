#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OLM MASTER PRO - LAUNCHER"""

import os, sys, time, json, random, hashlib, uuid, base64, pickle, subprocess, tempfile, platform, shutil
from datetime import datetime, timedelta
try:
    import requests
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--quiet"])
    import requests
import re

# ==================== CONFIG ====================
GITHUB_MAIN = "https://github.com/USERNAME/ToolOLM/raw/refs/heads/main/main.py"
GITHUB_VIP = "https://raw.githubusercontent.com/USERNAME/ToolOLM/refs/heads/main/vip_users.txt"
LINK_API = "https://link4m.co/api-shorten/v2"
LINK_TOKEN = "YOUR_TOKEN_HERE"
SECRET = b"OLM_PRO_2026_SECURE"

# ==================== COLORS ====================
class C:
    G='\033[92m';Y='\033[93m';R='\033[91m';CY='\033[96m';B='\033[94m';M='\033[95m';W='\033[97m';BOLD='\033[1m';E='\033[0m'
I={'ok':'✅','no':'❌','warn':'⚠️','info':'ℹ️','user':'👤','key':'🔑','crown':'👑','gem':'💎','fire':'🔥','rocket':'🚀','zap':'⚡','link':'🔗'}

def clear():os.system('cls' if os.name=='nt' else 'clear')
def w():
    try:return min(shutil.get_terminal_size().columns,100)
    except:return 80
def logo():
    clear();width=w()
    lines=[" ██████╗ ██╗     ███╗   ███╗    ███╗   ███╗ █████╗ ","██╔═══██╗██║     ████╗ ████║    ████╗ ████║██╔══██╗","██║   ██║██║     ██╔████╔██║    ██╔████╔██║███████║","██║   ██║██║     ██║╚██╔╝██║    ██║╚██╔╝██║██╔══██║","╚██████╔╝███████╗██║ ╚═╝ ██║    ██║ ╚═╝ ██║██║  ██║"," ╚═════╝ ╚══════╝╚═╝     ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝"]
    print(f"\n{C.CY}{C.BOLD}")
    for l in lines:print(" "*((width-len(l))//2)+l)
    print(f"\n{' '*((width-34)//2)}MASTER PRO - Created by Tuấn Anh{C.E}\n")
def hdr(t=""):
    logo()
    if t:width=w();print(f"{C.CY}{'─'*width}{C.E}");print(f"{C.Y}{' '*((width-len(t))//2)}{t.upper()}{C.E}");print(f"{C.CY}{'─'*width}{C.E}\n")
def st(m,i='info',c=C.W):print(f"{I.get(i,I['info'])} {c}{m}{C.E}")
def wait(p="Nhấn Enter..."):input(f"\n{C.Y}{p}{C.E}")

# ==================== DEVICE ====================
def dev_hash():return hashlib.md5(f"{platform.node()}{uuid.getnode()}".encode()).hexdigest()[:8]
def get_paths():
    s=platform.system();h=dev_hash()
    if s=="Windows":b=os.path.join(os.environ.get('APPDATA',''),'Microsoft','Windows','.cache')
    elif os.path.exists('/data/data'):b=os.path.expanduser('~/.cache/.android')
    elif os.path.exists('/System/Library'):b=os.path.expanduser('~/Library/Application Support/.config')
    else:b=os.path.expanduser('~/.config/.cache')
    os.makedirs(b,exist_ok=True)
    return {'lic':os.path.join(b,f'.{h}sc'),'ses':os.path.join(b,f'.{h}ss'),'acc':os.path.join(b,f'.{h}ac'),'lck':os.path.join(b,f'.{h}lk')}
P=get_paths()

# ==================== CRYPTO ====================
def xor(d,k):return bytes([d[i]^k[i%len(k)]for i in range(len(d))])
def enc(dd):
    try:
        js=json.dumps(dd,separators=(',',':'));e=xor(js.encode('utf-8'),SECRET);b=base64.b85encode(e).decode('ascii');cs=hashlib.sha256(b.encode()).hexdigest()[:12];n=hashlib.md5(str(time.time()).encode()).hexdigest()
        return f"{n[:8]}{cs}{b}{n[-8:][::-1]}"
    except:return None
def dec(es):
    try:
        if not es or len(es)<28:return None
        d=es[8:-8];cs=d[:12];b=d[12:]
        if hashlib.sha256(b.encode()).hexdigest()[:12]!=cs:return None
        e=base64.b85decode(b.encode('ascii'));de=xor(e,SECRET)
        return json.loads(de.decode('utf-8'))
    except:return None
def sv(fp,dd):e=enc(dd);return open(fp,'w').write(e)if e else False
def ld(fp):
    if not os.path.exists(fp):return None
    try:return dec(open(fp,'r').read())
    except:return None

# ==================== VIP ====================
def chk_vip(u):
    try:
        r=requests.get(GITHUB_VIP,timeout=10)
        if r.status_code==200:
            vl=[l.strip().lower()for l in r.text.split('\n')if l.strip()and not l.strip().startswith('#')]
            return u.lower()in vl
    except:pass
    return False

# ==================== ACCOUNTS ====================
def ld_acc():d=ld(P['acc']);return d if d else {}
def sv_acc(a):return sv(P['acc'],a)
def sel_acc():
    a=ld_acc()
    if not a:return None,None
    print(f"\n{C.CY}TÀI KHOẢN ĐÃ LƯU:{C.E}");print(f"{C.CY}{'─'*60}{C.E}")
    al=list(a.items())
    for i,(n,d)in enumerate(al,1):print(f"{C.Y}{i}.{C.E} {n} {C.W}({d.get('saved_at','')}){C.E}")
    print(f"{C.Y}0.{C.E} Đăng nhập mới");print(f"{C.CY}{'─'*60}{C.E}")
    ch=input(f"{C.Y}Chọn (0-{len(al)}): {C.E}").strip()
    if ch=='0':return None,None
    if ch.isdigit():
        i=int(ch)-1
        if 0<=i<len(al):n,d=al[i];return d.get('username'),d.get('password')
    return None,None
def sv_new_acc(n,u,p):
    a=ld_acc();a[n]={'username':u,'password':p,'saved_at':datetime.now().strftime("%d/%m/%Y %H:%M")}
    if sv_acc(a):st(f"Đã lưu: {n}",'ok',C.G)

# ==================== LICENSE ====================
def ip():
    try:return requests.get('https://api.ipify.org?format=json',timeout=5).json()['ip']
    except:return "unknown"
def sig(lic):return hashlib.sha256(f"{lic.get('mode','')}{lic.get('expire','')}{lic.get('ip','')}".encode()).hexdigest()[:16]
def ld_lic():
    d=ld(P['lic'])
    if not d:return None
    if d.get('sig')!=sig(d):os.remove(P['lic']);return None
    try:
        ed=datetime.strptime(d['expire'],"%d/%m/%Y").date()
        if ed<datetime.now().date():os.remove(P['lic']);return None
    except:return None
    if d.get('mode')=='FREE' and d.get('ip')!=ip():st("IP thay đổi",'warn',C.Y);os.remove(P['lic']);return None
    if d.get('remain',0)<=0:os.remove(P['lic']);return None
    return d
def sv_lic(m,k,days,att):
    exp=(datetime.now()+timedelta(days=days)).strftime("%d/%m/%Y")
    ld={'mode':m,'key':k,'expire':exp,'remain':att,'ip':ip(),'created_at':datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
    ld['sig']=sig(ld);return sv(P['lic'],ld)

def ld_lck():d=ld(P['lck']);return d.get('username')if d else None
def sv_lck(u):return sv(P['lck'],{'username':u})

# ==================== KEY SYSTEM (ẨN KEY) ====================
def gen_key():
    """Generate HIDDEN secret key"""
    now=datetime.now();did=dev_hash();us=f"{did}{now.timestamp()}{random.randint(1000,9999)}"
    hv=hashlib.sha256(us.encode()).hexdigest()
    return f"KEY_{now:%d%m%H%M}_{hv[:8].upper()}"

def gen_code(secret_key):
    """Generate PUBLIC verification code từ secret key"""
    h=hashlib.sha256(secret_key.encode()).hexdigest()
    return f"OLM{h[:4].upper()}-{h[4:8].upper()}-{h[8:12].upper()}"

def verify_code(code,secret_key):
    """Verify code với secret key"""
    expected=gen_code(secret_key)
    return code.strip().upper()==expected.upper()

def shorten(lu):
    """Shorten link or fallback"""
    try:
        r=requests.post(LINK_API,json={'url':lu},headers={'api-token':LINK_TOKEN,'Content-Type':'application/json'},timeout=10)
        if r.status_code==200:
            res=r.json()
            if res.get('status')=='success'and res.get('shortenedUrl'):return res.get('shortenedUrl')
    except:pass
    return lu

def get_free():
    """
    QUAN TRỌNG:
    1. Key ẨN hoàn toàn (user KHÔNG BAO GIỜ thấy)
    2. User vượt link
    3. Sau vượt, page hiển thị VERIFICATION CODE
    4. User nhập code (KHÔNG phải key)
    """
    max_try=3
    for att in range(max_try):
        # 1. GENERATE SECRET KEY (ẨN)
        secret_key=gen_key()  # User KHÔNG thấy cái này
        
        # 2. GENERATE PUBLIC CODE
        verify_code_public=gen_code(secret_key)
        
        # 3. TẠO LINK
        base="https://olm.vn"
        # Link sẽ redirect về page có code
        long_link=f"{base}?v={verify_code_public}"
        
        st("Đang tạo link...",'info',C.Y);time.sleep(1)
        short_link=shorten(long_link)
        
        clear();hdr("BƯỚC 1: VƯỢT LINK ĐỂ LẤY MÃ")
        
        # 4. HIỂN THỊ LINK (KEY VẪN ẨN!)
        print(f"{C.G}{'═'*70}{C.E}")
        if short_link!=long_link:
            print(f"{C.CY}{I['link']} Link rút gọn:{C.E} {C.W}{short_link}{C.E}")
        else:
            print(f"{C.Y}{I['warn']} Link trực tiếp:{C.E}")
            print(f"{C.CY}{I['link']}{C.E} {C.W}{long_link}{C.E}")
        print(f"{C.G}{'═'*70}{C.E}\n")
        
        print(f"{C.Y}📌 HƯỚNG DẪN:{C.E}")
        print(f"  1. Mở link trên trong trình duyệt")
        print(f"  2. Vượt qua các bước xác minh")
        print(f"  3. Sau khi vượt, trang sẽ hiển thị MÃ XÁC NHẬN")
        print(f"  4. Copy mã đó và nhập vào bên dưới")
        print(f"\n{C.R}⚠️  LƯU Ý: Mã ≠ Key (Key đã được ẩn an toàn){C.E}\n")
        
        # 5. USER NHẬP VERIFICATION CODE
        for i in range(3):
            ui=input(f"{C.Y}{I['key']} Nhập mã xác nhận (hoặc 'r' tạo link mới): {C.E}").strip()
            
            if ui.lower()=='r':
                if att<max_try-1:st("Đang tạo link mới...",'info',C.Y);time.sleep(1);break
                else:st("Hết lượt tạo link",'no',C.R);return None
            
            # 6. VERIFY CODE
            if verify_code(ui,secret_key):
                st("✅ Xác thực thành công!",'ok',C.G);time.sleep(0.5)
                return secret_key  # Return SECRET key để lưu
            
            time.sleep(1)
            if i<2:st(f"Sai mã ({2-i} lần còn)",'no',C.R)
        
        if ui.lower()!='r':st("Hết lượt thử",'no',C.R);return None
    
    st("Hết lượt tạo link",'no',C.R);return None

# ==================== LOGIN ====================
HDR={'user-agent':'Mozilla/5.0','accept':'application/json, text/javascript, */*','accept-language':'vi-VN,vi','x-requested-with':'XMLHttpRequest','origin':'https://olm.vn','referer':'https://olm.vn/'}
def login(u,p):
    s=requests.Session();s.headers.update(HDR)
    try:
        st("Đang đăng nhập...",'info',C.Y)
        s.get("https://olm.vn/dangnhap",headers=HDR);csrf=s.cookies.get('XSRF-TOKEN')
        pl={'_token':csrf,'username':u,'password':p,'remember':'true','device_id':'0b48f4d6204591f83dc40b07f07af7d4','platform':'web'}
        hl=HDR.copy();hl['x-csrf-token']=csrf
        s.post("https://olm.vn/post-login",data=pl,headers=hl)
        cr=s.get("https://olm.vn/thong-tin-tai-khoan/info",headers=HDR)
        m=re.search(r'name="name".*?value="(.*?)"',cr.text)
        if m and m.group(1).strip():
            un=m.group(1).strip();uid=None
            for cn,cv in s.cookies.get_dict().items():
                if 'remember_web'in cn and'%7C'in cv:
                    try:pts=cv.split('%7C');
                        if pts and pts[0].isdigit():uid=pts[0];break
                    except:pass
            if not uid:idm=re.findall(r'\b\d{10,}\b',cr.text);uid=idm[0]if idm else u
            return s,uid,un
        return None,None,None
    except:return None,None,None

def sv_ses(s,uid,un):
    try:
        with open(P['ses'],'wb')as f:pickle.dump({'cookies':dict(s.cookies),'user_id':uid,'user_name':un},f)
        return True
    except:return False

# ==================== MAIN ====================
def main():
    clear();hdr("LAUNCHER")
    
    # 1. CHỌN TÀI KHOẢN
    su,sp=sel_acc()
    if su and sp:u,p=su,sp;st(f"Dùng: {su}",'ok',C.G)
    else:print(f"\n{C.CY}ĐĂNG NHẬP MỚI{C.E}");print(f"{C.CY}{'─'*60}{C.E}\n");u=input(f"{I['user']} {C.Y}Tên đăng nhập: {C.E}").strip();p=input(f"{I['key']} {C.Y}Mật khẩu: {C.E}").strip()
    if not u or not p:st("Thông tin không hợp lệ!",'no',C.R);wait();sys.exit(1)
    
    # 2. LOGIN
    s,uid,un=login(u,p)
    if not s:st("Đăng nhập thất bại!",'no',C.R);wait();sys.exit(1)
    clear();st("ĐĂNG NHẬP THÀNH CÔNG!",'ok',C.G+C.BOLD);st(f"Xin chào: {un}",'user',C.CY)
    if not su or su!=u:
        sc=input(f"\n{C.Y}Lưu tài khoản? (y/n): {C.E}").lower()
        if sc=='y':sv_new_acc(un,u,p)
    
    # 3. CHECK VIP
    st("Kiểm tra quyền...",'info',C.Y);time.sleep(1)
    vip=chk_vip(u)
    el=ld_lic()
    
    # 4. LICENSE
    if vip:
        clear();print(f"\n{C.M}{'═'*70}{C.E}");print(f"{C.M}{I['crown']} CHÀO VIP: {un}{C.E}");print(f"{C.M}{I['gem']} UNLIMITED{C.E}");print(f"{C.M}{'═'*70}{C.E}\n")
        sv_lic('VIP','VIP_'+u,3650,999999)
    elif el and el.get('remain',0)>0:
        clear();rm=el['remain'];print(f"\n{C.G}{'═'*70}{C.E}");print(f"{C.G}{I['gem']} Còn {rm} lượt{C.E}");print(f"{C.G}{'═'*70}{C.E}\n")
        la=ld_lck()
        if la and la!=u:st(f"Key dùng bởi: {la}",'warn',C.Y);st("Tiếp tục = chuyển tk",'info',C.CY)
        sv_lck(u)
    else:
        clear();print(f"\n{C.CY}{'═'*70}{C.E}");print(f"{C.CY}{I['info']} FREE (4 lượt/ngày){C.E}");print(f"{C.CY}{'═'*70}{C.E}\n")
        k=get_free()  # KEY ẨN - user chỉ nhập verification code
        if not k:st("Không lấy được key!",'no',C.R);wait();sys.exit(1)
        sv_lic('FREE',k,1,4);sv_lck(u)
        clear();print(f"\n{C.G}{'═'*70}{C.E}");print(f"{C.G}{I['ok']} Kích hoạt 4 lượt!{C.E}");print(f"{C.G}{'═'*70}{C.E}\n")
    
    # 5. SAVE SESSION
    if not sv_ses(s,uid,un):st("Lỗi lưu session!",'no',C.R);wait();sys.exit(1)
    
    # 6. DOWNLOAD MAIN
    st("Đang tải main.py...",'info',C.Y)
    try:
        r=requests.get(GITHUB_MAIN,timeout=15)
        if r.status_code==200:
            td=tempfile.gettempdir();mp=os.path.join(td,f'olm_{dev_hash()}.py')
            with open(mp,'wb')as f:f.write(r.content)
            clear();print(f"\n{C.G}{'═'*70}{C.E}");print(f"{C.G}{I['rocket']} KHỞI ĐỘNG...{C.E}");print(f"{C.G}{'═'*70}{C.E}\n");time.sleep(1)
            subprocess.run([sys.executable,mp])
            try:os.remove(mp)
            except:pass
        else:st("Lỗi tải main!",'no',C.R);wait();sys.exit(1)
    except Exception as e:st(f"Lỗi: {e}",'no',C.R);wait();sys.exit(1)

if __name__=="__main__":
    try:main()
    except KeyboardInterrupt:print(f"\n{I['warn']} {C.Y}Đã dừng{C.E}");sys.exit(0)
    except Exception as e:st(f"Lỗi: {e}",'no',C.R);wait();sys.exit(1)
