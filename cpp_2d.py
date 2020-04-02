from time import time
from math import sqrt
from operator import itemgetter
from random import seed, randint
from bisect import bisect_left as bsearch

seed(123)
M, N = 100000000, 10000000
points = [[randint(-M, M), randint(-M, M), 0] for _ in range(N)]
Vx = sorted(points, key=itemgetter(0))
Vy = sorted(points, key=itemgetter(1))


def dist(a, b):
	xa, ya, _ = a
	xb, yb, _ = b
	return sqrt((xa - xb) ** 2 + (ya - yb) ** 2)


def d_and_d(Vx, Vy):
	if len(Vx) < 2:
		return [None, None, 0], float('inf')
	elif len(Vx) == 2:
		return Vx, dist(*Vx)

	im = len(Vx) // 2
	xm = Vx[im][0]
	Vx1 = Vx[:im]
	Vx2 = Vx[im:]

	for p in Vx2: # mark each point in the right
		p[-1] = 1
	Vy1, Vy2 = [], []
	for p in Vy: # divide between left and right
		(Vy1, Vy2)[p[-1]].append(p)
		p[-1] = 0 # remove mark

	p1, d1 = d_and_d(Vx1, Vy1)
	p2, d2 = d_and_d(Vx2, Vy2)
	delta, pair = (d1, p1) if d1 < d2 else (d2, p2)

	# find strip bounds:
	auxVx = [x[0] for x in Vx]
	i = bsearch(auxVx, xm - delta)
	j = bsearch(auxVx, xm + delta)

	for p in Vx[max(0, i):j]: # mark points in the strip
		p[-1] = 1
	strip = [p for p in Vy if p[-1]]

	cand = strip[:6]
	for i, p in enumerate(strip[3:-3]): # elevator like traversal
		cand.append(strip[i + 3])
		for q in cand:
			q[-1] = 0 # remove mark
			aux = dist(p, q)
			if aux < delta and id(p) != id(q):
				delta = aux
				pair = (p, q)
		cand.pop(0)

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
print(d_and_d(Vx, Vy))
print('took %.6fs' % (time() - start))