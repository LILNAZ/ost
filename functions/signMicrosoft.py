#!/usr/bin/env python3

# imports of libraries
import subprocess
import re
import os

# Tools
from .tool.toolColoredOutput import *
from .tool.toolGetFileType import *
from .tool.toolGetFileExtensions import getFileExtensionAndOccurrences, getFileExtension
from .tool.toolMountIso import UnMountIso, mountIso

def getMicrosoftSignatures (inputFile, microsoftCodeSign):
	# Run osslsigncode on the input file and capture the output
	cmd = ["osslsigncode", "verify", inputFile]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = proc.communicate()

	# Categorize the output and set file path to right corresponding file
	# All OK - Full trust chain
	if re.search(r'Succeeded', output.decode("UTF-8")) or re.search(r'Succeeded', error.decode("UTF-8")):
		osslsigncodeOutputPath = microsoftCodeSign.singedTrusted.report
		osslsigncodeFilePath = microsoftCodeSign.singedTrusted.files
		microsoftCodeSign.found = True
		microsoftCodeSign.singedTrusted.count += 1

	# OK-ish - not full trust chain
	elif re.search(r'Number of verified signatures', output.decode("UTF-8")) or re.search(r'Number of verified signatures', error.decode("UTF-8")):
		osslsigncodeOutputPath = microsoftCodeSign.singedNotFullChain.report
		osslsigncodeFilePath = microsoftCodeSign.singedNotFullChain.files
		microsoftCodeSign.found = True
		microsoftCodeSign.singedNotFullChain.count += 1

	# NOT OK - Unrecognized file
	elif re.search(r'Unrecognized file type', output.decode("UTF-8")) or re.search(r'Unrecognized file type', error.decode("UTF-8")):
		osslsigncodeOutputPath = microsoftCodeSign.unrecognized.report
		osslsigncodeFilePath = microsoftCodeSign.unrecognized.files
		microsoftCodeSign.found = True
		microsoftCodeSign.unrecognized.count += 1

	# NOT OK - No signature found
	elif re.search(r'No signature found', output.decode("UTF-8")) or re.search(r'No signature found', error.decode("UTF-8")):
		osslsigncodeOutputPath = microsoftCodeSign.unsigned.report
		osslsigncodeFilePath = microsoftCodeSign.unsigned.files
		microsoftCodeSign.found = True
		microsoftCodeSign.unsigned.count += 1

	# NOT OK - Signed but invalided due to unmatched PE Checksum
	elif re.search(r'Invalid signature', output.decode("UTF-8")) or re.search(r'Invalid signature', error.decode("UTF-8")) or re.search(r'MISMATCH!!!!', output.decode("UTF-8")) or re.search(r'MISMATCH!!!!', error.decode("UTF-8")):
		printError("Found invalided signature in file: " + str(osslsigncodeFilePath))
		osslsigncodeOutputPath = microsoftCodeSign.unsigned.report
		osslsigncodeFilePath = microsoftCodeSign.unsigned.files
		microsoftCodeSign.found = True
		microsoftCodeSign.unsigned.count += 1

	else:
		printError("FOUND UNEXPECTED MICROSOFT SIGNING RESULTS PLEASE CHECK LOCAL DIRECTOR FOR DEBUG INFO")
		osslsigncodeOutputPath = "./DEBUG-OSSLSIGNCODE-NEW-CASE.txt"
		osslsigncodeFilePath = "./DEBUG-OSSLSIGNCODE-NEW-CASE.files.txt"

	# Save output to file
	message = "\n-------------------------------------------------\n" + inputFile + "\n-------------------------------------------------\n" + output.decode("UTF-8") + "\n" + error.decode("UTF-8") + "\n"
	with open(osslsigncodeOutputPath, 'a') as output:
		output.write(message)
	
	with open(osslsigncodeFilePath, 'a') as output:
		output.write(inputFile + "\n")

	return microsoftCodeSign

