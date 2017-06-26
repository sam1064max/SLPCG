import sys

def writeMatrix(partition, numberOfNestedLoops, matrixFile):
	numberOfComponents = len(partition)
	matrixFile.write("int C[" + str(numberOfComponents+1) + "][" + str(max(map(len, partition))+1) + "][" + str(numberOfNestedLoops+1) + "] = ")
	matrixFile.write("{{{" + str(numberOfComponents) + "}}")

	for component in partition:
		matrixFile.write("\n,{{" + str(len(component)) + "}")
		for solution in component:
			matrixFile.write(",{" + ','.join(map(str,solution[0])) + "," + str(solution[1]) + "}")
		matrixFile.write("}")

	matrixFile.write("};")

def writeStatements(outPutFile, statements, loopVariablesList, numberOfNestedLoops):
		loopVariables = dict()
		for i in range(numberOfNestedLoops):
			loopVariables[loopVariablesList[i].strip()] = "index["+str(i)+"]"

		outPutFile.write("\nint nesting = " + str(numberOfNestedLoops) + ";\n");
		outPutFile.write("int index[" + str(numberOfNestedLoops) + "];\n");
		outPutFile.write("\n\n#pragma omp parallel for\n")
		outPutFile.write("for(int x = 1 ; x <= C[0][0][0] ; x++)\n")
		outPutFile.write("\tfor(int y = 1 ; y <= C[x][0][0] ; y++){\n")
		outPutFile.write("\t\tfor(int i = 0; i<nesting; i++)\n")
		outPutFile.write("\t\t\tindex[i] = C[x][y][i];\n")
		outPutFile.write("\t\tswitch(C[x][y][nesting]){\n")			
			
		case = 0
		for eachStatements in statements:
			newStatement = list()
			for s in eachStatements:
				if s in loopVariables.keys():
					newStatement.append(loopVariables[s])
				else:
					newStatement.append(s)
			outPutFile.write("\t\tcase " + str(case) + " : " + ''.join(newStatement))
			outPutFile.write("\n\t\t\tbreak;\n")
			case += 1

		outPutFile.write("\t\t}\n")
		outPutFile.write("\t}")


def writeFile(inputFile, outPutFile, partition, statements, numberOfNestedLoops, loopVariablesList):
	#statements = statements[2:]
	outPutFile = open(outPutFile, 'w')
	outPutFile.write("#include <omp.h>\n")
	f = True
	f2 = True
	for line in open(inputFile):
		if "#pragma scop" in line:
			f = False
		

		if f : outPutFile.write(line)
		elif f2 :
			writeMatrix(partition, numberOfNestedLoops, outPutFile)
			writeStatements(outPutFile, statements, loopVariablesList, numberOfNestedLoops)
			f2 = False
		if "#pragma endscop" in line:
			f = True
		




