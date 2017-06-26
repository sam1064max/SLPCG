import Parser
import Exhaustive
import SPDP
import Scheduler
import OpenMPGenerator
import sys
import multiprocessing
from bitstring import BitArray

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("logfile.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass    

sys.stdout = Logger()

def getBitVectorSize():
	partitionSize = 1
	for i in range(len(loopInfo)):
		partitionSize *= (loopInfo[i][2] - loopInfo[i][1])
	bitVectorSize = partitionSize*len(statementList)
	return bitVectorSize,partitionSize

tree, statementList = Parser.parseCode(sys.argv[1])
loopInfo,statementsInfo = Parser.getLoopInfo(tree)

log = open("logfile.log","w")
log.write("Parse Tree : ")
print >> log, tree
log.write("\n\nLoop Information : ")
print >> log, loopInfo

print "Statements: -------------------------------------------------------------------------------------------------------------------------"

for i in range(len(statementList)): 
	print i, "->", statementList[i]

lde = Parser.getLDEMapping(statementList, statementsInfo, SPDP.getLoopVariables(loopInfo))

log.write("\n\nLDEs : ")
print >> log, lde

numberOfLDEs = len(lde)

print "Number of LDEs :", numberOfLDEs, "---------------------------------------------------------------------------------------------------"

for i in lde.items(): print i

solutionsDict = dict()
solutions = list()
partition = list()

globalBitVector = BitArray(getBitVectorSize()[0])
dependantComponentsBitVector = list()

print "Bit Vectore Size =", getBitVectorSize()[0] 

for key in lde:
	print "\nProcessing LDE", key, "-----------------------------------------------------------------------------------------------------------"
	if len(lde[key])>3:
		solutionsDict[key] = Exhaustive.getSolutions(loopInfo, lde[key], key)
		print "Multidimentional array detected. Name =", key, ", Dimention =", len(lde[key])/3
		print "Number of base solutions pairs =", len(solutionsDict[key])
		log.write("\n\nSolutions for" + key + ": ")
		print >> log, solutionsDict[key]
		for i in range(1,len(lde[key])/3):
			solutionsDict[key] = Exhaustive.getIntersectionSolutions(loopInfo, lde[key][i*3:(i+1)*3], solutionsDict[key])
			print "Number of solutions pairs after", i, " intersections =", len(solutionsDict[key])
			log.write("\n\nSolutions for" + key + ": ")
			print >> log, solutionsDict[key]
	else:
		solutionsDict[key] = Exhaustive.getSolutions(loopInfo, lde[key], key)
		print "Single dimentional array detected. Name =", key, ", Dimention =", len(lde[key])/3
		print "Number of solutions pairs (Iteration Level) =", len(solutionsDict[key])
		log.write("\n\nSolutions for " + key + ": ")
		print >> log, solutionsDict[key]

	SPDP.init(loopInfo, statementsInfo, solutionsDict[key], lde[key], dependantComponentsBitVector, globalBitVector, len(statementList))
	dependantComponentsBitVector, globalBitVector = SPDP.spdp()

	#print "Number of dependant components =", len(dependantComponentsBitVector)
	print "Maximum parallelism achived (Statement Level) =", len(dependantComponentsBitVector) - sum(globalBitVector) + getBitVectorSize()[0]
	print "Length of longest component (Statement Level) =", max(map(sum,dependantComponentsBitVector))
	print "Number of component chains (Statement Level) =", len(dependantComponentsBitVector)
	print "Number of independant components (Statement Level) =", getBitVectorSize()[0] - sum(globalBitVector)

	solutions+= solutionsDict[key]

	print >> log, "\n\nDependant Components BitVector : "

	for i in dependantComponentsBitVector: print>> log, i

print "\nFinal Result -----------------------------------------------------------------------------------------------------------"
print "Maximum parallelism achived =", len(dependantComponentsBitVector) - sum(globalBitVector) + getBitVectorSize()[0]
print "Length of longest component =", max(map(sum,dependantComponentsBitVector))
print "Number of component chains =", len(dependantComponentsBitVector)
print "Number of independant components =", getBitVectorSize()[0] - sum(globalBitVector)

partition = SPDP.getFinalPartition()

print >> log, "\n\nFinal Statewise Partition ---------------------------------------------------------"

for i in partition: print>> log, i

if len(sys.argv)> 3 and sys.argv[3] == "-schedule":
	print "\nScheduler is activated------------------------------------------------------------------------------------------------"
	if len(sys.argv)> 4:
		if sys.argv[4] == "auto":
			print "Autodetected number of cores : ", multiprocessing.cpu_count()
			partition = Scheduler.loadBalance(partition, multiprocessing.cpu_count())
			print "Partitions has been balanced into", multiprocessing.cpu_count(), "threads."
			print "Size of longest components :", max(map(len,partition))
		else:
			print "Number of threads are given user. Cores : ", sys.argv[4]
			partition = Scheduler.loadBalance(partition, int(sys.argv[4]))
			print "Partitions has been balanced into", sys.argv[4], "threads."
			print "Size of longest components :", max(map(len,partition))
	print >> log, "\n\nFinal Scheduled Partition ---------------------------------------------------------"
	for i in partition: print>> log, i

print "Generating Parallel Code -------------------------------------------------------------------------------------------------------"
OpenMPGenerator.writeFile(sys.argv[1], sys.argv[2], partition, statementList, SPDP.numberOfNestedLoops, SPDP.getLoopVariables(loopInfo))
print "OpenMP code has been written to", sys.argv[2],"."
print "Use \"g++ -openmp <filename>\" to compile OpenMP code."

