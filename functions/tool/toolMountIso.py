#!/usr/bin/env python3

# imports of libraries
import subprocess

#tools
from .toolColoredOutput import printInfo

def mountIso (inputIso):
	printInfo("Mounting ISO file may require sudo privileges")

	path = "./extractedISO"
	#sudo mount -o ro $inputFile ./extractedISO
	cmd = ['sudo', 'mount', '-o', 'ro', inputIso, path]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = proc.communicate()

	return path

def UnMountIso (inputPath):
	printInfo("Unmounting ISO file may require sudo privileges")

	#sudo mount -o ro $inputFile ./extractedISO
	cmd = ['sudo', 'umount', inputPath]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = proc.communicate()