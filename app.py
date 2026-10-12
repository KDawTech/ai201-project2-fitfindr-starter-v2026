#!/usr/bin/env python3
"""FitFindr CLI."""
import argparse, json
from utils.data_loader import load_listings, get_example_wardrobe, get_empty_wardrobe

EXAMPLE_QUERIES = [
    "vintage graphic tee under $30",
    "90s track jacket in size M",
    "silk slip dress in midi length under $40",
    "platform sneakers size 8",
    "denim jacket under $50",
    "designer ballgown size XXS under $5",
]

def fields(_):
    listing = load_listings()[0]
    print("A listing has these fields:\n")
    for k,v in listing.items(): print(f"  {k:<14} {type(v).__name__:<6} {str(v)[:60]}")
    item = get_example_wardrobe()["items"][0]
    print("\nA wardrobe item has these fields:\n")
    for k,v in item.items(): print(f"  {k:<14} {type(v).__name__:<6} {str(v)[:60]}")

def listings(args):
    items = load_listings()
    if args.full:
        for item in items[:args.n]: print(json.dumps(item, indent=2), "\n")
    else:
        print(f"{len(items)} listings.\n")
        for item in items[:args.n]: print(f"{item['id']:<8} ${item['price']:<6.2f} {item['size']:<20} {item['platform']:<10} {item['title']}")

def examples(_):
    for q in EXAMPLE_QUERIES: print(f"python app.py ask '{q}'")

def ask(args):
    import generate
    from agent import run_agent
    import trace as trace_module
    wardrobe = get_empty_wardrobe() if args.empty_wardrobe else get_example_wardrobe()
    if args.trace: trace_module.start_trace()
    session = run_agent(args.query, wardrobe)
    print()
    if session["error"]: print(" ", session["error"])
    else:
        item=session["selected_item"]
        print(f"  Found:    {item['title']} — ${item['price']} on {item['platform']}")
        print(f"\n  Outfit:   {session['outfit_suggestion']}")
        print(f"\n  Fit card: {session['fit_card']}")
    print("\n" + generate.usage())

def main():
    p=argparse.ArgumentParser(prog="app.py")
    sp=p.add_subparsers(dest="cmd",required=True)
    x=sp.add_parser("fields"); x.set_defaults(func=fields)
    x=sp.add_parser("listings"); x.add_argument("-n",type=int,default=15); x.add_argument("--full",action="store_true"); x.set_defaults(func=listings)
    x=sp.add_parser("examples"); x.set_defaults(func=examples)
    x=sp.add_parser("ask"); x.add_argument("query"); x.add_argument("--empty-wardrobe",action="store_true"); x.add_argument("--trace",action="store_true"); x.set_defaults(func=ask)
    args=p.parse_args(); args.func(args)

if __name__ == "__main__": main()
