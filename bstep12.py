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

(options,args) = parser.parse_args()

# if input assigned
if options.input:
	inputfile = options.input
else:
	inputfile = "train.txt"#data/train20.txt"

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

	print elements
	return elements

def checkRoot(givenroot):
	if not givenroot:
		return ""
	regex = re.compile("@[^@]+")
	groupsfound = regex.findall(givenroot)
	print groupsfound[-1] + "fuaaaaaaaaaaaaaaaaaaaaa"
	return groupsfound[-1]


# given line binarize
def binarizeLong(line, givenroot,useroot):
	givenroot = checkRoot(givenroot)
	temproot = givenroot
	if useroot:
		left = " (" + givenroot + " ("
	else:
		givenroot = ""
		left = " ("
	right = ")"
	output = ""

	# split the line into tag and children
	elements = getSubStrings(line[1:-1])

	# if not at terminal
	if elements != False:

		# if there is one element in the line besides the tag
		if len(elements) == 2:
			print "len 2"
			print elements
			# left side is tag
			left += elements[0]

			# binarize single element and put into output
			output = left + binarizeLong(elements[1], "",False)[0] + right

		# if more elements in the line
		elif len(elements) == 3:
			print "danger danger high voltage"
			print elements
			
			# original element on the left added
			left += elements[0]

			# binarize left side
			temp1 = binarizeLong(elements[1], "@" + elements[0] + "->",False)
			# update variables
			givenroot += temp1[1]
			templist = temp1[0]
			#output += temp1[0]

			# binarize the right side 
			for element in elements[2:]:
				temp2 = binarizeLong(element, givenroot,True)
				templist += temp2[0]
				#update root
				givenroot += temp2[1]

			# finalize output
			output += left + output + templist + right
		else:
			print "ELEMENT X SHEET"
			print elements
			
			# original element on the left added
			left += elements[0]

			# binarize left side
			temp1 = binarizeLong(elements[1], "@" + elements[0] + "->",False)
			# update variables
			givenroot += temp1[1]
			templist = temp1[0]
			#output += temp1[0]

			# binarize the right side 
			for element in elements[2:]:
				temp2 = binarizeLong(element, givenroot,True)
				templist += temp2[0]
				#update root
				givenroot += temp2[1]

			# finalize output
			output += left + output + templist + right
	#if at terminal
	else:
		linesp = line.split()
		givenroot += "_" + linesp[0][1:]
		output += line[1:-1]
		output = left + output + right

	print output + " hmmm"
	if not useroot:
		givenroot = temproot + givenroot
	return [output,givenroot]
		


	 
############## main code ###############
for line in inputlines:
	if line == "\n":
		outputfile.write('\n')
		continue
	print binarizeLong(line,"",False)[0].strip()
