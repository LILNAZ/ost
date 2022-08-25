#!/usr/bin/env python3

# imports of libraries

import subprocess
import os

def getFileExtensionAndOccurrences (inputFile):
	if os.path.exists(inputFile):
		cmd = ["./functions/tool/bashNumberOfFileExtension.sh", inputFile]
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		output, error = proc.communicate()

		return output.decode('ascii').strip()
	else:
		return ""

def getFileExtension (inputFile):
	#returns file extension in lower case
	return os.path.splitext(inputFile)[1].lower()