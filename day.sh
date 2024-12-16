#!/usr/bin/env python3
import os
import sys
from datetime import datetime

if len(sys.argv) != 2:
  print("Usage: {} <day>".format(sys.argv[0]))
  sys.exit(1)

day = sys.argv[1]

if not day.isdigit() or not (1 <= int(day) <= 25):
  print("Usage: {} <day>".format(sys.argv[0]))
  print("<day> must be a number between 1 and 25")
  sys.exit(1)

day0 = day.zfill(2)
date = datetime.now().strftime("%Y-%m-%d")

os.makedirs(f"src/day{day0}", exist_ok=True)

for filename in os.listdir("src/day00"):
  src = os.path.join("src/day00", filename)
  dst = os.path.join(f"src/day{day0}", filename.replace("day00", f"day{day0}"))
  with open(src) as fsrc, open(dst, 'w') as fdst:
    content = fsrc.read()
    content = content.replace("DAY = 1", f"DAY = {day}")
    content = content.replace("https://adventofcode.com/2024/day/1", f"https://adventofcode.com/2024/day/{day}")
    content = content.replace("Date: 2023-12-01", f"Date: {date}")
    fdst.write(content)

print(f"Day {day0} ready")
