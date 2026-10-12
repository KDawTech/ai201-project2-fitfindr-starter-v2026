#!/usr/bin/env python3
"""Quick Unit 3 health check."""
import os, sys
from pathlib import Path

checks=[]
def check(name, fn):
    try:
        detail=fn(); checks.append((name,True,detail or "ok"))
    except Exception as exc: checks.append((name,False,str(exc)))

def main():
    check("Python version", lambda: sys.version.split()[0] if sys.version_info >= (3,11) else (_ for _ in ()).throw(RuntimeError("Python 3.11+ required")))
    check("Listings data", lambda: __import__('utils.data_loader',fromlist=['load_listings']).load_listings() and "loaded")
    def search_check():
        from tools import search_listings
        r=search_listings("graphic tee",max_price=30)
        assert r and r[0]["price"] <= 30
        return f"{len(r)} matches, top={r[0]['id']}"
    check("search_listings",search_check)
    def empty_check():
        from tools import search_listings
        assert search_listings("designer ballgown",size="XXS",max_price=5)==[]
        return "returns []"
    check("empty search",empty_check)
    def parse_check():
        from agent import parse_query
        p=parse_query("90s track jacket in size M under $50")
        assert p["size"]=="M" and p["max_price"]==50.0
        return str(p)
    check("query parser",parse_check)
    check(".env hygiene",lambda: ".env" in Path('.gitignore').read_text(encoding='utf-8'))
    print("FitFindr Unit 3 check\n"+"-"*50)
    for n,ok,d in checks: print(f"[{'PASS' if ok else 'FAIL'}] {n}\n       {d}")
    failed=sum(not ok for _,ok,_ in checks)
    print("-"*50); print(f"{len(checks)-failed} passed, {failed} failed")
    raise SystemExit(1 if failed else 0)
if __name__=='__main__': main()
