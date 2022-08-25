#!/usr/bin/env python3

# imports of libraries
import subprocess
import re
import os

from .tool.toolColoredOutput import *
from .tool.toolGetFileType import getFileMagic
from .tool.toolMountIso import UnMountIso, mountIso

from .signMicrosoft import verifyMicrosoftSignatures

def getRpmSignatures (inputFile, rpmSigning):
	# Run rpm checksig on the input file and capture the output
	cmd = ["rpm", "--checksig", "-v", inputFile]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = proc.communicate()
	
	
	if re.search(r'Signature', output.decode("UTF-8")) or re.search(r'Signature', error.decode("UTF-8")):
		if re.search(r'NOKEY', output.decode("UTF-8")) or re.search(r'NOKEY', error.decode("UTF-8")):
			rpmOutputPath = rpmSigning.singedKeyNotFound.report
			rpmFilePath = rpmSigning.singedKeyNotFound.files
			rpmSigning.singedKeyNotFound.count += 1
			rpmSigning.found = True
		else:
			rpmOutputPath = rpmSigning.signed.report
			rpmFilePath = rpmSigning.signed.files
			rpmSigning.signed.count += 1
			rpmSigning.found = True
	elif re.search(r'BAD', output.decode("UTF-8")) or re.search(r'BAD', error.decode("UTF-8")):
		rpmOutputPath = rpmSigning.corrupted.report
		rpmFilePath = rpmSigning.corrupted.files
		rpmSigning.corrupted.count += 1
		rpmSigning.found = True
	else:
		rpmOutputPath = rpmSigning.unsigned.report
		rpmFilePath = rpmSigning.unsigned.files
		rpmSigning.unsigned.count += 1
		rpmSigning.found = True

	# Save output to file
	message = "\n-------------------------------------------------\n" + inputFile + "\n-------------------------------------------------\n" + output.decode("UTF-8") + "\n" + error.decode("UTF-8") + "\n"
	with open(rpmOutputPath, 'a') as output:
		output.write(message)
	
	with open(rpmFilePath, 'a') as output:
		output.write(inputFile + "\n")

	return rpmSigning

def verifyStatusOfRpmSignatures (rpmSigning, workingDir):
	if rpmSigning.found == False:
		printError("Did not find any singed or unsigned files!")
		exit(1)
	
	totalSignedPackages = rpmSigning.signed.count + rpmSigning.singedKeyNotFound.count
	totalUnsignedPackages = rpmSigning.unsigned.count + rpmSigning.corrupted.count

	# If all packages are singed
	if totalSignedPackages != 0 and totalUnsignedPackages == 0:

		# If some Key ID not found
		if rpmSigning.singedKeyNotFound.count != 0:
			printWarn(str(totalSignedPackages) + " package(s) singed. However, " + str(rpmSigning.singedKeyNotFound.count) + " package(s) did not have a local GPG key")

		# If all key ID found
		else:
			printOk("All " + str(rpmSigning.signed.count) + " package(s) singed and with GPG keys found on the system")

	# If there is a mix of singed and unsigned
	elif totalSignedPackages != 0 and totalUnsignedPackages != 0:
		printError(str(totalSignedPackages) + " packages singed. However, " + str(rpmSigning.singedKeyNotFound.count) + " package(s) did not have a local GPG key. Found: " + str(totalUnsignedPackages) + " package(s) that where not signed")

		# If there are corrupted packages
		if rpmSigning.corrupted.count != 0:
			printError("Out of the unsigned package(s): " + str(rpmSigning.corrupted.count) + " where corrupted!")

	# If all packages are unsigned
	else:
		printError(str(totalUnsignedPackages) + " package(s) that where not signed")

		# If there are corrupted packages
		if rpmSigning.corrupted.count != 0:
			printError("Out of the unsigned package(s): " + str(rpmSigning.corrupted.count) + " where corrupted!")

	# match key id to fingerprint (singingSubject)
	if rpmSigning.signed.count != 0:
		rpmSigning = matchKeyIdToFingerprint (rpmSigning, workingDir)

	# append if necessary key ID for the key not found
	if rpmSigning.singedKeyNotFound.count != 0:
		rpmSigning.singedKeyNotFound.singingSubject = findKeyIdInOutput(rpmSigning.singedKeyNotFound.report)

	return rpmSigning

