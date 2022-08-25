#!/usr/bin/env python3

def printError (text):
	Color_Off='\033[0m'		# Text Reset
	errText='\033[0;31m'	# Red
	err='\033[1;31m'		# BOLD Red
	print(err + "ERROR: " + errText + text + Color_Off)

def printInfo (text):
	Color_Off='\033[0m'		# Text Reset
	info='\033[1;36m'		# Cyan BOLD
	print(info + "INFO: " + Color_Off + text)

def printWarn (text):
	Color_Off='\033[0m'		# Text Reset
	warnText='\033[0;33m'	# Yellow
	warn='\033[1;33m'		# BOLD Yellow

	print(warn + "WARNING: " + warnText + text + Color_Off)

def printOk (text):
	Color_Off='\033[0m'		# Text Reset
	okText='\033[0;32m'		 # Green
	ok='\033[1;32m'			# BOLD Green

	print(ok + "OK: " + okText + text + Color_Off)