import os, secrets, string, hashlib, time
from argon2 import PasswordHasher
from cryptography.fernet import Fernet
import jwt

PH=PasswordHasher()
JWT_SECRET=os.getenv('JWT_SECRET') or secrets.token_urlsafe(48)
JWT_ALG='HS256'
_INVITE_SYMBOLS='!@#$%^&*?_-+'
_INVITE_ALPHABET=string.ascii_letters+string.digits+_INVITE_SYMBOLS

def hash_password(p:str)->str: return PH.hash(p)
def verify_password(h:str,p:str)->bool:
    try: return PH.verify(h,p)
    except Exception: return False

def invite_token()->str:
    # exactly 35 chars and guaranteed to contain upper/lower/digit/symbol
    required=[secrets.choice(string.ascii_uppercase),secrets.choice(string.ascii_lowercase),secrets.choice(string.digits),secrets.choice(_INVITE_SYMBOLS)]
    chars=required+[secrets.choice(_INVITE_ALPHABET) for _ in range(31)]
    secrets.SystemRandom().shuffle(chars)
    return ''.join(chars)

def invite_hash(token:str)->str: return hashlib.sha256(token.encode()).hexdigest()

def issue_jwt(user_id:int,minutes:int=720)->str:
    now=int(time.time()); return jwt.encode({'sub':str(user_id),'iat':now,'exp':now+minutes*60},JWT_SECRET,algorithm=JWT_ALG)
def decode_jwt(token:str)->int: return int(jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALG])['sub'])

def fernet_from_env():
    raw=os.getenv('DATA_ENCRYPTION_KEY')
    if raw: return Fernet(raw.encode())
    path=os.path.join(os.path.dirname(__file__),'..','data','.dev_fernet_key')
    os.makedirs(os.path.dirname(path),exist_ok=True)
    if os.path.exists(path): key=open(path,'rb').read().strip()
    else:
        key=Fernet.generate_key(); open(path,'wb').write(key)
    return Fernet(key)
