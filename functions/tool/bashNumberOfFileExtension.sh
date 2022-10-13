#!/bin/bash

cat $1 | awk -F . '{print $NF}' | sort | uniq -c | awk '{print $1,$2}'