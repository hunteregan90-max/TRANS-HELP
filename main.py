from fastapi import FastAPI, HTTPException, Header, Depends, Request
from pydantic import BaseModel, Field
from datetime import datetime, timezone, timedelta
import json, hashlib, time
from .db import init, conn
from .security import hash_password, verify_password, invite_token, invite_hash, issue_jwt, decode_jwt, fernet_from_env

app=FastAPI(title='Private Wellness API',version='0.1.0')
FERNET=fernet_from_env()
RANK_CAPS={'XXX':2,'XX':3,'X':4}
LOWER_RANKS=['Senior Officer','Officer','Community Guardian','Moderator','Support Leader','Group Leader','Verified Member','Member','New Member']

@app.on_event('startup')
def startup(): init()

class Register(BaseModel): invite_code:str=Field(min_length=35,max_length=35); username:str=Field(min_length=3,max_length=40); password:str=Field(min_length=10,max_length=200); display_name:str=Field(min_length=1,max_length=80)
class BootstrapReq(BaseModel): username:str=Field(min_length=3,max_length=40); password:str=Field(min_length=12,max_length=200); display_name:str=Field(min_length=1,max_length=80)
class Login(BaseModel): username:str; password:str
class InviteReq(BaseModel): hours_valid:int=Field(default=168,ge=1,le=8760)
class RankReq(BaseModel): rank:str
class ResponseReq(BaseModel): question_id:str=Field(pattern=r'^(TM|TW|MH)-\d{3}$'); value:object
class PostReq(BaseModel): body:str=Field(min_length=1,max_length=20000); visibility:str='community'
class ReportReq(BaseModel): post_id:int|None=None; reason:str=Field(min_length=3,max_length=1000)
class ProfileReq(BaseModel): pronouns:str|None=None; bio:str|None=Field(default=None,max_length=2000); followers_enabled:bool=False
class CommentReq(BaseModel): body:str=Field(min_length=1,max_length=10000)
class ReactionReq(BaseModel): reaction:str=Field(min_length=1,max_length=40)
class GroupReq(BaseModel): name:str=Field(min_length=1,max_length=120); description:str|None=Field(default=None,max_length=3000); kind:str='support'
class MessageReq(BaseModel): recipient_id:int; body:str=Field(min_length=1,max_length=20000)
class ModerateReq(BaseModel): action:str; reason:str|None=Field(default=None,max_length=2000); hours:int|None=Field(default=None,ge=1,le=8760)
class AppealReq(BaseModel): moderation_action_id:int|None=None; body:str=Field(min_length=3,max_length=5000)

def audit(actor,action,target_type=None,target_id=None,detail=None):
 c=conn(); c.execute('INSERT INTO audit(actor_id,action,target_type,target_id,detail) VALUES(?,?,?,?,?)',(actor,action,target_type,str(target_id) if target_id is not None else None,detail)); c.commit(); c.close()

def current_user(authorization:str|None=Header(default=None)):
 if not authorization or not authorization.startswith('Bearer '): raise HTTPException(401,'Authentication required')
 try: uid=decode_jwt(authorization[7:])
 except Exception: raise HTTPException(401,'Invalid or expired session')
 c=conn(); u=c.execute('SELECT * FROM users WHERE id=?',(uid,)).fetchone(); c.close()
 if not u or u['status']!='active': raise HTTPException(403,'Account unavailable')
 return dict(u)

def require_rank(*ranks):
 def dep(u=Depends(current_user)):
  if u['rank'] not in ranks: raise HTTPException(403,'Insufficient role')
  return u
 return dep

def blocked_attempt(kind,key_hash,limit=8):
 cutoff=int(time.time())-900; c=conn(); n=c.execute('SELECT COUNT(*) n FROM login_attempts WHERE kind=? AND key_hash=? AND success=0 AND created_at>?',(kind,key_hash,cutoff)).fetchone()['n']; c.close(); return n>=limit

