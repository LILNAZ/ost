#!/usr/bin/env python3

# imports of libraries
import argparse


def commandLineFlags(buildVersion):
	# Helper text set up
	Color_Off='\033[0m'		# Text Reset
	boldText='\033[1m'			# BOLD
	

	descriptionText = '''Open Source Tvätt (OST) is a \"simple\" python script that verifies SHA256 sums and verifies signings of microsoft styled files and rpm packages.'''
	epilogText = '''This tool is not 100% accurate and can give false positives. Thus, the script still rely that you ''' + boldText + '''trust the source!''' + Color_Off + '''
The script also has a limitation that it dose not unpack any archives.

Version: ''' + str(buildVersion)


	#setup of flag argument
	parser = argparse.ArgumentParser (formatter_class=argparse.RawDescriptionHelpFormatter, description=descriptionText,epilog=epilogText)

	parser.add_argument('-f', '--filepath', type=str, required=True, help="Absolute or relative filepath to the file that should be tested", metavar=boldText + "FILE" + Color_Off)
	parser.add_argument('-s', '--sha256', type=str, required=True, help="Vendor SHA 256 to test against",metavar=boldText + "HASH-SUM" + Color_Off)

	parser.add_argument('-m', '--microsoft', action='store_true', help="For Microsoft file or ISO")
	parser.add_argument('-r', '--rhel', action='store_true', help="For Red Hat Enterprise Linux file or ISO")
	parser.add_argument('-v', '--vmware', action='store_true', help="For VMWare ISO")

	args = parser.parse_args ()

	return args
