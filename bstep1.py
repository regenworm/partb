#
#	Students	: Philip Bouman , Alex Khawalid
#	Studentnr	: 10668667		, 10634207
#	Assignment B: step 1 NTMI
#	Date		: 06-02-2015
#
# Command-line:
# (1): python bstep1.py -i [non-binarized] -o [binarized]
from optparse import OptionParser

# parse options
parser = OptionParser()
parser.add_option("-i", "--input", dest="input")
parser.add_option("-o", "--output", dest="output")

(options,args) = parser.parse_args()

# if input assigned
if options.input:
	inputfile = options.input
else:
	inputfile = "data/test20.txt"

# if output assigned
if options.output:
	outputfile = options.output
else:
	outputfile = "test.txt"

inputfile = open(inputfile, 'r')
inputlines = inputfile.readlines()
inputfile.close()
outputfile = open(outputfile, 'w')

# get substrings
# line is of the form TAG followed by children
# line = TAG (..) (..) (..)
# elements returns these elements in a list
def getSubStrings(line):
	openCount = 0
	closeCount = 0
	lastStart = 0
	elements = []
	i = 0
	char = line[i]

	if "(" not in line:
		return False


	while char != "(":
		i+= 1
		if i > len(line)-1:
			return False
		char = line[i]


	lastStart = i
	elements.append(line[:lastStart-1])

	while i < len(line):
		if line[i] == " ":
			i += 1
			continue
		elif line[i] == "(":
			openCount += 1
		elif line[i] == ")":
			closeCount += 1
		if openCount-closeCount == 0 and openCount > 0:
			elements.append(line[lastStart:i+1].strip())
			lastStart = i + 1
		i += 1

	return elements

def getTerminalTag(element):
	elements = element.split()
	return elements[0][1:]

def updateSibilings(siblings, newsib):
	if len(siblings) < 2:
		siblings.append(newsib)
	else:
		siblings.append(newsib)
		siblings = siblings[1:]
	return siblings


def binarizeLeft(line, parent):
	# init variables
	left = " ("
	right = ")"
	output = ""
	root = ""

	# get tree elements
	elements = getSubStrings(line[1:-1])
	if elements != False:
		# if only 1 child
		if len(elements) == 2:
			output += elements[0] + " "
			temp = binarizeLeft(elements[1],elements[0])
			output += temp[0]
			root = elements[0]

		# if 2 children or more
		elif len(elements) > 2:
			# get root element of this level
			root = elements[0]
			output += root + " "

			# binarize first element and get tag
			temp = binarizeLeft(elements[1],root)
			output += temp[0]
			lastsib = temp[1]
			siblings = [lastsib]

			# add siblings to other elements
			for el in elements[2:]:
				output += " (@" + root + "->_" + "_".join(siblings) + " "
				temp = binarizeLeft(el,root)
				output += temp[0]
				lastsib = temp[1]
				siblings = updateSibilings(siblings,lastsib)
				right += ")"
	# terminal node
	else:
		return [line,getTerminalTag(line)]

	#print output

	return [left + output + right,root]


############## main code ###############
for line in inputlines:
	if line == "\n":
		outputfile.write('\n')
		continue
	outputfile.write(binarizeLeft(line,"")[0].strip() + "\n")
