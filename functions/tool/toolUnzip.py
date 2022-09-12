#!/usr/bin/env python3

# imports of libraries
import os

from .toolGetFileType import *


def extractFile (inputFile, outputDir):
	magic = getFileMagic(inputFile)

	if magic == "application/x-7z-compressed":
		print ("OK!1")
	elif magic == "application/x-bzip2":
		print ("OK!2")
	elif magic == "application/gzip":
		print ("OK!3")
	elif magic == "application/x-tar":
		print ("OK!4")
	elif magic == "application/x-xz":
		print ("OK!5")
	elif magic == "application/zip":
		print ("OK!6")
	else:
		print ("NOK!")

def SevenZExtract (SevenZFile, outputDir):
	return

def bzip2Extract (bz2File, outputDir):
	return

def gzipExtract (gzipFile, outputDir):
	return

def tarExtract (tarFile, outputDir):
	return

def xzExtract (xzFile, outputDir):
	return

def zipExtract (zipFile, outputDir):
	return


def CleanExtractedFiles (extractedFilesDir):
	for f in os.listdir(extractedFilesDir):
		os.remove(os.path.join(extractedFilesDir, f))