def record_attempt(kind,key_hash,success):
 c=conn(); c.execute('INSERT INTO login_attempts(kind,key_hash,success,created_at) VALUES(?,?,?,?)',(kind,key_hash,1 if success else 0,int(time.time()))); c.commit(); c.close()

@app.get('/health')
def health(): return {'ok':True,'service':'private-wellness-api'}

@app.post('/admin/bootstrap')
def bootstrap(req:BootstrapReq, owner_secret:str=Header(alias='X-Bootstrap-Secret',default='')):
 expected=__import__('os').getenv('BOOTSTRAP_SECRET')
 if not expected or owner_secret!=expected: raise HTTPException(403,'Bootstrap disabled or secret incorrect')
 c=conn(); count=c.execute('SELECT COUNT(*) n FROM users').fetchone()['n']
 if count: c.close(); raise HTTPException(409,'Already bootstrapped')
 if c.execute('SELECT 1 FROM users WHERE username=?',(req.username,)).fetchone(): c.close(); raise HTTPException(409,'Username already exists')
 ph=hash_password(req.password); c.execute('INSERT INTO users(membership_no,username,display_name,password_hash,rank) VALUES(?,?,?,?,?)',('MEM-000001',req.username,req.display_name,ph,'XXX')); uid=c.execute('SELECT last_insert_rowid() id').fetchone()['id']; c.commit(); c.close(); audit(uid,'bootstrap_owner','user',uid,'Original creator account created as XXX.'); return {'membership_no':'MEM-000001','user_id':uid,'rank':'XXX','access_token':issue_jwt(uid),'token_type':'bearer'}

@app.post('/admin/invites')
def create_invite(req:InviteReq,u=Depends(require_rank('XXX','XX'))):
 token=invite_token(); h=invite_hash(token); exp=(datetime.now(timezone.utc)+timedelta(hours=req.hours_valid)).isoformat(); c=conn(); c.execute('INSERT INTO invites(token_hash,created_by,expires_at) VALUES(?,?,?)',(h,u['id'],exp)); iid=c.execute('SELECT last_insert_rowid() id').fetchone()['id']; c.commit(); c.close(); audit(u['id'],'create_invite','invite',iid); return {'invite_code':token,'length':len(token),'expires_at':exp,'display_once':True}


@app.get('/admin/invites')
def list_invites(status:str|None=None,u=Depends(require_rank('XXX','XX'))):
 c=conn(); rows=c.execute('SELECT id,created_by,created_at,expires_at,used_at,revoked_at FROM invites ORDER BY id DESC LIMIT 500').fetchall(); c.close(); now=datetime.now(timezone.utc); out=[]
 for r in rows:
  if r['revoked_at']: st='revoked'
  elif r['used_at']: st='used'
  elif r['expires_at'] and datetime.fromisoformat(r['expires_at'])<=now: st='expired'
  else: st='active'
  if status and st!=status: continue
  out.append({'id':r['id'],'created_by':r['created_by'],'created_at':r['created_at'],'expires_at':r['expires_at'],'used_at':r['used_at'],'revoked_at':r['revoked_at'],'status':st})
 return out

@app.delete('/admin/invites/{invite_id}')
def revoke_invite(invite_id:int,u=Depends(require_rank('XXX','XX'))):
 c=conn(); c.execute('UPDATE invites SET revoked_at=CURRENT_TIMESTAMP WHERE id=?',(invite_id,)); c.commit(); c.close(); audit(u['id'],'revoke_invite','invite',invite_id); return {'ok':True}

