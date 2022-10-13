#!/bin/bash

cat $1 | grep "Subject" | sort | uniq | grep -o '[^=]*$'