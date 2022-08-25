#!/usr/bin/env python3

# imports of libraries
from .toolColoredOutput import *

def questionDefaultYes (textType, text, iterations):
	# Set Up colors
	Color_Off='\033[0m'		# Text Reset
	errText='\033[0;31m'	# Red
	okText='\033[0;32m'		# Green
	warnText='\033[0;33m'	# Yellow
	err='\033[1;31m'		# BOLD Red
	ok='\033[1;32m'			# BOLD Green
	warn='\033[1;33m'		# BOLD Yellow
	info='\033[1;36m'		# Cyan BOLD

	# Determine what text type is used
	if textType.upper() == "OK":
		message = ok + "OK: " + okText + text + Color_Off
	elif textType.upper() == "WARNING":
		message = warn + "WARNING: " + warnText + text + Color_Off
	elif textType.upper() == "ERROR":
		message = err + "ERROR: " + errText + text + Color_Off
	else:
		message = info + "INFO: " + Color_Off + text

	numberOfAnsweredIterations = 0

	while numberOfAnsweredIterations < iterations:
		response = input(message + info + " (YES or no): " + Color_Off)
		if any(response.lower() == f for f in ["yes", "y", "1", "ye"]):
			return True
			
		elif any(response.lower() == f for f in ["no", "n", "0"]):
			return False

		else:
			numberOfAnsweredIterations += 1
			if numberOfAnsweredIterations < iterations:
				printWarn("Please Answer yes or no")
			else:
				printWarn("No Answer defaulting to: yes")
				return True


def questionDefaultNo (textType, text, iterations):
	Color_Off='\033[0m'		# Text Reset
	errText='\033[0;31m'	# Red
	okText='\033[0;32m'		# Green
	warnText='\033[0;33m'	# Yellow
	err='\033[1;31m'		# BOLD Red
	ok='\033[1;32m'			# BOLD Green
	warn='\033[1;33m'		# BOLD Yellow
	info='\033[1;36m'		# Cyan BOLD

	if textType.upper() == "OK":
		message = ok + "OK: " + okText + text + Color_Off
	elif textType.upper() == "WARNING":
		message = warn + "WARNING: " + warnText + text + Color_Off
	elif textType.upper() == "ERROR":
		message = err + "ERROR: " + errText + text + Color_Off
	else:
		message = info + "INFO: " + Color_Off + text
	

	numberOfAnsweredIterations = 0
	while numberOfAnsweredIterations < iterations:
		response = input(message + info + " (yes or NO): " + Color_Off)
		if any(response.lower() == f for f in ["yes", "y", "1", "ye"]):
			return True
			
		elif any(response.lower() == f for f in ["no", "n", "0"]):
			return False

		else:
			numberOfAnsweredIterations += 1
			if numberOfAnsweredIterations < iterations:
				printWarn("Please Answer yes or no")
			else:
				printWarn("No Answer defaulting to: No")
				return False