@app.post('/auth/register')
def register(req:Register, request:Request):
 h=invite_hash(req.invite_code)
 client_ip=request.client.host if request.client else 'unknown'
 ip_hash=hashlib.sha256(client_ip.encode()).hexdigest()
 if blocked_attempt('invite',h) or blocked_attempt('invite_ip',ip_hash,12): raise HTTPException(429,'Too many failed invitation attempts. Try later.')
 c=conn(); inv=c.execute('SELECT * FROM invites WHERE token_hash=?',(h,)).fetchone()
 valid=bool(inv and not inv['used_at'] and not inv['revoked_at'] and (not inv['expires_at'] or datetime.fromisoformat(inv['expires_at'])>datetime.now(timezone.utc)))
 record_attempt('invite',h,valid); record_attempt('invite_ip',ip_hash,valid)
 if not valid: c.close(); raise HTTPException(400,'Invitation is invalid, expired, revoked, or already used')
 if c.execute('SELECT 1 FROM users WHERE username=?',(req.username,)).fetchone(): c.close(); raise HTTPException(409,'Username already exists')
 next_id=c.execute('SELECT COALESCE(MAX(id),0)+1 n FROM users').fetchone()['n']; mem=f'MEM-{next_id:06d}'; rank='Member'
 c.execute('INSERT INTO users(membership_no,username,display_name,password_hash,rank) VALUES(?,?,?,?,?)',(mem,req.username,req.display_name,hash_password(req.password),rank)); uid=c.execute('SELECT last_insert_rowid() id').fetchone()['id']; c.execute('UPDATE invites SET used_at=CURRENT_TIMESTAMP WHERE id=?',(inv['id'],)); c.commit(); c.close(); audit(uid,'register','user',uid); return {'access_token':issue_jwt(uid),'token_type':'bearer','membership_no':mem,'rank':rank}

@app.post('/auth/login')
def login(req:Login):
 c=conn(); u=c.execute('SELECT * FROM users WHERE username=?',(req.username,)).fetchone(); c.close()
 if not u or not verify_password(u['password_hash'],req.password) or u['status']!='active': raise HTTPException(401,'Invalid credentials')
 return {'access_token':issue_jwt(u['id']),'token_type':'bearer','membership_no':u['membership_no'],'rank':u['rank']}

@app.get('/me')
def me(u=Depends(current_user)): return {k:u[k] for k in ['id','membership_no','username','display_name','rank','status','created_at']}

@app.patch('/admin/users/{user_id}/rank')
def set_rank(user_id:int,req:RankReq,u=Depends(require_rank('XXX','XX'))):
 rank=req.rank; c=conn(); target=c.execute('SELECT id,rank,status FROM users WHERE id=?',(user_id,)).fetchone(); c.close()
 if not target: raise HTTPException(404,'User not found')
 if target['rank']=='XXX' and u['rank']!='XXX': raise HTTPException(403,'Only XXX can change an XXX account')
 if rank in ('XXX','XX') and u['rank']!='XXX': raise HTTPException(403,'Only XXX can appoint XXX or XX')
 if rank=='XXX' and u['rank']!='XXX': raise HTTPException(403,'Only XXX can appoint XXX')
 if target['rank']==rank: return {'ok':True,'rank':rank}
 if rank in ('XXX','XX','X'):
  cap=RANK_CAPS[rank]; c=conn(); n=c.execute('SELECT COUNT(*) n FROM users WHERE rank=? AND status="active"',(rank,)).fetchone()['n']; c.close();
  if n>=cap: raise HTTPException(409,f'{rank} cap of {cap} reached')
 elif rank not in LOWER_RANKS: raise HTTPException(400,'Unknown rank')
 c=conn(); c.execute('UPDATE users SET rank=? WHERE id=?',(rank,user_id)); c.commit(); c.close(); audit(u['id'],'set_rank','user',user_id,rank); return {'ok':True,'rank':rank}

@app.put('/responses')
def put_response(req:ResponseReq,u=Depends(current_user)):
 blob=FERNET.encrypt(json.dumps(req.value,ensure_ascii=False).encode())
 c=conn(); c.execute('INSERT INTO responses(user_id,question_id,ciphertext) VALUES(?,?,?) ON CONFLICT(user_id,question_id) DO UPDATE SET ciphertext=excluded.ciphertext,updated_at=CURRENT_TIMESTAMP',(u['id'],req.question_id,blob)); c.commit(); c.close(); return {'ok':True}

