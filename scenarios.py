"""Unit 4 evaluation scenarios. Included now so the same repo is ready for the next unit."""
SCENARIOS = [
    {"name":"matching query completes","query":"vintage graphic tee under $30","wardrobe":"example","criterion":1},
    {"name":"impossible query stops early","query":"designer ballgown size XXS under $5","wardrobe":"example","criterion":2},
    {"name":"state handoff","query":"90s track jacket size M","wardrobe":"example","criterion":3},
    {"name":"fit card facts","query":"denim jacket under $50","wardrobe":"example","criterion":4},
    {"name":"price ceiling","query":"vintage top under $20","wardrobe":"example","criterion":5},
    {"name":"empty wardrobe","query":"denim jacket under $50","wardrobe":"empty","criterion":None},
]
WARDROBES=("example","empty")
def validate():
    problems=[]
    for i,s in enumerate(SCENARIOS,1):
        if not s.get("query","").strip(): problems.append(f"scenario {i} has no query")
        if s.get("wardrobe") not in WARDROBES: problems.append(f"scenario {i} has invalid wardrobe")
    return problems
