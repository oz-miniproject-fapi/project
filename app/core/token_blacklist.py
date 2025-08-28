# app/core/token_blacklist.py
from datetime import datetime, timedelta

# 블랙리스트: 토큰 -> 만료시간
BLACKLIST = {}

def add_to_blacklist(token: str, expires_at: datetime):
    BLACKLIST[token] = expires_at

def is_blacklisted(token: str) -> bool:
    # 만료된 토큰은 자동 제거
    now = datetime.utcnow()
    expired_tokens = [t for t, exp in BLACKLIST.items() if exp < now]
    for t in expired_tokens:
        del BLACKLIST[t]
    return token in BLACKLIST
