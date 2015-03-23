#
#	Students	: Philip Bouman , Alex Khawalid
#	Studentnr	: 10668667		, 10634207
#	Assignment B: step 2 NTMI
#	Date		: 06-02-2015
#
# Command-line:
# (1): python bstep2.py -i [non-binarized] -o [binarized] -c [number] -v [number]
from optparse import OptionParser

# parse options
parser = OptionParser()
parser.add_option("-i", "--input", dest="input")
parser.add_option("-o", "--output", dest="output")
parser.add_option("-c", "--horizontal", dest="horizontal")
parser.add_option("-v", "--vertical", dest="vertical")

(options,args) = parser.parse_args()

# if input assigned
if options.input:
	inputfile = options.input
else:
	inputfile = "data/small.txt"

# if output assigned
if options.output:
	outputfile = options.output
else:
	outputfile = "test.txt"

# if horizontal assigned
if options.horizontal:
	horder = options.horizontal
else:
	horder = 2

# if vertical assigned
if options.vertical:
	vorder = options.vertical
else:
	vorder = 2

# read files and init output file
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

# get tag from terminal node
def getTerminalTag(element):
	elements = element.split()
	return elements[0][1:]

# update list of siblings
# given a list if the number of siblings is
# lower than horizontal order, append
# otherwise discard first element and then append
def updateSibilings(siblings, newsib):
	if len(siblings) < horder:
		siblings.append(newsib)
	else:
		siblings.append(newsib)
		siblings = siblings[1:]
	return siblings


# binarize line
# parent = tag of parent node
def binarizeLeft(line, parent):
	# init variables
	left = " ("
	right = ")"
	output = ""
	root = ""

	# get tree elements
	elements = getSubStrings(line[1:-1])

	# if not terminal node
	if elements != False:
		# if only 1 child
		if len(elements) == 2:
			# if vertical order is 2 and not root node add parent 
			if vorder == 2 and parent != "":
				output += elements[0] + "^" + parent + " "
			# if not, dot not add parent
			else:
				output += elements[0] + " "

			# binarize only child and update output and root
			temp = binarizeLeft(elements[1],elements[0])
			output += temp[0]
			root = elements[0]

		# if 2 children or more
		elif len(elements) > 2:
			# update root element
			root = elements[0]

			# if vertical order is 2 add parent
			if vorder == 2:
				output += elements[0] + "^" + parent + " "
			# if not do not add parent
			else:
				output += elements[0] + " "

			# binarize first element and get tag
			# put tag in siblings
			temp = binarizeLeft(elements[1],root)
			output += temp[0]
			lastsib = temp[1]
			siblings = [lastsib]

			# binarize rest of children and add siblings
			for el in elements[2:]:
				# if vertical order is 2 add parent and siblings
				if vorder == 2:
					output += " (@" + root + "^" + parent + "->_" + "_".join(siblings) + " "
				# if not, only add siblings
				else:
					output += " (@" + root + "->_" + "_".join(siblings) + " "

				# get binarized line and update siblings
				temp = binarizeLeft(el,root)
				output += temp[0]
				lastsib = temp[1]
				siblings = updateSibilings(siblings,lastsib)
				right += ")"
	# terminal node
	else:
		# return line and head of node
		return [line,getTerminalTag(line)]

	# return output
	return [left + output + right,root]




############## main code ###############
for line in inputlines:
	if line == "\n":
		outputfile.write('\n')
		continue
	outputfile.write(binarizeLeft(line,"")[0].strip() + "\n")

outputfile.close()
