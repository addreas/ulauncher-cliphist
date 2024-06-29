from subprocess import run

def cliphist_list():
    out = run(["cliphist", "list"], capture_output=True)
    return parse_list(out.stdout)

def parse_list(output):
    output = output.strip().split(b"\n")
    items = []
    for item in output:
        number, preview = item.split(b"\t")
        items.append((number, preview))
    return items

def set_clipboard(number):
    out = run(["cliphist", "decode"], input=number, capture_output=True)
    run(["wl-copy"], input=out.stdout)

