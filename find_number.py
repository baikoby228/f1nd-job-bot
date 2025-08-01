def find_number(s) -> int:
    res = 0

    for c in s:
        if '0' <= c <= '9':
            res = res * 10 + int(c)

    return res