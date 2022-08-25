#!/usr/bin/env python3

# imports of libraries
from os.path import exists
import string

# Tools
from ..tool.toolColoredOutput import *

def validateInput (inputFile, inputHash, isMicrosoft, isRHEL, isVmWare):
	inputValid = True

	# Check if the input file exist
	inputFileExist = exists(inputFile)

	if not inputFileExist:
		printError("File not found!")
		inputValid = False

	# Check if the hash is correct
	inputHashIsHex = all(c in string.hexdigits for c in inputHash)
	inputHashLength = len(inputHash)

	if not inputHashIsHex and inputHashLength == 64:
		inputValid = False
	elif inputHashLength != 64:
		inputValid = False

	# check if only one type has been used
	numberOfType = int(isMicrosoft) + int(isRHEL) + int(isVmWare)

	if numberOfType < 1:
		printError("Need one type: -m, --microsoft, -r, --rhel, -v, --vmware")
		inputValid = False
	elif numberOfType > 1:
		printError("Need one type: -m, --microsoft, -r, --rhel, -v, --vmware")
		inputValid = False
	

	if inputValid:
		printOk("Input flags OK!")
	else:
		printError("Input flags not ok!")
		exit(1)

	