@app.get('/responses')
def get_responses(u=Depends(current_user)):
 c=conn(); rows=c.execute('SELECT question_id,ciphertext,updated_at FROM responses WHERE user_id=?',(u['id'],)).fetchall(); c.close(); out=[]
 for r in rows:
  try: value=json.loads(FERNET.decrypt(r['ciphertext']).decode())
  except Exception: value=None
  out.append({'question_id':r['question_id'],'value':value,'updated_at':r['updated_at']})
 return out

@app.post('/posts')
def create_post(req:PostReq,u=Depends(current_user)):
 if req.visibility not in ['only_me','selected_contacts','friends','selected_group','leadership','community','custom']: raise HTTPException(400,'Invalid visibility')
 blob=FERNET.encrypt(req.body.encode()); c=conn(); c.execute('INSERT INTO posts(user_id,body_ciphertext,visibility) VALUES(?,?,?)',(u['id'],blob,req.visibility)); pid=c.execute('SELECT last_insert_rowid() id').fetchone()['id']; c.commit(); c.close(); return {'id':pid,'visibility':req.visibility}

@app.post('/reports')
def report(req:ReportReq,u=Depends(current_user)):
 c=conn(); c.execute('INSERT INTO reports(reporter_id,post_id,reason) VALUES(?,?,?)',(u['id'],req.post_id,req.reason)); rid=c.execute('SELECT last_insert_rowid() id').fetchone()['id']; c.commit(); c.close(); audit(u['id'],'report','report',rid); return {'id':rid,'status':'open'}

@app.get('/admin/audit')
def get_audit(u=Depends(require_rank('XXX','XX'))):
 c=conn(); rows=[dict(r) for r in c.execute('SELECT * FROM audit ORDER BY id DESC LIMIT 500').fetchall()]; c.close(); return rows

@app.get('/profile')
def get_profile(u=Depends(current_user)):
 c=conn(); p=c.execute('SELECT pronouns,bio,avatar_url,followers_enabled,updated_at FROM profiles WHERE user_id=?',(u['id'],)).fetchone(); c.close()
 return {'membership_no':u['membership_no'],'username':u['username'],'display_name':u['display_name'],'rank':u['rank'],'pronouns':p['pronouns'] if p else None,'bio':p['bio'] if p else None,'avatar_url':p['avatar_url'] if p else None,'followers_enabled':bool(p['followers_enabled']) if p else False}

@app.put('/profile')
def put_profile(req:ProfileReq,u=Depends(current_user)):
 c=conn(); c.execute('INSERT INTO profiles(user_id,pronouns,bio,followers_enabled) VALUES(?,?,?,?) ON CONFLICT(user_id) DO UPDATE SET pronouns=excluded.pronouns,bio=excluded.bio,followers_enabled=excluded.followers_enabled,updated_at=CURRENT_TIMESTAMP',(u['id'],req.pronouns,req.bio,1 if req.followers_enabled else 0)); c.commit(); c.close(); audit(u['id'],'update_profile','user',u['id']); return {'ok':True}

@app.get('/posts')
def list_posts(u=Depends(current_user)):
 c=conn()
 rows=c.execute("SELECT p.id,p.user_id,p.body_ciphertext,p.visibility,p.created_at,u.display_name,u.membership_no,u.rank FROM posts p JOIN users u ON u.id=p.user_id WHERE p.status='visible' AND (p.user_id=? OR p.visibility='community' OR (p.visibility='leadership' AND ? IN ('XXX','XX','X'))) ORDER BY p.id DESC LIMIT 200",(u['id'],u['rank'])).fetchall()
 c.close(); out=[]
 for r in rows:
  try: body=FERNET.decrypt(r['body_ciphertext']).decode()
  except Exception: body='[unavailable]'
  out.append({'id':r['id'],'user_id':r['user_id'],'display_name':r['display_name'],'membership_no':r['membership_no'],'rank':r['rank'],'body':body,'visibility':r['visibility'],'created_at':r['created_at']})
 return out