def verifyStatusOfMicrosoftSignatures (microsoftCodeSign):
	# Verify that we have gotten any signatures to check
	if microsoftCodeSign.found == False:
		printError("Did not find any singed or unsigned files!")
		exit(1)

	# Get number of signed and unsigned files
	totalNumberOfSingedFiles = microsoftCodeSign.singedTrusted.count + microsoftCodeSign.singedNotFullChain.count
	totalNumberOfUnSingedFiles = microsoftCodeSign.unrecognized.count + microsoftCodeSign.unsigned.count

	# All signed
	if totalNumberOfSingedFiles != 0 and totalNumberOfUnSingedFiles == 0:
		# Full trust chain
		if microsoftCodeSign.singedNotFullChain.count == 0:
			printOk("All " + str(totalNumberOfSingedFiles) + " file(s) singed!")
		# Not full trust chain
		else:
			printWarn("All " + str(totalNumberOfSingedFiles) + " file(s) singed! However, full trust chain could not be established with " + str(microsoftCodeSign.singedNotFullChain.count) + " file(s).")
			printInfo("This is most likely Microsoft problem, as they do not for some reason publish code sining CA certs and for some other cool Microsoft reason have multiple CA certs named the same :)")

	# Mix of singed and unsigned
	elif totalNumberOfSingedFiles != 0 and totalNumberOfUnSingedFiles != 0:
		printWarn(str (totalNumberOfSingedFiles) + " file(s) where singed" + str(totalNumberOfUnSingedFiles) + " file(s) where not signed")
		printWarn("Out of the unsigned file(s) " + str(microsoftCodeSign.unrecognized.count) + " where of an unrecognized file type and " + str(microsoftCodeSign.unsigned.count) + " where unsigned")
		printWarn("Out of the singed file(s) " + str(microsoftCodeSign.singedNotFullChain.count) + " could full trust chain not be established and " + str(microsoftCodeSign.singedTrusted.count) + " file(s) could full trust chain be established")

		if microsoftCodeSign.singedNotFullChain.count != 0:
			printInfo("About the files with not full trust chain. This is most likely Microsoft problem, as they do not for some reason publish code sining CA certs and for some other cool Microsoft reason have multiple CA certs named the same :)")

	# All unsigned
	elif totalNumberOfUnSingedFiles != 0 and totalNumberOfSingedFiles == 0:
		printWarn("All" + str(totalNumberOfUnSingedFiles) + " file(s) where not signed")

	else:
		print("")

	# If all singed
	if microsoftCodeSign.singedTrusted.count != 0 and microsoftCodeSign.singedNotFullChain.count == 0 and totalNumberOfUnSingedFiles == 0:
		printOk("All " + str(totalNumberOfSingedFiles) + " file(s) singed!")

	# If we have not fully trusted
	elif totalNumberOfUnSingedFiles == 0 and totalNumberOfSingedFiles != 0:
		printWarn("All " + str(totalNumberOfSingedFiles) + " file(s) singed! However, full trust chain could not be established with " + str(microsoftCodeSign.singedNotFullChain.count) + " file(s).")

		printInfo("This is most likely Microsoft problem, as they do not for some reason publish code sining CA certs and for some other cool Microsoft reason have multiple CA certs named the same :)")

	# If we have only unrecognized files
	elif totalNumberOfUnSingedFiles != 0 and microsoftCodeSign.unrecognized.count == 0:
		printWarn(str(totalNumberOfUnSingedFiles) + " file(s) where not signed")

	# If we have unsigned
	elif totalNumberOfUnSingedFiles != 0:
		printWarn(str(totalNumberOfUnSingedFiles) + " file(s) where not signed. However, " + str(microsoftCodeSign.unrecognized.count) + " could not be tested due to unrecognized file types")

	# Get file extensions the files tested
	resultFileExtensionTrusted = getFileExtensionAndOccurrences(microsoftCodeSign.singedTrusted.files)
	resultFileExtensionNotFullChain = getFileExtensionAndOccurrences(microsoftCodeSign.singedNotFullChain.files)
	resultFileExtensionUnrecognized = getFileExtensionAndOccurrences(microsoftCodeSign.unrecognized.files)
	resultFileExtensionFailed = getFileExtensionAndOccurrences(microsoftCodeSign.unsigned.files)

	# Print unsigned file extensions
	if resultFileExtensionTrusted != "":
		printInfo("The file extensions and count of the singed file(s) with full chain of trust:\n" + resultFileExtensionTrusted)
	if resultFileExtensionNotFullChain != "":
		printInfo("The file extensions and count of the singed file(s) that not full chain of trust could be established:\n" + resultFileExtensionNotFullChain)
	if resultFileExtensionUnrecognized != "":
		printInfo("The file extensions and count of the unrecognized file(s):\n" + resultFileExtensionUnrecognized)
	if resultFileExtensionFailed != "":
		printInfo("The file extensions and count of the unsigned file(s):\n" + resultFileExtensionFailed)

	# Get signing subjects
	if microsoftCodeSign.singedTrusted.count != 0:
		microsoftCodeSign.singedTrusted.singingSubject = findMicrosoftSingingSubject(microsoftCodeSign.singedTrusted.report)
	
	if microsoftCodeSign.singedNotFullChain.count != 0:
		microsoftCodeSign.singedNotFullChain.singingSubject = findMicrosoftSingingSubject(microsoftCodeSign.singedNotFullChain.report)

	return microsoftCodeSign

