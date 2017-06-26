# -----------------------------------------------------------------------------
# Parser.py
#
# A simple For loop parser for c
# -----------------------------------------------------------------------------

import ply.yacc as yacc
import sys

tokens = [
	'ID','NUMBER',
	'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
	'LPAR','RPAR', 'LT', 'GT', 'LTET',
	'GTET', 'ET', 'SEMC', 'LSPAR', 'RSPAR', 'INCRE',
	'DECRE', 'LCPAR', 'RCPAR', 'ALL'
	]

reserved = {
	'for' : 'FOR'
}

tokens += reserved.values()
# Tokens

t_FOR     = r'for'
t_SEMC    = r';'
t_LCPAR   = r'{'
t_RCPAR   = r'}'
t_EQUALS  = r'='
t_LPAR    = r'\('
t_RPAR    = r'\)'
#t_ALL     = r'[^((?!for))]|[a-zA-Z0-9_\[\]\+\*\-\/\=\>\<;]+'

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
#t_NAME    = r'[^((?!for))][a-zA-Z_][a-zA-Z0-9_]*|[a-zA-Z_][a-zA-Z0-9_]*'
#t_NUMBER  = r'[0-9]'
t_LT      = r'<'
t_GT      = r'>'
t_LTET    = r'<='
t_GTET    = r'>='
t_ET      = r'=='
t_LSPAR   = r'\['
t_RSPAR   = r'\]'
t_INCRE   = r'\+\+'
t_DECRE   = r'--'



t_NUMBER    = '(-)*\d+'

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	if t.value in reserved:
		t.type = reserved[ t.value ]
	return t

# def t_NUMBER(t):
#     r'\d+'
#     try:
#         t.value = int(t.value)
#     except ValueError:
#         print("Integer value too large %d", t.value)
#         t.value = 0
#     return t

# Ignored characters
t_ignore = " \t\n"

# def t_newline(t):
#     r'\n+'
#     t.lexer.lineno += t.value.count("\n")
	
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)
	
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
	('left','PLUS','MINUS'),
	('left','TIMES','DIVIDE'),
	('right','UMINUS'),
	)

# dictionary of names
names = { }

def p_statement_for(t):
	'statement : FOR LPAR expression SEMC expression SEMC expression RPAR statement'
	t[0] = ['for', t[3], t[5], t[7], t[9]]
	return t[0]

def p_statement_curlys(t):
	'statement : LCPAR statement RCPAR'
	t[0] = t[2]

# def p_statement_assign_scaler(t):
# 	'statement : ID EQUALS expression SEMC'
# 	t[0] = [t[1],t[2],t[3]]

# def p_statement_assign_scaler(t):
# 	'statement : ID EQUALS expression SEMC statement'
# 	t[0] = [t[1],t[2],t[3]]

def p_statement_assign(t):
	'statement : expression EQUALS expression SEMC'
	t[0] = [t[1],t[2],t[3]]

def p_statement_assign_next(t):
	'statement : expression EQUALS expression SEMC statement'
	t[0] = [[t[1],t[2],t[3]],t[5]]

def p_expression_equal(t):
	'expression : ID EQUALS NUMBER'
	t[0] = [t[1],t[2],t[3]]

# def p_expression_equal_negative(t):
#     'expression : ID EQUALS MINUS NUMBER'
#     t[0] = (t[1],"=",-1*int(t[4]))

def p_expression_less_than_equal_to(t):
	'expression : ID LTET NUMBER'
	t[0] = [t[1],t[2],t[3]]

def p_expression_less_than(t):
	'expression : ID LT NUMBER'
	t[0] = [t[1],t[2],t[3]]

def p_expression_increment(t):
	'expression : ID INCRE'
	t[0] = [t[1],"+",1]

def p_statement_array_name(t):
	'expression : ID expression'
	t[0] = [t[1],t[2]]

def p_statement_array_index(t):
	'expression : LSPAR expression RSPAR expression'                  
	t[0] = [t[2],t[4]]

def p_statement_array_index_next(t):
	'expression : LSPAR expression RSPAR'                 
	t[0] = t[2]

def p_statement_expr(t):
	'statement : expression'
	t[0] = t[1]

def p_expression_expression(t):
	'''expression : ID
				  | NUMBER'''
	#print t[1]
	t[0] = t[1]

def p_expression_binop_plus_minus(t):
	'''expression : expression PLUS expression
				  | expression MINUS expression'''
	t[0] = [t[1],t[2],t[3]]
	# if t[2] == '+'  : t[0] = t[1] + t[3]
	# elif t[2] == '-': t[0] = t[1] - t[3]

def p_expression_binop_times_divide(t):
	'''expression : expression TIMES expression
				  | expression DIVIDE expression'''
	t[0] = [t[1],t[2],t[3]]
	# elif t[2] == '*': t[0] = t[1] * t[3]
	# elif t[2] == '/': t[0] = t[1] / t[3]

def p_expression_uminus(t):
	'expression : MINUS expression %prec UMINUS'
	#print(t[0],t[1],t[2])
	t[0] = -int(t[2])
	

# def p_expression_group(t):
#     'expression : LPAR expression RPAR'
#     t[0] = t[2]

