#!/usr/bin/env python3

 
buildVersion = "0004"


# imports of libraries
# Setup
from functions.setup.setupCommandLineFlags import commandLineFlags
from functions.setup.setupHeader import informationHeader
from functions.setup.setupValidateInput import validateInput
from functions.setup.setupWorkingDir import setupDirs

# Tools
from functions.tool.toolUnixTime import getCurrentUnixTime
from functions.tool.toolColoredOutput import *

# Hash
from functions.hashVerifyHash import verifyHash, generateSHA512

# Sign
from functions.signMicrosoft import verifyMicrosoftSignatures
from functions.signRhel import verifyRhelSignatures
from functions.signVmware import verifyVmWareSignatures

# CVS
from functions.writeCsvReport import writeCsvReport

# Results
from functions.done.results import statusOfTheResults

# clan up
from functions.done.cleanup import finalSteps

def setupArgs ():
	# Global vars
	global inputFile	#str
	global inputHash	#str
	global isMicrosoft	#bool
	global isRHEL		#bool
	global isVmWare		#bool
	
	# Get command line flags
	args = commandLineFlags(buildVersion)

	# Set the arguments to variables
	inputFile = args.filepath
	inputHash = args.sha256
	isMicrosoft = args.microsoft
	isRHEL = args.rhel
	isVmWare = args.vmware

	# Validate input
	validateInput(inputFile, inputHash, isMicrosoft, isRHEL, isVmWare)

	# Print Information header
	informationHeader()

if __name__ == '__main__':
	# Set up
	# Get current time
	currentUnixTime = getCurrentUnixTime()
	
	# Set up arguments
	setupArgs()

	# Create folder structure
	workingDir = setupDirs(currentUnixTime, inputFile, isMicrosoft, isRHEL, isVmWare)
	CsvOutputDir="./output/"

	# Setup of classes
	# hash
	class hashResults:
		isEqual = False
		vendorHash = inputHash
		generateSHA256 = ""
		generateSHA512 = ""
	
	# Microsoft (is also used inside RHEL and VMWare)
	class microsoftCodeSign:
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
	
	# Red Hat
	class rpmSigning:
		found = False
		fingerprintsGenerated = False
		class signed:
			count = 0
			report = ""
			files = ""
			singingSubject = []
		class singedKeyNotFound:
			count = 0
			report = ""
			files = ""
			singingSubject = []
		class unsigned:
			count = 0
			report = ""
			files = ""
		class corrupted:
			count = 0
			report = ""
			files = ""
		class efi:
			count = 0
			singingSubjectTrusted = []
			singingSubject = []

	# VMWare (uses the microsoft class with appended ovf)
	class vmwareMicrosoftAndOvf:
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
		class ovf:
			vendor = []

	hashResults = verifyHash(workingDir, inputFile, hashResults)
	hashResults.generateSHA512 = generateSHA512(workingDir, inputFile)

	if isMicrosoft:
		microsoftCodeSign = verifyMicrosoftSignatures(workingDir, inputFile, microsoftCodeSign, [])
		printInfo("Done verifying Microsoft Signatures")
	elif isRHEL:
		rpmSigning = verifyRhelSignatures(workingDir,inputFile, rpmSigning)
	elif isVmWare:
		vmwareMicrosoftAndOvf = verifyVmWareSignatures(workingDir, inputFile, vmwareMicrosoftAndOvf)

	# Create CSV
	
	writeCsvReport(buildVersion, currentUnixTime, CsvOutputDir, inputFile, hashResults, microsoftCodeSign, rpmSigning, vmwareMicrosoftAndOvf)

	statusOfTheResults(workingDir, hashResults, microsoftCodeSign, rpmSigning, vmwareMicrosoftAndOvf)

	# Cleanup and existing
	finalSteps(workingDir, currentUnixTime)
