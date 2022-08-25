#!/bin/bash

keyLocation=$1
workingFile=$2


keyIDtoRPMkeyName () {
	currKey=$(gpg --show-keys --with-fingerprint $1 | grep -Eio "[0-9a-fA-F]{4,} [0-9a-fA-F]{4,} [0-9a-fA-F ]{4,}" | tr -d ' ')
	echo "$currKey:$1" >> $2

}

# Find all fingerprint in $1
find $keyLocation -name '*GPG-KEY*' -type f -print0 | while IFS= read -r -d '' file; do keyIDtoRPMkeyName $file $workingFile; done