def matchKeyIdToFingerprint (rpmSigning, workingDir):
	# Check if fingerprints have been generated
	if rpmSigning.fingerprintsGenerated == False:
		# Set up
		pathToRpmGpg = "/etc/pki/rpm-gpg/"

		# Generate Fingerprints
		rpmSigning.fingerprintsGenerated = generateFingerprints (pathToRpmGpg, workingDir)

	# Get all key ID
	signedKeyId = findKeyIdInOutput(rpmSigning.signed.report)

	# match the key ID with the fingerprints
	with open(fingerPrintFile) as f:
		for fingerprintLine in f:
			for keyId in signedKeyId:
				if re.search(keyId, fingerprintLine, re.IGNORECASE):
					#print(fingerprintLine)
					correctKey = fingerprintLine.strip().split(':')
					rpmSigning.signed.singingSubject.append(os.path.basename(correctKey[1]))

	return rpmSigning

def generateFingerprints (gpgKeyLocation, workingDir):
	global fingerPrintFile
	fingerPrintFile = workingDir + "/tmp.gpg.fingerprint.txt"

	cmd = ["./functions/tool/bashGenerateGpgFingerprint.sh", gpgKeyLocation, fingerPrintFile]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = proc.communicate()

	if str(output) == "b\'\'" or str(error) == "b\'\'":
		printInfo("GPG key fingerprints generated!")
		return True
	else:
		printError("GPG Key fingerprint could not be generated!")
		printWarn(str(output))
		exit(2)

def findKeyIdInOutput (rpmSingedOutput):
	# find all key ID
	cmd = ["./functions/tool/bashFindRpmKeyId.sh", rpmSingedOutput]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = proc.communicate()

	# convert output to list and return
	return output.decode("UTF-8").strip().split('\n')

def verifyRhelSignatures(workingDir, inputFile, rpmSigning):
	class MsEfiSigning:
		found = False
		class singedTrusted:
			count = 0
			report = ""
			files = ""
			fileExtensions = ""
			singingSubject = []
		class singedNotFullChain:
			count = 0
			report = ""
			files = ""
			fileExtensions = ""
			singingSubject = []
		class unrecognized:
			count = 0
			report = ""
			files = ""
			fileExtensions = ""
		class unsigned:
			count = 0
			report = ""
			files = ""
			fileExtensions = ""
	# class rpmSigning:
	# 	found = False
	# 	fingerprintsGenerated = False
	# 	class signed:
	# 		count = 0
	# 		report = ""
	# 		files = ""
	# 		singingSubject = []
	# 	class singedKeyNotFound:
	# 		count = 0
	# 		report = ""
	# 		files = ""
	# 		singingSubject = []
	# 	class unsigned:
	# 		count = 0
	# 		report = ""
	# 		files = ""
	# 	class corrupted:
	# 		count = 0
	# 		report = ""
	# 		files = ""
	# 	class efi:
	# 		count = 0
	# 		singingSubjectTrusted = []
	# 		singingSubject = []

	# Set variables
	rpmSigning.signed.report = workingDir + "/rpm.signed.txt"
	rpmSigning.singedKeyNotFound.report = workingDir + "/rpm.signedKeyNotFound.txt"
	rpmSigning.unsigned.report = workingDir + "/rpm.unsigned.txt"
	rpmSigning.corrupted.report = workingDir + "/rpm.corrupted.txt"

	rpmSigning.signed.files = workingDir + "/rpm.signed.files.txt"
	rpmSigning.singedKeyNotFound.files = workingDir + "/rpm.signedKeyNotFound.files.txt"
	rpmSigning.unsigned.files = workingDir + "/rpm.unsigned.files.txt"
	rpmSigning.corrupted.files = workingDir + "/rpm.corrupted.files.txt"

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
	
				fileInsideIsoMagic = getFileMagic(fileInsideIso)
				if fileInsideIsoMagic == "application/x-rpm":
					rpmSigning = getRpmSignatures(fileInsideIso, rpmSigning)

		# Verify secure boot
		MsEfiSigning = verifyMicrosoftSignatures(workingDir, inputFile, MsEfiSigning, [".efi"])

		UnMountIso(isoPath)

	elif inputFileType == "application/x-rpm":
		# Get signatures of input file
		rpmSigning = getRpmSignatures(inputFile, rpmSigning)
	
	else:
		printError("File not ISO or rpm could not verify rpm signatures")

	# Verify status of the signed files
	rpmSigning = verifyStatusOfRpmSignatures(rpmSigning, workingDir)

	# Append if necessary relevant information from microsoft signing
	if MsEfiSigning.found:
		rpmSigning.efi.count = MsEfiSigning.singedTrusted.count + MsEfiSigning.singedNotFullChain.count
		rpmSigning.efi.singingSubjectTrusted = MsEfiSigning.singedTrusted.singingSubject
		rpmSigning.efi.singingSubject = MsEfiSigning.singedNotFullChain.singingSubject

	return rpmSigning
