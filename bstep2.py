#
#	Students	: Philip Bouman , Alex Khawalid
#	Studentnr	: 10668667		, 10634207
#	Assignment A: step 4 NTMI
#	Date		: 06-02-2015
#
# Command-line:
# (1): python assignment4.py -c [trainset] -t [testset] -s [yes|no] -p [predictedtagsfile]
import re
from optparse import OptionParser

# parse options
parser = OptionParser()
parser.add_option("-i", "--input", dest="input")
parser.add_option("-o", "--output", dest="output")
parser.add_option("-h", "--output", dest="horizontal")
parser.add_option("-v", "--output", dest="vertical")

(options,args) = parser.parse_args()

# if input assigned
if options.input:
	inputfile = options.input
else:
	inputfile = "data/train20.txt"

# if output assigned
if options.output:
	outputfile = options.output
else:
	outputfile = "test.txt"

# if output assigned
if options.output:
	horder = options.horizontal
else:
	horder = 2

# if output assigned
if options.output:
	vorder = options.vertical
else:
	vorder = 2



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

def binarizeRight(elements, givenroot):
	# first left of right does not contain binarization
	left = binarizeLeft(elements[0])
	temphead = left.split()[0][1:]
	right = ""
	output = " "
	
	# every right is a left with binarization
	for el in elements[1:]:
		givenroot += "_" + temphead
		output += givenroot + " " + binarizeLeft(el) 
		right += ")"

	return left + output + right


def binarizeLeft(line):
	# init variables
	left = " ("
	right = ")"
	output = ""

	# get tree elements
	elements = getSubStrings(line[1:-1])

	# if non terminal node
	if elements != False:

		# add root to left
		left += elements[0]

		# if more than one node
		if len(elements) > 2:
			output = binarizeRight(elements[1:],"(@" + elements[0] + "->")
		# else if single node besides tag
		else:
			left += binarizeLeft(elements[1])
	# if terminal node
	else:
		output += line[1:-1]

	return left + output + right

############## main code ###############
for line in inputlines:
	if line == "\n":
		outputfile.write('\n')
		continue
	outputfile.write(binarizeLeft(line).strip() + "\n")
