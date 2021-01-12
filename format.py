
def split_text(text : str, n = 1990):
    spl = []
    start = 0
    while len(text) - start > n:
        p = text.rfind('\n', start + n, n)
        spl.append(text[start : p])
        start = p + 1
    spl.append(text[start:])
    return spl