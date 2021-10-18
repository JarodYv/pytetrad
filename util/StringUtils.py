def compare_set(a: set, b: set) -> bool:
    if not len(a) == len(b):
        return False
    c = a & b
    return len(c) == len(a)
