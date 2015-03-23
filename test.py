#######################################################
#	Pepijn van Diepen
#   Studentennummer: 10537473
#   Email: pepijnvandiepen@gmail.com
#
#   Joris Baan
#   Studentennummer: 10576681
#   Email: jsbaan@gmail.com
# 
#	This code has been tested on Python 2.7.6
# 	Instruction on testing can be found in the report
#
#	Binarization (with markovization depth specified)
#######################################################

# Import required components
import argparse
import time
import sys
import re
import inspect

if __name__ == "__main__":
	# Parse command line arguments
	parser = argparse.ArgumentParser(description = "Enter the command lines as \
	 specified in the assignments, only use underscores instead of dashes. \
	 The answer to the corresponding question will be showed")
	parser.add_argument('-H', type = int, help = "[number]")
	parser.add_argument('-V', type = int, help = "[number]")
	parser.add_argument('-input', help = "[non-binarized]")
	parser.add_argument('-output', help = "[binarized]")
	args = parser.parse_args()

	# When not enough arguments are given, print the parser description 
	if len(sys.argv) < 2:
		print "Usage: python b_step2 -h [number] -v [number] -input [non_binarized] -output [binarized]"			
		sys.exit(0)	

	# if input assigned
	if args.input:
		inputfile = options.input
	else:
		inputfile = "data/train20.txt"

	# if output assigned
	if args.output:
		outputfile = options.output
	else:
		outputfile = "test.txt"

	# Run binarization model
	if args.H and args.V:
		h = args.H
		v = args.V

		# load files
		nonBinarizedFile = open(inputfile)
		nonBinarized = nonBinarizedFile.readlines()
		output = open(outputfile, 'w')

		# remove empty lines and split sentences
		nonBinarized = " ".join(nonBinarized)
		nonBinarized = nonBinarized.replace("\n", "")
		nonBinarized = nonBinarized.split("  ")
		binarized = [];
		
		def printL(string):
		    """Returns the current line number in our program."""
		    print inspect.currentframe().f_back.f_lineno, string

		def getMatchingBracketIdx(phrase):
			# Calculate the index of the bracket matching the first opening bracket
			parIndex = 0
			parOpen = 1
			parClosed = 0 
			for char in list(re.search(r'\((.*)\)', phrase).group(1)):
				if char == "(":
					parOpen += 1
				if char == ")":
					parClosed += 1
				if parOpen - parClosed == 0:
					parIndex = parClosed
					break
			return parIndex

		def binarizeSentence(sentence):
			binarizedSentence = []

			# initialize ROOT
			phrase = re.search(r'\((.*)\)', sentence).group(1)
			phrase = phrase.split()
			binarizedSentence.append(phrase[0])
			# Replace meaningful comma's and quotationmarks with distinctive characters
			phrase = " ".join(phrase[1:]).replace(",", "+").replace("'", '"')

			# Activate recursion
			binarizedSentence = binarizePhraseHoly(binarizedSentence, phrase)
			# Delete commas, quotationmarks and replace square brackets for parentheses (also change the distinctive characters back to the originals)
			return str(binarizedSentence).replace('[', '(').replace(']', ')').replace("'", "").replace(",", "").replace("+", ",").replace('"',"'")
			
		# input is of the form POS(children)
		def binarizePhraseHoly(binarizedSentence, phrase):
			# Calculate the index of the bracket matching the first opening bracket
			parIndex = getMatchingBracketIdx(phrase)

			# Initialize left and right part of phrase
			leftPhrase = ""
			rightPhrase = ""

			# In case there is only one child (only a left phrase)
			if(parIndex == 0):
				leftPhrase = re.search(r'\((.*)\)', phrase).group(1)

			# Assign the first paranthesed phrase to the left child, and the remainder to the right child
			else:
				splittedPhrase = phrase.split(")", parIndex)
				# Determine left phrase
				leftPhrase = ")".join(splittedPhrase[0:parIndex]) + ") "
				leftPhrase = re.search(r'\((.*)\)', leftPhrase).group(1)
				# Determine right phrase
				rightPhrase = ") ".join(splittedPhrase[parIndex:])

			leftPhrase = leftPhrase.split()
			
			# Check whether the given phrase has no children (BASE CASE 1)
			if len(leftPhrase) == 2:
				binarizedSentence.append(leftPhrase)

			# If more exploring is to be done; expand parent node and create new child
			else:
				# Vertical markovization
				tag = leftPhrase[0] + '^' + binarizedSentence[0].replace('@', '')
				tag = tag.split("^")
				# Get the 0-v of the tag sequence (cut off redundand parents)
				tag = "^".join(tag[0:v])
				binarizedSentence.append([tag])

				leftPhrase = " ".join(leftPhrase[1:])
				# Replace old child with new more explored version of it
				binarizedSentence[1] = binarizePhraseHoly(binarizedSentence[1], leftPhrase)

			# In case a right phrase is present 
			if rightPhrase is not "":
				# Determine name of the new child
				if "@" in binarizedSentence[0]:
					# Horizontal markovization 
					splittedSen = binarizedSentence[0].split('_')
					# 
					horizontalDepth = len(splittedSen)-1
					# In case h is 1; adds only the last tag
					if h == 1:
						newParent = splittedSen[0] + "_" + binarizedSentence[1][0]
					# In case the tag sequences length is within the bounds of h
					elif (horizontalDepth) >= h:
						newParent = splittedSen[0] + "_" + "_".join(splittedSen[2:]) + "_" + binarizedSentence[1][0].split('^')[0]
					else:
					# When no cutting in the tag sequence is needed (limit is not yet reached)
						newParent = binarizedSentence[0] + "_" + binarizedSentence[1][0].split('^')[0]
				else:
					newParent = "@" + binarizedSentence[0] + "->_" + binarizedSentence[1][0].split('^')[0]

				# Add child
				binarizedSentence.append([newParent])
				rightPhrase = newParent + rightPhrase 

				# Check whether the given phrase has no children (BASE CASE 2)
				if len(rightPhrase.split()) == 3:
					rightPhrase = re.search(r'\((.*)\)', rightPhrase).group(1)
					binarizedSentence[2].append([rightPhrase])
					return binarizedSentence
				else:
					binarizedSentence[2] = binarizePhraseHoly(binarizedSentence[2], rightPhrase)
				
			# Return completely explored child (this is done recursively so the last return is the complete binarized sentence)
			return binarizedSentence

		start = time.time()
		print "Please wait while "+ str(args.input) + " gets binarized.."
		# for sentence in nonBinarized:
		# 	output.write(binarizeSentence(sentence) + '\n\n')
		# print binarizeSentence(nonBinarized[2])
		# print "Binarization process took", time.time()-start, "seconds."
		# print "The binarized sentences are save to", str(args.output)

		toolbar_width = (len(nonBinarized)/400)+1

		# setup toolbar
		sys.stdout.write("[%s]" % (" " * toolbar_width))
		sys.stdout.flush()
		sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['


		for i in xrange(len(nonBinarized)):
		    # time.sleep(0.1) # do real work here
		    output.write(binarizeSentence(nonBinarized[i]) + '\n\n')
		    # update the bar
		    if(i%400 == 0):
			    sys.stdout.write("-")
			    sys.stdout.flush()

		sys.stdout.write("\n")
		print "Binarization process took", time.time()-start, "seconds."
		print "The binarized sentences are save to", str(args.output)