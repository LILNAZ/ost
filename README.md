# Open Source Tvätt - Analysis of Signatures in Code and Hash (OST ASCH)

## Setup:
-------------

1. Run the command `sha256sum -c scriptBuild_{BUILD NUMBER}.sha256sum` in the root on this folder to verify that the code is intact.
	A. The command is part of "coreutils" so it should exist on most standard installations

2. Run the `setup.sh` script as a normal user.
	A) This will install the necessary dependencies.
	b) If you get and "OK" from the script then all necessary dependencies are installed.


## Instructions:
-------------

1. Run "python3 OpenSourceTvatt.py" with the appropriate flags for the use case and the results will be placed in `./output` as well as printed in the terminal

2. Look at the results in `./output/FILENAME/TIME_OF_COMMAND/` as well as the csv report in `./output/report.csv`


3. For help on what flags to use run with "-h" or "--help" to get the flags to use
```
-f FILE, --filepath FILE			Absolute or relative filepath to the file that should be tested
-s HASH-SUM, --sha256 HASH-SUM		Vendor SHA 256 to test against
TYPE:
	-m, --microsoft					For Microsoft file or ISO
	-r, --rhel						For Red Hat Enterprise Linux file or ISO
	-v, --vmware					For VMWare ISO
```
3. The flags can be used in any order and long and short can be used interchangeably. For example:
```
python3 OpenSourceTvatt.py --filepath ~/Downloads/Windows_10_20h2.iso --sha256 365cc933f39d5aa4c869481891bee5903e7000eed9f9420d9c9bafccdcb6fb0b --microsoft
```
```
python3 OpenSourceTvatt.py -f /home/user/Downloads/AccessRuntime.exe -s 4e5172539b4f5bbfb1286fe5cb849648e3413540dc32a5589ee6f47bf4bf6f71 -m
```
```		
python3 OpenSourceTvatt.py -f "./Red Hat.iso" -s ca5e31e4f13edf64102d6e6aea05ccc34c0013339c0c1bf2fc779d8e375e7b42 -r
```
```
python3 OpenSourceTvatt.py -f "./package.rpm" -s 5c476f28435bc633f07a88ff07ab5f782b600ba91888e0ba6c21455f2eba2456 -r
```
```
python3 OpenSourceTvatt.py --vmware -f ~/Downloads/VMware-VCSA-all-7.0.3-20051473.iso -s 01D2FCF9672B2E0F63BCE76CA3FE49D253ED58D4B9361E5DC46C5C4944868C0B
```
