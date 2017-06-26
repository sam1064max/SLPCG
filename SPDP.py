import sys
import ast
import itertools
from bitstring import BitArray

def init(loopInfo, stateInfo, pdpFile, lde1, bitVectorList, bitVector, numberofStatements1):
	global numberOfNestedLoops, statements, pdpPartition, lde2StateMapping, numberofStatements
	global independantComponents, dependantComponents, dependantComponentsBitVector, lde
	global upperLimits, lowerLimits, ranges, bitBlocks, bitVectorSize, partitionSize, globalBitVector
	global numberofStatements2
	lde = lde1
	numberOfNestedLoops = len(loopInfo)
	statements = getStatements(lde)
	pdpPartition = pdpFile
	lde2StateMapping = getLDE2StateMapping(lde)
	numberofStatements = len(stateInfo)
	upperLimits = getUpperLimits(loopInfo)
	lowerLimits = getLowerLimits(loopInfo)
	ranges = getRanges(upperLimits,lowerLimits)
	numberofStatements2 = numberofStatements1
	bitBlocks = getBitBlocks()
	bitVectorSize, partitionSize = getBitVectorSize(upperLimits,lowerLimits,numberOfNestedLoops,numberofStatements2)
	globalBitVector = bitVector
	dependantComponentsBitVector = bitVectorList
	dependantComponents = list()
	independantComponents = list()

def getLoopVariables(loopInfo):
	return [i[0] for i in loopInfo]

def getLowerLimits(loopInfo):
    return [int(i[1]) for i in loopInfo]

def getUpperLimits(loopInfo):
    return [int(i[2]) for i in loopInfo]

def getRanges(upperLimits, lowerLimits):
	return [upperLimits[i]-lowerLimits[i] for i in range(numberOfNestedLoops)]

def getStatements(lde): 
	stateList = [l.values() for l in lde[:2]]
	return stateList

def getPdpPartition(pdpPartitionFile): 
	ret = list()
	for s in open(pdpPartitionFile):
		return ast.literal_eval(s)

def getLDE2StateMapping(led): 
	return led[2]	

def evaluateEachStatementIndexes(statement,x):
	y = x + [1]
	return sum([i[0] * i[1] for i in zip(statement, y)])

def evaluateStatementIndexes(statements,x):
	return [evaluateEachStatementIndexes(state,x) for state in statements]

def checkForEqulePartition(x,y):
	if x == y:
		return True
	else:
		return False 

def checkDependance(partition,statements,lde2StateMapping):
	xl = evaluateStatementIndexes(statements,list(partition))
	if xl[0] == xl[1]: 
		return True
	return False

def getBitVectorSize(upperLimits,lowerLimits,numberOfNestedLoops,numberofStatements):
	partitionSize = 1
	for i in range(numberOfNestedLoops):
		partitionSize *= (upperLimits[i] - lowerLimits[i])
	bitVectorSize = partitionSize*numberofStatements
	return bitVectorSize,partitionSize

def getBit(itrationVector, statement):
	bit = statement
	bit += sum([itrationVector[i]*bitBlocks[i+1] for i in range(numberOfNestedLoops)])
	return bit

def getBitVector(bit1,bit2):
	bitVector = BitArray(bitVectorSize)
	bitVector[bit1] = 1
	bitVector[bit2] = 1
	return bitVector

def addIndependantComponent(component):
	independantComponents.append(component)

def removeIndependantComponent():
	newIndependantComponents = list()
	for component in independantComponents:
		bit = getBit(component[0][0],component[0][1])
		if not globalBitVector[bit]: newIndependantComponents.append(component)
	return newIndependantComponents

def getElement(bit):
	itrationVector = [0]*len(bitBlocks)
	for i in range(len(bitBlocks)-1,-1,-1):
 		itrationVector[i] = bit%bitBlocks[i]
 		bit/=bitBlocks[i]


	#rranges = [i for i in reversed(ranges)]
	# for i in range(numberOfNestedLoops):
	# 	itrationVector.append(bit%rranges[i]+lowerLimits[i])
	# 	bit/=rranges[i] 
	return (itrationVector[:-1], itrationVector[-1])

def getComponent(bitVector):
	component = list()
	for bit in range(len(bitVector)):
		if bitVector[bit]: component.append(getElement(bit))

	return component

def getDependantComponent():
	for bitVector in dependantComponentsBitVector:
		dependantComponents.append(getComponent(bitVector))

	return dependantComponents
	

def getIndependantComponent():
	for bit in range(bitVectorSize):
		if not globalBitVector[bit]:
			independantComponents.append([getElement(bit)])

	return independantComponents

def addDependantComponent(component):
	itrationVector_statement1, itrationVector_statement2 = component
	bit1 = getBit(itrationVector_statement1[0], lde2StateMapping[itrationVector_statement1[1]])
	bit2 = getBit(itrationVector_statement2[0], lde2StateMapping[itrationVector_statement2[1]])

	for i in range(len(dependantComponentsBitVector)):
		if dependantComponentsBitVector[i][bit1]:
			#dependantComponents[i].append(tuple(itrationVector_statement2))
			dependantComponentsBitVector[i][bit2] = 1
			globalBitVector[bit2] = 1
			return
		elif dependantComponentsBitVector[i][bit2]:
			#dependantComponents[i].append(tuple(itrationVector_statement1))
			dependantComponentsBitVector[i][bit1] = 1
			globalBitVector[bit1] = 1
			return
	
	#dependantComponents.append([tuple(itrationVector_statement2),tuple(itrationVector_statement1)])
	dependantComponentsBitVector.append(getBitVector(bit1,bit2))
	globalBitVector[bit1] = 1
	globalBitVector[bit2] = 1
	return


def getBitBlocks():
	bitBlocks = [0]*(numberOfNestedLoops+1)
	bitBlocks[-1] = numberofStatements2
	for i in range(numberOfNestedLoops-1,-1,-1):
		bitBlocks[i] = ranges[i]*bitBlocks[i+1]
	return bitBlocks


def checkStatementWisePartition(partition): 

	x,y = partition[1],partition[2]
	# if checkForEqulePartition(x,y):
	# 	if checkDependance(partition,statements,lde2StateMapping):
	# 		#independantComponents.append([(x,lde2StateMapping[partition[0][0]][0]),(x,lde2StateMapping[partition[0][0]][1])])
	# 		addDependantComponent([(x,lde2StateMapping[partition[0][0]][0]),(x,lde2StateMapping[partition[0][0]][1])])
	# 	else:
	# 		addIndependantComponent([(x,lde2StateMapping[partition[0][0]][0])])
	# 		addIndependantComponent([(x,lde2StateMapping[partition[0][0]][1])])
	# 	return

	xl = evaluateStatementIndexes(statements,x)
	yl = evaluateStatementIndexes(statements,y)

	for i in range(numberofStatements):
		f = False
		for j in range(numberofStatements):
			if xl[i] == yl[j]:
				f = True
				addDependantComponent([(x,i),(y,j)])
	# 	if not f: addIndependantComponent([(x,i)])
	# for j in range(len(statements)):
	# 	if yl[j] not in xl:addIndependantComponent([(y,j)])

def spdp():
	map(checkStatementWisePartition, pdpPartition)
	return dependantComponentsBitVector, globalBitVector

def getFinalPartition():
	dependantComponents = getDependantComponent()
	independantComponents = getIndependantComponent()
	finalPartition = dependantComponents + independantComponents

	return finalPartition
