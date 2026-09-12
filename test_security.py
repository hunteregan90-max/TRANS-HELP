from app.security import invite_token, invite_hash
import string

def test_invite_shape():
    for _ in range(100):
        t=invite_token(); assert len(t)==35; assert any(c.isupper() for c in t); assert any(c.islower() for c in t); assert any(c.isdigit() for c in t); assert any(not c.isalnum() for c in t); assert t not in invite_hash(t)
