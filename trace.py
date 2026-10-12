"""Simple trace helper. Unit 4 adds trace.step calls to the loop."""
import config
_lines = []
_step_number = 0

def start_trace():
    global _step_number
    _lines.clear(); _step_number = 0

def step(name, inputs=None, returned=None, note=""):
    global _step_number
    _step_number += 1
    line = f"[{_step_number}] {name}"
    if inputs is not None: line += f"\n      in:  {_short(inputs)}"
    if returned is not None: line += f"\n      out: {_short(returned)}"
    if note: line += f"\n      ->   {note}"
    _lines.append(line)
    print(line, flush=True)

def get_trace():
    return "\n".join(_lines)

def _short(value, limit=110):
    if isinstance(value, list):
        if not value: return "[] (empty)"
        if isinstance(value[0], dict) and "title" in value[0]:
            names = ", ".join(v.get("title", "?") for v in value[:3])
            return f"{len(value)} items: {names}" + (f" ... +{len(value)-3} more" if len(value)>3 else "")
    if isinstance(value, dict):
        if "title" in value: return f"{value.get('title')} (${value.get('price')}, {value.get('platform')})"
        return "dict with keys: " + ", ".join(list(value)[:6])
    text = str(value).replace("\n", " ")
    return text if len(text) <= limit else text[:limit] + "..."

def check_iterations(count):
    if count > config.MAX_ITERATIONS:
        raise RuntimeError(f"Loop exceeded MAX_ITERATIONS={config.MAX_ITERATIONS}")
