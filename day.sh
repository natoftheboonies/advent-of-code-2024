#!/bin/bash
# usage:  ./day.sh 1
# creates day01 directory and copies template files to it
zfill() {
  local n=$1
  local w=2
  printf "%0${w}d" $n
}

day=$1
# exit if day is not a number
if ! [[ $day =~ ^[0-9]+$ ]] || [ $day -lt 1 ] || [ $day -gt 25 ]; then
    echo "Usage: $0 <day>"
    echo "<day> must be a number between 1 and 25"
    exit 1
fi

day0=$(zfill $1)
date=$(date "+%Y-%m-%d")

mkdir -p src/day$day0
cp src/day00/* src/day$day0
mv src/day$day0/day00.py src/day$day0/day$day0.py
# replace DAY = 1 with DAY = $day
sed -i'' -E "s/DAY = 1/DAY = $day/g" src/day$day0/day$day0.py
# replace "https://adventofcode.com/2024/day/1" with $day
sed -i'' -E "s|https://adventofcode.com/2024/day/1|https://adventofcode.com/2024/day/$day|g" src/day$day0/day$day0.py
# populate Date like "Date: 2023-12-01"
sed -i'' -E "s/Date: 2023-12-01/Date: $date/g" src/day$day0/day$day0.py

echo "Day $day0 ready"
