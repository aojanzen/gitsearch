#!/usr/bin/env python3

"""
gitsearch.py

Author: Dr. Andreas Janzen, janzen@gmx.net
Date: 2020-07-24
"""

import os
import sys

from collections import namedtuple
from github import Github

token = os.environ["GIT_ACCESS_TOKEN"]
gh = Github(token)

if len(sys.argv) < 3:
    print("Syntax: gitsearch <language> <topic>") # [<topic2>...]")
    exit()
else:
    language = sys.argv[1]
    topic = sys.argv[2]
    searchstring = f"language:{language} topic:{topic}"
    results = gh.search_repositories(searchstring)

print(f"\n\ngitsearch has found {results.totalCount} repositories with topic {topic}:")
print()

for index, repository in enumerate(results, 1):
    print(f"({index}) {repository.name}")


print()
#    found = gh.search_topics("chess")
