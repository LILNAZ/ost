#!/usr/bin/env python3

# imports of libraries
import hashlib
from .tool.toolColoredOutput import *
from .tool.toolYesNoQuestion import *

def verifyHash (workingDir, inputFile, hashResults):
	# generate SHA 256 of input file
	hashResults.generateSHA256 = generateSHA256(workingDir, inputFile)
	
	# Check if the hashes are equal
	if hashResults.generateSHA256.upper() == hashResults.vendorHash.upper():
		printOk("SHA256 are equal!")
		hashResults.isEqual = True
	else:
		printError("SHA256 are not equal!")
		hashResults.isEqual = False

		continueAfterNotEqual = questionDefaultYes("warning", "Hash not equal do you want to continue?", 10)
		if not continueAfterNotEqual:
			printInfo("Exiting...")
			exit(100)

	return hashResults

def generateSHA256 (workingDir, inputFile):
	# Calculate SHA 256 sum of the input File
	sha256hash = hashlib.sha256()
	with open(inputFile, "rb") as file:
		for byte_block in iter(lambda: file.read(4096),b""):
			sha256hash.update(byte_block)

	# Save results to working dir
	pathToFile = workingDir + "/hash.inputFileSha256.txt"
	with open(pathToFile, 'a') as output:
		output.write(str(sha256hash.hexdigest()) + " : " + inputFile + "\n")


	return sha256hash.hexdigest()

def generateSHA512 (workingDir, inputFile):
	# Calculate SHA 256 sum of the input File
	sha512hash = hashlib.sha512()
	with open(inputFile, "rb") as file:
		for byte_block in iter(lambda: file.read(4096),b""):
			sha512hash.update(byte_block)

	# Save results to working dir
	pathToFile = workingDir + "/hash.inputFileSha512.txt"
	with open(pathToFile, 'a') as output:
		output.write(str(sha512hash.hexdigest()) + " : " + inputFile + "\n")

	return sha512hash.hexdigest()