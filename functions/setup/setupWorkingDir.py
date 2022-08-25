#!/usr/bin/env python3

# imports of libraries
import os
from ..tool.toolColoredOutput import printError

def setupDirs (currentUnixTime, inputFilePath, isMicrosoft, isRHEL, isVmWare):
	# Get the filename of the input file
	inputFile = os.path.basename(inputFilePath)

	sanityCheck = int(isMicrosoft) + int(isRHEL) + int(isVmWare)

	if sanityCheck != 1:
		printError("Only one type is supported when creating directories!")
		exit(1)

	# Check what working directory needs to be created
	# Works only with one!
	if isMicrosoft:
		workingDir = "./output/Microsoft/" + inputFile + "/" + str(currentUnixTime)
	elif isRHEL:
		workingDir = "./output/RedHat/" + inputFile + "/" + str(currentUnixTime)
	elif isVmWare:
		workingDir = "./output/VMWare/" + inputFile + "/" + str(currentUnixTime)
	else:
		workingDir = "./output/Misc/" + inputFile + "/" + str(currentUnixTime)

	# Create working directory
	os.makedirs(workingDir, exist_ok=True)

	# Create mount point for ISO
	os.makedirs("./extractedISO", exist_ok=True)

	return workingDir