# def p_expression_number(t):
#     'expression : NUMBER'
#     t[0] = t[1]

# def p_expression_name(t):
#     'expression : NAME'
#     try:
#         t[0] = names[t[1]]
#     except LookupError:
#         print("Undefined name '%s'" % t[1])
#         t[0] = 0

def p_error(t):
	print("Syntax error at '%s'" % t.value,t)

parser = yacc.yacc()


##########################################################################################

def parseCode(file):
	f = False
	s = list()
	with open(file) as file:
		lines = file.read().splitlines()
	for line in lines:
		if "#pragma endscop" in line:
			f = False
		if f : s.append(line)
		if "#pragma scop" in line:
			f = True
		
	statementList = list()
	for i in s:
		if "[" in i:
			statementList.append(i.strip())
	s = "\n".join(s)
	lexer.input(s)
	# for tok in lexer:
	#     print(tok)
	tree = (parser.parse(s))

	return tree, statementList

# --------------------------------------------------------------------------------------------------

#print(tree)

#def getCycles(tree):
	
#tree = parseCode(sys.argv[1])
loopInfo = list()
statementsInfo = list()

#def genStatementsInfo(tree):


def genLoopInfo(tree):
	#print tree[0]
	if 'for' in tree[0]:
		#print [tree[1][0],tree[1][2],tree[2][2]]
		loopInfo.append([tree[1][0],int(tree[1][2]),int(tree[2][2])])
		genLoopInfo(tree[4])
	else:
		for i in tree:
			statementsInfo.append(i)
		return
		
def getLoopInfo(tree):
	genLoopInfo(tree)
	return loopInfo,statementsInfo

def getLoopVariables(loopInfo):
	return [i[0] for i in loopInfo]

def getStatements(file):
	l = [i for i in open(file)]
	statementList = list()
	for i in l:
		if "[" in i:
			statementList.append(i.strip())

	return statementList

def atLeastOneloopVar(var, loopVariables):
	for loopVar in loopVariables:
		if loopVar in var:
			return True
	return False


def getLDEMapping(statementList, statementsInfo, loopVariables):
	lde = dict()
	for i in range(len(statementList)):
		var = statementList[i].split("=")
		var = map(lambda x: x.strip(), var)
		varl, varr = var[0].strip(), var[1].strip()
		if "[" in varl:
			array = varl[0]
			orig = varl.split("]")
			for j in range(len(orig)-1):
				varl = orig[j] + "]"
				if array not in lde.keys():
					lde[array] = [dict() for _ in range(3*(len(orig)-1))]
					for k in range((len(orig)-1)):
						lde[array][2+k*3] = [None for _ in range(2)]
				for loopVar in loopVariables:
					if loopVar in varl:
						index = varl.index(loopVar)
						if varl[index-1] == "*":
							if varl[index-3] == "-":
								lde[array][j*3][loopVar] = -int(varl[index-2])
							else:
								lde[array][j*3][loopVar] = int(varl[index-2])
						elif varl[index+1] == "*":
							lde[array][j*3][loopVar] = int(varl[index+2])
						else:
							lde[array][j*3][loopVar] = 1
					elif atLeastOneloopVar(varl, loopVariables):
						lde[array][j*3][loopVar] = 0

					ele = varl[varl.index("[")+1:varl.index("]")].split("+")
					if ele[-1].isdigit():
						lde[array][j*3]["con"] = int(ele[-1])
					else:
						lde[array][j*3]["con"] = 0
					lde[array][j*3+2][0] = i


		if "[" in varr:
			array = varr[0]
			orig = varr.split("]")
			for j in range(len(orig)-1):
				varr = orig[j] + "]"
				if array not in lde.keys():
					lde[array] = [dict() for _ in range(3*(len(orig)-1))]
					for k in range((len(orig)-1)):
						lde[array][2+k*3] = [None for _ in range(2)]
				for loopVar in loopVariables:
					if loopVar in varr:
						index = varr.index(loopVar)
						if varr[index-1] == "*":
							if varr[index-3] == "-":
								lde[array][j*3+1][loopVar] = -int(varr[index-2])
							else:
								lde[array][j*3+1][loopVar] = int(varr[index-2])
						elif varr[index+1] == "*":
							lde[array][j*3+1][loopVar] = int(varr[index+2])
						else:
							lde[array][j*3+1][loopVar] = 1 
					elif atLeastOneloopVar(varr, loopVariables):
						lde[array][j*3+1][loopVar] = 0

					ele = varr[varr.index("[")+1:varr.index("]")].split("+")
					if ele[-1].isdigit():
						lde[array][j*3+1]["con"] = int(ele[-1])
					else:
						lde[array][j*3+1]["con"] = 0

					ele = varr[varr.index("[")+1:varr.index("]")].split("-")
					if ele[-1].isdigit():
						lde[array][j*3+1]["con"] = -int(ele[-1])
					else:
						lde[array][j*3+1]["con"] = 0

					lde[array][j*3+2][1] = i

	for ele in lde.keys():
		if len(lde[ele][0])<= 1 or len(lde[ele][1])<= 1:
			del lde[ele]
	return lde
		

