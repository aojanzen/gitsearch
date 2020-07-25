#!/usr/bin/env python3

"""
gitsearch.py

Author: Dr. Andreas Janzen, janzen@gmx.net
Date: 2020-07-24
"""

import datetime
import os
import sys
import time
import webbrowser

from collections import namedtuple
from github import Github


# GENERAL DEFINITIONS

candidate = namedtuple("candidate", "full_name description clone_url git_url\
        open_issues size stargazers_count")

now = datetime.datetime.now()
token = os.environ["GIT_ACCESS_TOKEN"]

candidate_list = list()


def get_Github_data():
    gh = Github(token)

    if len(sys.argv) < 3:
        print("Syntax: gitsearch <language> <topic>") # [<topic2>...]")
        exit()
    else:
        language = sys.argv[1]
        topic = sys.argv[2]
        searchstring = f"language:{language} topic:{topic}"
        results = gh.search_repositories(searchstring)

        print(f"\ngitsearch has found {results.totalCount} matching repositories.")
        print(f"Language: {language}, topic: '{topic}'.\n")
        print("Processing data -- please wait.")

        for repo in results:
            if not repo.private and repo.has_issues\
                    and (now-repo.updated_at).days <= 30:
                new = candidate(
                        repo.full_name,
                        repo.description,
                        repo.clone_url,
                        repo.git_url,
                        repo.open_issues,
                        repo.size,
                        repo.stargazers_count
                        )

                candidate_list.append(new)


def display_repos():
    print("\nDisplay most relevant results:")
    print("="*30+"\n")
    print("(1) Stargazers count")
    print("(2) Open issues")
    print("(3) Size")
    choice = int(input("\nChoose sorting criterion > "))
    num_tabs = int(input("Number of repos to be opened in webbrowser > "))

    if choice == 1:
        sort_func = lambda repo: repo.stargazers_count
    elif choice == 2:
        sort_func = lambda repo: repo.open_issues
    elif choice == 3:
        sort_func = lambda repo: repo.size
    else:
        print("\nYOU ENTERED AN INVALID SORTING CRITERION!\n")
        display_repos()

    chosen_repos = sorted(candidate_list, key=sort_func, reverse=True)[:num_tabs]

    open_url = chosen_repos.pop(0).clone_url
    webbrowser.open_new(open_url)
    time.sleep(1)

    while chosen_repos: # ... not empty
        open_url = chosen_repos.pop(0).clone_url
        webbrowser.open_new_tab(open_url)

    return -1


def make_pull_request(create_repo):
    print("\nCreate folder and pull git data for repo {}?")


# MAIN
get_Github_data()
create_repo = display_repos()

if create_repo != -1:
    make_pull_request(create_repo)

