#!/bin/bash

rpmSingedOutput=$1

cat $rpmSingedOutput | grep -Eio "[0-9a-fA-F]{6,}" | sort -u