#!/usr/bin/env python3

# imports of libraries
import os
import re

# Microsoft
from itertools import count
from .signMicrosoft import verifyMicrosoftSignatures

# Tools
from .tool.toolColoredOutput import *
from .tool.toolYesNoQuestion import *
from .tool.toolGetFileType import getFileMagic
from .tool.toolGetFileExtensions import getFileExtension
from .tool.toolMountIso import *

def getVendorFromOVA (workingDir, inputFile):
	listOfVendors = []
	
	cmd = ["ovftool", inputFile]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = proc.communicate()

	# Find all vendors in the ova/ovf file
	foundVendors = re.findall(r'Vendor:.+', output.decode("UTF-8"), re.MULTILINE)

	# Save the results to a list
	for vendor in foundVendors:
		listOfVendors.append(vendor.split(':')[1].lstrip())
	
	# save output of the
	pathToOvfFile = workingDir + "/ova.report.txt"
	message = "\n-------------------------------------------------\n" + inputFile + "\n-------------------------------------------------\n" + output.decode("UTF-8") + "\n" + error.decode("UTF-8") + "\n"
	with open(pathToOvfFile, 'a') as output:
		output.write(message)

	return listOfVendors


def checkOvaVendor (workingDir, inputFile):
	listOfVendor = []
	extensionFiltering = [".ova", ".ovf"]

	# Mount ISO
	isoPath = mountIso(inputFile)

	for subdir, dirs, files in os.walk(isoPath):
		for file in files:
			fileInsideIso = os.path.join(subdir, file)
			# Get the current file extension
			currFileExtension = getFileExtension(fileInsideIso)

			# Compare if it is in extension filtering
			if currFileExtension in extensionFiltering:
				listOfVendor.extend(getVendorFromOVA(workingDir, fileInsideIso))

	# Unmount ISO
	UnMountIso(isoPath)

	# Remove duplicate entries in the list
	listOfVendor = list(dict.fromkeys(listOfVendor))

	return listOfVendor


def verifyVmWareSignatures(workingDir, inputFile, vmwareMicrosoftAndOvf):
	# MS class with added ovf field
	# class vmwareMicrosoftAndOvf:
	# 	found = False
	# 	class singedTrusted:
	# 		count = 0
	# 		report = ""
	# 		files = ""
	# 		fileExtensions = ""
	# 		singingSubject = []
	# 	class singedNotFullChain:
	# 		count = 0
	# 		report = ""
	# 		files = ""
	# 		fileExtensions = ""
	# 		singingSubject = []
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
	# 	class ovf:
	# 		vendor = []

	# Preamble information about the limitations
	printInfo("Due to variances in VMware releases (ESXI, VCSA, and so on) and that most files are gzip or scripts.")
	printInfo("This portion of the script has the most variance where with ESXI it can only check signings of efi secure boot.")
	printInfo("VCSA has a some win32 installer that contains .exe, .dll, .msi and .efi. As well can ova and ovf files be checked, however, I do not know if the vendor flag is easily spoofed or any sort of verification")
	continueTests = questionDefaultYes("INFO","Have you read the above information?",1)

	if continueTests:
		#Verify signatures of windows files
		vmwareMicrosoftAndOvf = verifyMicrosoftSignatures(workingDir, inputFile, vmwareMicrosoftAndOvf, [".efi", ".dll", ".msi", ".exe"])

		# Check ova and ovf files
		# get the file magic of the input file
		inputFileType = getFileMagic(inputFile)
		
		# Check if input file is an ISO file
		if inputFileType == "application/x-iso9660-image":
			#Verify OVA and OVF files
			vmwareMicrosoftAndOvf.ovf.vendor = checkOvaVendor (workingDir, inputFile)

		return vmwareMicrosoftAndOvf

	else:
		printError("Exiting...")
		exit(1)










#VCSA
# application/csv
# application/gzip
# application/javascript
# application/json
# application/octet-stream
# application/x-archive
# application/x-dosexec
# application/x-executable
# application/x-gettext-translation
# application/x-mach-binary
# application/x-msi
# application/x-sharedlib
# application/x-tar
# application/x-wine-extension-ini
# application/zip
# font/sfnt
# image/bmp
# image/gif
# image/png
# image/vnd.microsoft.icon
# image/x-icns
# inode/directory
# inode/x-empty
# message/rfc822
# text/html
# text/plain
# text/rtf
# text/troff
# text/x-asm
# text/x-c
# text/x-c++
# text/x-java
# text/x-makefile
# text/xml
# text/x-msdos-batch
# text/x-objective-c
# text/x-python
# text/x-ruby
# text/x-shellscript
# text/x-tex




# ESXI
# application/gzip
# application/octet-stream
# application/x-c32-comboot-syslinux-exec
# application/x-dbt
# application/x-dosexec
# application/x-executable
# application/zip
# inode/directory
# text/plain
# text/xml
# text/x-python
