#!/bin/bash
data=$(cat pwdbackup); for i in $(seq 1 13); do data=$(echo $data | tr -d ' ' | base64 -d); done; echo $data
