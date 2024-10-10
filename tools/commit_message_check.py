#!/usr/bin/env python3
import os
import sys
import subprocess
import re

# Get the current branch
branch_name = subprocess.check_output(
    ['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()

if branch_name == "main":
    # Read the commit message from the file passed to the hook
    commit_msg_filepath = sys.argv[1]

    with open(commit_msg_filepath, 'r') as file:
        commit_msg = file.read()

    pattern = r"^(build|chore|ci|docs|feat|fix|perf|style|refactor|test)(\([a-z0-9\-_]+\))?(!)?:\s.*"

    # Check if the commit message starts with a valid tag
    if not re.match(pattern, commit_msg):

        print("Error: Commit message must follow the Angular format (e.g., "
              "'feat: description' or 'fix(scope): description').")

        sys.exit(1)

sys.exit(0)
