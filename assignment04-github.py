"""
Weekly Assignment 04
Author: Galal Abdelaziz
File Name: assignment04-github.py
Task: Write a program in python that will read a file from a repository, The program should then replace all the instances of the text "Andrew" with your name, then commit those changes and push the file back to the repository (You will need authorisation to do this).
Dataset found on this URL "https://data.cso.ie/table/FIQ02"
"""

import requests
import base64
from config import config

# GitHub repo info
username = "Galal-Abdelaziz"
repo = "WSAA-coursework"
file_path = "original-assignment04.txt"
branch = "main"

# GitHub API info
api_key = config["assignment04key"]
headers = {
    "Authorization": f"token {api_key}",
    "Accept": "application/vnd.github.v3+json"
}

# Construct the API URL
url = f"https://api.github.com/repos/{username}/{repo}/contents/{file_path}?ref={branch}"

# Request the file content
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Error fetching file: {response.status_code}")
    print(response.text)
    exit()

try:
    file_data = response.json()
except Exception as e:
    print(f"Failed to parse response as JSON: {e}")
    print(response.text)
    exit()

# Decode base64 content
encoded_content = file_data.get("content")
if not encoded_content:
    print("No content found in the file.")
    exit()

decoded_content = base64.b64decode(encoded_content).decode("utf-8")

# Replace "Andrew" with "Galal"
modified_content = decoded_content.replace("Andrew", "Galal")

# Prepare the data for the commit
commit_message = "Update original-assignment04.txt to replace 'Andrew' with 'Galal'"
sha = file_data.get("sha")  # Get the SHA of the existing file

# Create the payload for the update
update_payload = {
    "message": commit_message,
    "content": base64.b64encode(modified_content.encode("utf-8")).decode("utf-8"),
    "sha": sha,
    "branch": branch
}

# Push the changes to the repository
update_url = f"https://api.github.com/repos/{username}/{repo}/contents/{file_path}"
update_response = requests.put(update_url, headers=headers, json=update_payload)

if update_response.status_code == 200:
    print("File updated successfully.")
else:
    print(f"Error updating file: {update_response.status_code}")
    print(update_response.text)

