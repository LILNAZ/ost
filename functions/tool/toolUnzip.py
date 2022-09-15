#!/usr/bin/env python3

# imports of libraries
import os
import subprocess

from .toolGetFileType import *
from .toolColoredOutput import *

def extractFile (inputFile, outputDir):
	# verify if output directory exist
	createOutputDir(outputDir)

	# Get the file magic number form the input file
	magic = getFileMagic(inputFile)

	if magic == "application/x-7z-compressed":
		SevenZExtract(inputFile, outputDir)

	elif magic == "application/zip":
		zipExtract(inputFile, outputDir)

	elif magic == "application/x-bzip2":
		tarExtract(inputFile, outputDir)

	elif magic == "application/gzip":
		tarExtract(inputFile, outputDir)

	elif magic == "application/x-tar":
		tarExtract(inputFile, outputDir)

	elif magic == "application/x-xz":
		tarExtract(inputFile, outputDir)

	elif magic == "application/x-rar":
		rarExtract(inputFile, outputDir)

	else:
		printWarn("Not a file that could be extracted!")


def SevenZExtract (SevenZFile, outputDir):
	sevenZoutpath = "-o" + outputDir
	cmd = ['7z', 'x', SevenZFile, '-C', sevenZoutpath]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = proc.communicate()

def zipExtract (zipFile, outputDir):
	cmd = ['unzip', zipFile, '-d', outputDir]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = proc.communicate()

def tarExtract (tarFile, outputDir):
	cmd = ['tar', '-xf', tarFile, '-C', outputDir]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = proc.communicate()

def rarExtract (rarFile, outputDir):
	cmd = ['rar', 'x', rarFile, outputDir]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = proc.communicate()


def createOutputDir (outputDir):
	os.makedirs(outputDir, exist_ok=True)


def CleanExtractedFiles (extractedFilesDir):
	for f in os.listdir(extractedFilesDir):
		os.remove(os.path.join(extractedFilesDir, f))