def findMicrosoftSingingSubject (inputFile):
	cmd = ["./functions/tool/bashGetMsSiningSubject.sh", inputFile]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = proc.communicate()
	return output.decode("UTF-8").strip().split('\n')

def verifyMicrosoftSignatures (workingDir, inputFile, microsoftCodeSign, extensionFiltering):
	# class microsoftCodeSign:
	# 	found = False
	# 	class singedTrusted:
	# 		count = 0
	# 		report = ""
	# 		files = ""
	# 		fileExtensions = ""
	# 		singingSubject = ""
	# 	class singedNotFullChain:
	# 		count = 0
	# 		report = ""
	# 		files = ""
	# 		fileExtensions = ""
	# 		singingSubject = ""
	# 	class unrecognized:
	# 		count = 0
	# 		report = ""
	# 		files = ""
	# 		fileExtensions = ""
	# 	class unsigned:
	# 		count = 0
	# 		report = ""
	# 		files = ""
	# 		fileExtensions = ""

	# Set of of variables
	# set output reports
	microsoftCodeSign.singedTrusted.report = workingDir + "/signed.trusted.txt"
	microsoftCodeSign.singedNotFullChain.report = workingDir + "/signed.couldNotVerifyChainOfTrust.txt"
	microsoftCodeSign.unrecognized.report = workingDir + "/signed.unrecognized.txt"
	microsoftCodeSign.unsigned.report = workingDir + "/signed.failed.txt"

	# Set output files
	microsoftCodeSign.singedTrusted.files = workingDir + "/tmp.signed.trusted.filePath.txt"
	microsoftCodeSign.singedNotFullChain.files = workingDir + "/tmp.signed.couldNotVerifyChainOfTrust.filePath.txt"
	microsoftCodeSign.unrecognized.files = workingDir + "/tmp.signed.unrecognized.filePath.txt"
	microsoftCodeSign.unsigned.files = workingDir + "/tmp.signed.failed.filePath.txt"

	# Get magic info from the input file
	inputFileType = getFileMagic(inputFile)
	
	# Check if input file is an ISO file
	if inputFileType == "application/x-iso9660-image":
		# Mount ISO if ISO
		isoPath = mountIso(inputFile)

		# Get signatures of all files inside the ISO
		for subdir, dirs, files in os.walk(isoPath):
			for file in files:
				fileInsideIso = os.path.join(subdir, file)
				# Get the current file extension
				currFileExtension = getFileExtension(fileInsideIso)

				# Compare if we have any extension filtering and if so is the file extension something we should check
				if currFileExtension in extensionFiltering or not extensionFiltering:
					# get the results from the the microsoft styled signatures
					microsoftCodeSign = getMicrosoftSignatures(fileInsideIso, microsoftCodeSign)

		UnMountIso(isoPath)

	else:
		# Get signatures of input file
		microsoftCodeSign = getMicrosoftSignatures(inputFile, microsoftCodeSign)
	
	# Verify status of the signed files
	microsoftCodeSign = verifyStatusOfMicrosoftSignatures(microsoftCodeSign)

	return microsoftCodeSign
