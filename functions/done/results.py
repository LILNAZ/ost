#!/usr/bin/env python3

# imports of libraries
from ..tool.toolColoredOutput import *


def statusOfHashResult (hashResults):
	if hashResults.isEqual:
		return 100
	else:
		return -100

def statusOfMicrosoftResult (microsoftCodeSign):
	result = 0.0
	totalCount = microsoftCodeSign.singedTrusted.count + microsoftCodeSign.singedNotFullChain.count + microsoftCodeSign.unsigned.count
	
	if microsoftCodeSign.singedTrusted.count != 0:

		result += (microsoftCodeSign.singedTrusted.count / totalCount) * 100

	if microsoftCodeSign.singedNotFullChain.count != 0:
		printWarn("Do you trust these Public Keys?: " + str(microsoftCodeSign.singedNotFullChain.singingSubject))

		result += (microsoftCodeSign.singedNotFullChain.count / totalCount) * 10

	if microsoftCodeSign.unsigned.count != 0:
		print("")
		result += (microsoftCodeSign.unsigned.count / totalCount) * -100

	return round(result)

def statusOfRedHatResults (rpmSigning):
	result = 0.0
	totalCount = rpmSigning.signed.count + rpmSigning.singedKeyNotFound.count + rpmSigning.unsigned.count + rpmSigning.efi.count
	
	if rpmSigning.signed.count != 0:

		result += (rpmSigning.signed.count / totalCount) * 100

	if rpmSigning.singedKeyNotFound.count != 0:
		printWarn("Do you trust these Public Keys?: " + str(rpmSigning.singedKeyNotFound.singingSubject))

		result += (rpmSigning.singedKeyNotFound.count / totalCount) * 10

	if rpmSigning.efi.singingSubject:
		printWarn("Do you trust these Public Keys?: " + str(rpmSigning.efi.singingSubject))

	if rpmSigning.efi.singingSubject or rpmSigning.efi.singingSubjectTrusted:
		result += (rpmSigning.efi.count / totalCount) * 100

	if rpmSigning.unsigned.count != 0:
		result += (rpmSigning.unsigned.count / totalCount) * -100

	return round(result)

def statusOfVMWareResults (vmwareMicrosoftAndOvf):
	result = 0.0
	totalCount = vmwareMicrosoftAndOvf.singedTrusted.count + vmwareMicrosoftAndOvf.singedNotFullChain.count + vmwareMicrosoftAndOvf.unsigned.count
	
	if vmwareMicrosoftAndOvf.singedTrusted.count != 0:

		result += (vmwareMicrosoftAndOvf.singedTrusted.count / totalCount) * 100

	if vmwareMicrosoftAndOvf.singedNotFullChain.count != 0:
		printWarn("Do you trust these Public Keys?: " + str(vmwareMicrosoftAndOvf.singedNotFullChain.singingSubject))

		result += (vmwareMicrosoftAndOvf.singedNotFullChain.count / totalCount) * 10

	if vmwareMicrosoftAndOvf.unsigned.count != 0:
		result += (vmwareMicrosoftAndOvf.unsigned.count / totalCount) * -100

	return round(result)

def statusOfTheResults (workingDir, hashResults, microsoftCodeSign, rpmSigning, vmwareMicrosoftAndOvf):
	sumOfResults = 0

	sumOfResults += statusOfHashResult(hashResults)
	sumOfResults += statusOfMicrosoftResult(microsoftCodeSign)
	sumOfResults += statusOfRedHatResults(rpmSigning)
	sumOfResults += statusOfVMWareResults(vmwareMicrosoftAndOvf)

	sum

	scorePassing = 199
	scoreWarning = 150

	if sumOfResults > scorePassing:
		color='\033[0;32m'		 # Green
	elif sumOfResults > scoreWarning:
		color='\033[0;33m'	# Yellow
	else:
		color='\033[0;31m'	# Red
	Color_Off='\033[0m'


	print('''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''+color+'''

        ██████  ███████ ███████ ██    ██ ██      ████████ ███████
        ██   ██ ██      ██      ██    ██ ██         ██    ██     
        ██████  █████   ███████ ██    ██ ██         ██    ███████
        ██   ██ ██           ██ ██    ██ ██         ██         ██
        ██   ██ ███████ ███████  ██████  ███████    ██    ███████
''' + Color_Off)



	printInfo("Score is from -200 to 200.\n "+str(scorePassing)+" - 200 = 0k\n "+str(scoreWarning)+" - "+str(scorePassing-1)+" = Warning\n-200 - "+str(scoreWarning-1)+" = Error\n")
	if sumOfResults > scorePassing:
		printOk("Score: " + str(sumOfResults))
	elif sumOfResults > scoreWarning:
		printWarn("Score: " + str(sumOfResults))
		printWarn("Check the output it can be:\n(1) that files are unsigned\n(2) full trust chain could not be established for signing verification\n(3) Hash is not equal")
	else:
		printError("Score: " + str(sumOfResults))
		printError("Check the output it can be:\n(1) that files are unsigned\n(2) full trust chain could not be established for signing verification\n(3) Hash is not equal\nEssentially look for error or warnings above and correlate with: " + workingDir)

	print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")