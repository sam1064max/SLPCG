solutions = list()

def genSolutions(loopInfo, lde, s, x, v, n, sol, key):
	#print s, x, v, n, sol
	if x == n:
		if s == v:
			solutions.append([[key]]+[[i for i in j] for j in sol])
		return
	for x1 in range(loopInfo[x][1], loopInfo[x][2]):
		for y1 in range(loopInfo[x][1], loopInfo[x][2]):
			sol[0][x] = x1
			sol[1][x] = y1
			genSolutions(loopInfo, lde, s+(lde[0][loopInfo[x][0]]*x1 - lde[1][loopInfo[x][0]]*y1), x+1, v, n, sol, key)

def getSolutions(loopInfo, lde, key):
	global solutions
	solutions = list()
	v = lde[1]["con"] - lde[0]["con"]
	genSolutions(loopInfo, lde, 0, 0, v, len(loopInfo), [[None for _ in range(len(loopInfo))] for _ in range(2)], key)
	return solutions

def getIntersectionSolutions(loopInfo, lde, solutions):
	selectedSolutions = list()
	for solution in solutions:
		x1 = solution[1]
		y1 = solution[2]
		x, y = lde[0]["con"], lde[1]["con"]
		for i in range(len(loopInfo)):
			x+= lde[0][loopInfo[i][0]]*x1[i]
			y+= lde[1][loopInfo[i][0]]*y1[i]
		if x == y:
			selectedSolutions.append(solution)
			continue

		x1 = solution[1]
		y1 = solution[2]
		y, x = lde[0]["con"], lde[1]["con"]
		for i in range(len(loopInfo)):
			y+= lde[0][loopInfo[i][0]]*y1[i]
			x+= lde[1][loopInfo[i][0]]*x1[i]

		if x == y:
			selectedSolutions.append(solution)

	return selectedSolutions
