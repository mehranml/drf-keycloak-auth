import json

def dump(out):
    try:
        out = json.dumps(out, indent=4, sort_keys=True)
    except Exception:
        pass

    CYAN = '\033[96m'
    ENDC = '\033[0m'
    print(CYAN + str(out).replace('\\n', '\n').replace('\\t', '\t') + ENDC)
