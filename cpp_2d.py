from time import time
from math import sqrt
from operator import itemgetter
from itertools import takewhile
from random import seed, randint

seed(123)
M, N = 2500, 2500
points = [(randint(-M, M), randint(-M, M)) for _ in range(N)]
Vx = sorted(points, key=itemgetter(0))


def dist(a, b):
	xa, ya = a
	xb, yb = b
	return sqrt((xa - xb) ** 2 + (ya - yb) ** 2)


def d_and_d(S):
	if len(S) < 2:
		return (None, None), float('inf')
	elif len(S) == 2:
		return tuple(S), dist(*S)

	im = len(S) // 2
	xm = S[im][0]
	S1 = S[:im]
	S2 = S[im:]

	p1, d1 = d_and_d(S1)
	p2, d2 = d_and_d(S2)
	delta, pair = (d1, p1) if d1 < d2 else (d2, p2)

	# TODO: Way to remove this sorting:
	vy1F = list(takewhile(lambda p: p[0] > xm - delta, reversed(S1)))
	vy1F.sort(key=itemgetter(1))
	vy2F = list(takewhile(lambda p: p[0] < xm + delta, S2))
	vy2F.sort(key=itemgetter(1))

	i = 0
	for p in vy1F:
		while i < len(vy2F) and p[1] > vy2F[i][1]:
			i += 1

		cand = vy2F[max(0, i - 3):i + 3]
		for q in cand:
			aux = dist(p, q)
			if aux < delta:
				delta = aux
				pair = (p, q)

	return pair, delta


def naive(S):
	delta = float('inf')
	for i, p in enumerate(S[:-1]):
		for q in S[i + 1:]:
			aux = dist(p, q)
			if aux < delta:
				delta = aux
				pair = (p, q)

	return pair, delta

start = time()
print(d_and_d(Vx))
print('took %.6fs' % (time() - start))

start = time()
print(naive(Vx))
print('took %.6fs' % (time() - start))