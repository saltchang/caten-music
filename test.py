import re

h = "我覺得金城武是世界上最帥的男人"

keywords = ["可以", "不行"]

if any(re.findall('|'.join(keywords), h)):
    print("match")
else:
    print("None")
