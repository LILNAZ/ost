#!/usr/bin/env python3

# imports of libraries
import os
import re

# Tools
from ..tool.toolUnixTime import getCurrentUnixTime
from ..tool.toolColoredOutput import *
from ..tool.toolYesNoQuestion import questionDefaultYes

def cleanUp (workingDir):

	# Remove temp files
	tmpFiles = []
	foundTmpFiles = False
	
	# Check if the process left any temp files
	for (root, dirs, file) in os.walk(workingDir):
		for f in file:
			if re.search(r'tmp.*', f):
				tmpFiles.append(f)
				foundTmpFiles = True

	# If temp files where found ask if they should be deleted
	if foundTmpFiles:
		removeTmpFiles = questionDefaultYes("INFO", "Do you want to delete temporary files (tmp.* in " + workingDir + " )?", 1)
		if removeTmpFiles:
			for files in tmpFiles:
				os.remove(workingDir + "/" + files)


def finalSteps (workingDir, startTime):
	# Get current time for the end of the script
	endTime = getCurrentUnixTime()
	# Calculate the length in secounds it took to perform the scripts function
	totalExecutionTime = endTime - startTime
	printInfo("Execution took: " + str(totalExecutionTime) + " second(s)")


	# Clean up of temporary files
	cleanUp(workingDir)