@app.post('/posts/{post_id}/comments')
def create_comment(post_id:int,req:CommentReq,u=Depends(current_user)):
 blob=FERNET.encrypt(req.body.encode()); c=conn(); post=c.execute('SELECT id FROM posts WHERE id=? AND status="visible"',(post_id,)).fetchone()
 if not post: c.close(); raise HTTPException(404,'Post not found')
 c.execute('INSERT INTO comments(post_id,user_id,body_ciphertext) VALUES(?,?,?)',(post_id,u['id'],blob)); cid=c.execute('SELECT last_insert_rowid() id').fetchone()['id']; c.commit(); c.close(); return {'id':cid}

@app.get('/posts/{post_id}/comments')
def list_comments(post_id:int,u=Depends(current_user)):
 c=conn(); rows=c.execute('SELECT c.id,c.user_id,c.body_ciphertext,c.created_at,u.display_name,u.membership_no FROM comments c JOIN users u ON u.id=c.user_id WHERE c.post_id=? AND c.status="visible" ORDER BY c.id ASC LIMIT 500',(post_id,)).fetchall(); c.close(); out=[]
 for r in rows:
  try: body=FERNET.decrypt(r['body_ciphertext']).decode()
  except Exception: body='[unavailable]'
  out.append({'id':r['id'],'user_id':r['user_id'],'display_name':r['display_name'],'membership_no':r['membership_no'],'body':body,'created_at':r['created_at']})
 return out

@app.put('/posts/{post_id}/reaction')
def put_reaction(post_id:int,req:ReactionReq,u=Depends(current_user)):
 c=conn(); c.execute('INSERT OR IGNORE INTO reactions(post_id,user_id,reaction) VALUES(?,?,?)',(post_id,u['id'],req.reaction)); c.commit(); c.close(); return {'ok':True}

@app.put('/posts/{post_id}/bookmark')
def put_bookmark(post_id:int,u=Depends(current_user)):
 c=conn(); c.execute('INSERT OR IGNORE INTO bookmarks(post_id,user_id) VALUES(?,?)',(post_id,u['id'])); c.commit(); c.close(); return {'ok':True}

@app.get('/groups')
def list_groups(u=Depends(current_user)):
 c=conn(); rows=[dict(r) for r in c.execute('SELECT g.*,CASE WHEN gm.user_id IS NULL THEN 0 ELSE 1 END joined FROM groups g LEFT JOIN group_members gm ON gm.group_id=g.id AND gm.user_id=? ORDER BY g.id DESC',(u['id'],)).fetchall()]; c.close(); return rows

@app.post('/groups')
def create_group(req:GroupReq,u=Depends(require_rank('XXX','XX','X','Senior Officer','Officer','Community Guardian','Moderator','Support Leader','Group Leader'))):
 c=conn(); c.execute('INSERT INTO groups(name,description,kind,created_by) VALUES(?,?,?,?)',(req.name,req.description,req.kind,u['id'])); gid=c.execute('SELECT last_insert_rowid() id').fetchone()['id']; c.execute('INSERT INTO group_members(group_id,user_id,role) VALUES(?,?,?)',(gid,u['id'],'owner')); c.commit(); c.close(); audit(u['id'],'create_group','group',gid); return {'id':gid}

@app.post('/groups/{group_id}/join')
def join_group(group_id:int,u=Depends(current_user)):
 c=conn(); exists=c.execute('SELECT id FROM groups WHERE id=?',(group_id,)).fetchone()
 if not exists: c.close(); raise HTTPException(404,'Group not found')
 c.execute('INSERT OR IGNORE INTO group_members(group_id,user_id) VALUES(?,?)',(group_id,u['id'])); c.commit(); c.close(); return {'ok':True}

