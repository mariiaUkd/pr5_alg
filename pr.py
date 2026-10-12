import random
import time
from operator import lt, gt


def partition(a, low, high, before):
    i = low
    for j in range(low, high):
        if before(a[j], a[high]):
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[high] = a[high], a[i]
    return i


def _qs(a, low, high, before):
    while low < high: 
        p = partition(a, low, high, before)
        if p - low < high - p:
            _qs(a, low, p - 1, before)
            low = p + 1
        else:
            _qs(a, p + 1, high, before)
            high = p - 1


def quick_sort(a, ascending=True):
    _qs(a, 0, len(a) - 1, lt if ascending else gt)
    return a


def is_sorted(a, ascending=True):
    ok = (lambda x, y: x <= y) if ascending else (lambda x, y: x >= y)
    return all(ok(a[i], a[i + 1]) for i in range(len(a) - 1))


def bubble_sort(a, ascending=True):
    before = lt if ascending else gt
    for i in range(len(a) - 1):
        for j in range(len(a) - 1 - i):
            if before(a[j + 1], a[j]):
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def selection_sort(a, ascending=True):
    before = lt if ascending else gt
    for i in range(len(a) - 1):
        m = i
        for j in range(i + 1, len(a)):
            if before(a[j], a[m]):
                m = j
        a[i], a[m] = a[m], a[i]
    return a


def insertion_sort(a, ascending=True):
    before = lt if ascending else gt
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0 and before(key, a[j]):
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def timeit(f, data, asc):
    a = data.copy()
    t = time.perf_counter()
    f(a, asc)
    t = time.perf_counter() - t
    assert is_sorted(a, asc)
    return t


if __name__ == "__main__":
    demo = [3, 7, 0, 1, 4, 2]
    print(demo, "->", quick_sort(demo.copy(), True), quick_sort(demo.copy(), False))
    print(is_sorted([1, 2, 3]), is_sorted([3, 1, 2]))

    algos = [quick_sort, bubble_sort, selection_sort, insertion_sort]
    for asc in (True, False):
        print(f"\n{'за зростанням' if asc else 'за спаданням'}, секунди")
        print(f"{'N':>8}" + "".join(f"{f.__name__:>16}" for f in algos))
        for n in (1_000, 10_000, 100_000):
            data = [random.uniform(-1e6, 1e6) for _ in range(n)]
            row = []
            for f in algos:
                if f is not quick_sort and n > 10_000: 
                    row.append("—")
                else:
                    row.append(f"{timeit(f, data, asc):.4f}")
            print(f"{n:>8}" + "".join(f"{x:>16}" for x in row))