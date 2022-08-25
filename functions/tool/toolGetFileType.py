#!/usr/bin/env python3

# imports of libraries
import subprocess

def getFileMagic (inputFile):
	# get the magic file type of the input file
	cmd = ["file", "-b", "--mime-type", inputFile]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	output, error = proc.communicate()
	magic = output.decode('ascii')

	return magic.strip()