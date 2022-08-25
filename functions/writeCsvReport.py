#!/usr/bin/env python3

# imports of libraries
import csv
from os.path import exists

# Tools
from .tool.toolColoredOutput import *

def writeCsvReport (buildVersion, currentUnixTime, outputDir, inputFile, hashResults, microsoftCodeSign, rpmSigning, vmwareMicrosoftAndOvf):

	csvFilePath = outputDir + "/report.csv"

	header = ["Time of report",
	"Script version",
	"Filename",
	"SHA256 Equal",
	"Vendor SHA256",
	"Generated SHA512",
	"Other partners SHA512",
	"Number of singed files",
	"Number of singed files with not full trust chain",
	"Number of unsigned files",
	"Number of unrecognized or corrupted",
	"Signing subjects (continuing)"]


	# Convert hash results to string
	if hashResults.isEqual:
		hashStatus = "OK"
	else:
		hashStatus = "NOK"

	# Set the specific type results
	# Get Microsoft results
	if microsoftCodeSign.found:
		numberOfSingedFiles = str(microsoftCodeSign.singedTrusted.count)
		numberOfSingedNotFullChain = str(microsoftCodeSign.singedNotFullChain.count)
		numberOfUnrecognizedOrCorrupted = str(microsoftCodeSign.unrecognized.count)
		numberOfUnsigned = str(microsoftCodeSign.unsigned.count)
		siningSubjects = [*microsoftCodeSign.singedTrusted.singingSubject, *microsoftCodeSign.singedNotFullChain.singingSubject]
	# Get Red Hat results
	elif rpmSigning.found:
		numberOfSingedFiles = str(rpmSigning.signed.count)
		numberOfSingedNotFullChain = str(rpmSigning.singedKeyNotFound.count)
		numberOfUnrecognizedOrCorrupted = str(rpmSigning.corrupted.count)
		numberOfUnsigned = str(rpmSigning.unsigned.count)
		siningSubjects = [*rpmSigning.signed.singingSubject, *rpmSigning.singedKeyNotFound.singingSubject, *rpmSigning.efi.singingSubjectTrusted, *rpmSigning.efi.singingSubject]
	# Get VMWare results
	elif vmwareMicrosoftAndOvf.found:
		numberOfSingedFiles = str(vmwareMicrosoftAndOvf.singedTrusted.count)
		numberOfSingedNotFullChain = str(vmwareMicrosoftAndOvf.singedNotFullChain.count)
		numberOfUnrecognizedOrCorrupted = str(vmwareMicrosoftAndOvf.unrecognized.count)
		numberOfUnsigned = str(vmwareMicrosoftAndOvf.unsigned.count)
		siningSubjects = [*vmwareMicrosoftAndOvf.singedTrusted.singingSubject, *vmwareMicrosoftAndOvf.singedNotFullChain.singingSubject, *vmwareMicrosoftAndOvf.ovf.vendor]
	else:
		printError("Could not find any results to CSV")
		exit(1)

	resultsToSave = [str(currentUnixTime),
	str(buildVersion),
	inputFile,
	hashStatus,
	hashResults.generateSHA256,
	hashResults.generateSHA512,
	"",
	numberOfSingedFiles,
	numberOfSingedNotFullChain,
	numberOfUnsigned,
	numberOfUnrecognizedOrCorrupted]
	resultsToSave.extend(siningSubjects)

	# Check if files exist
	csvExist = exists(csvFilePath)

	# Write results to CSV
	with open(csvFilePath, mode='a') as report:
		resultsCsv = csv.writer(report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		# Write header if newly created file
		if not csvExist:
			headerCsv = csv.DictWriter(report, delimiter=',', fieldnames=header)
			headerCsv.writeheader()
		resultsCsv.writerow(resultsToSave)