@app.post('/messages')
def send_message(req:MessageReq,u=Depends(current_user)):
 if req.recipient_id==u['id']: raise HTTPException(400,'Choose another member')
 blob=FERNET.encrypt(req.body.encode()); c=conn(); target=c.execute('SELECT id FROM users WHERE id=? AND status="active"',(req.recipient_id,)).fetchone()
 if not target: c.close(); raise HTTPException(404,'Recipient unavailable')
 c.execute('INSERT INTO direct_messages(sender_id,recipient_id,body_ciphertext) VALUES(?,?,?)',(u['id'],req.recipient_id,blob)); mid=c.execute('SELECT last_insert_rowid() id').fetchone()['id']; c.commit(); c.close(); return {'id':mid}

@app.get('/messages/{other_user_id}')
def conversation(other_user_id:int,u=Depends(current_user)):
 c=conn(); rows=c.execute('SELECT id,sender_id,recipient_id,body_ciphertext,created_at FROM direct_messages WHERE (sender_id=? AND recipient_id=?) OR (sender_id=? AND recipient_id=?) ORDER BY id ASC LIMIT 1000',(u['id'],other_user_id,other_user_id,u['id'])).fetchall(); c.close(); out=[]
 for r in rows:
  try: body=FERNET.decrypt(r['body_ciphertext']).decode()
  except Exception: body='[unavailable]'
  out.append({'id':r['id'],'sender_id':r['sender_id'],'recipient_id':r['recipient_id'],'body':body,'created_at':r['created_at']})
 return out

@app.get('/admin/reports')
def admin_reports(u=Depends(require_rank('XXX','XX','X','Senior Officer','Officer','Community Guardian','Moderator'))):
 c=conn(); rows=[dict(r) for r in c.execute('SELECT * FROM reports ORDER BY id DESC LIMIT 500').fetchall()]; c.close(); return rows

@app.post('/admin/moderation')
def moderate(req:ModerateReq,target_user_id:int|None=None,target_post_id:int|None=None,u=Depends(require_rank('XXX','XX','X','Senior Officer','Officer','Community Guardian','Moderator'))):
 allowed={'warning','note','content_removal','temporary_mute','posting_cooldown','room_mute','temporary_suspension','permanent_removal'}
 if req.action not in allowed: raise HTTPException(400,'Unsupported moderation action')
 exp=(datetime.now(timezone.utc)+timedelta(hours=req.hours)).isoformat() if req.hours else None
 c=conn()
 if target_user_id:
  target=c.execute('SELECT id,rank FROM users WHERE id=?',(target_user_id,)).fetchone()
  if not target: c.close(); raise HTTPException(404,'Target user not found')
  if target['rank']=='XXX': c.close(); raise HTTPException(403,'XXX accounts require owner-level governance and cannot be restricted by ordinary community penalties')
  protected={'XX':{'XXX'},'X':{'XXX','XX'}}
  if target['rank'] in protected and u['rank'] not in protected[target['rank']]: c.close(); raise HTTPException(403,'Cannot moderate a higher leadership rank')
 c.execute('INSERT INTO moderation_actions(actor_id,target_user_id,target_post_id,action,reason,expires_at) VALUES(?,?,?,?,?,?)',(u['id'],target_user_id,target_post_id,req.action,req.reason,exp)); mid=c.execute('SELECT last_insert_rowid() id').fetchone()['id']
 if req.action=='content_removal' and target_post_id: c.execute('UPDATE posts SET status="removed" WHERE id=?',(target_post_id,))
 if req.action in ('temporary_suspension','permanent_removal') and target_user_id: c.execute('UPDATE users SET status=? WHERE id=?',('suspended' if req.action=='temporary_suspension' else 'removed',target_user_id))
 c.commit(); c.close(); audit(u['id'],req.action,'moderation_action',mid,req.reason); return {'id':mid,'expires_at':exp}

@app.post('/appeals')
def create_appeal(req:AppealReq,u=Depends(current_user)):
 c=conn(); c.execute('INSERT INTO appeals(user_id,moderation_action_id,body) VALUES(?,?,?)',(u['id'],req.moderation_action_id,req.body)); aid=c.execute('SELECT last_insert_rowid() id').fetchone()['id']; c.commit(); c.close(); return {'id':aid,'status':'open'}
