#!/usr/bin/env python3
import os
import sys
import subprocess

# Get the current branch
branch_name = subprocess.check_output(
    ['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()

if branch_name == "main":
    # Read the commit message from the file passed to the hook
    commit_msg_filepath = sys.argv[1]

    with open(commit_msg_filepath, 'r') as file:
        commit_msg = file.read()

    # Define valid tags
    valid_tags = ["build", "chore", "ci", "docs", "feat", "fix", "perf",
                  "style", "refactor", "test"]

    # Check if the commit message starts with a valid tag
    if not any(commit_msg.startswith(tag + ":") or commit_msg.startswith(tag + "!") for tag in valid_tags):

        tag_list = ", ".join([tag + ":" for tag in valid_tags])

        print(
            "Error: Commit message must start with one of the following tags: "
            f"{tag_list}.")

        sys.exit(1)

sys.exit(0)
