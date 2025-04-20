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

# Fetch the file content from GitHub
url = f"https://api.github.com/repos/{username}/{repo}/contents/{file_path}?ref={branch}"
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

# Modify the content
modified_content = decoded_content.replace("Andrew", "Galal")
encoded_modified_content = base64.b64encode(modified_content.encode("utf-8")).decode("utf-8")


# ======= OPTION 1: Update Existing File =======
"""
commit_message = "Update original-assignment04.txt to replace 'Andrew' with 'Galal'"
sha = file_data.get("sha")  # Required for updating existing files

update_payload = {
    "message": commit_message,
    "content": encoded_modified_content,
    "sha": sha,
    "branch": branch
}

update_url = f"https://api.github.com/repos/{username}/{repo}/contents/{file_path}"
update_response = requests.put(update_url, headers=headers, json=update_payload)

if update_response.status_code == 200:
    print("File updated successfully.")
else:
    print(f"Error updating file: {update_response.status_code}")
    print(update_response.text)
"""

# ======= OPTION 2: Upload as New File =======

new_file_path = "modified-assignment04.txt"  # Change filename here
commit_message = "Upload modified copy of original-assignment04.txt"

upload_payload = {
    "message": commit_message,
    "content": encoded_modified_content,
    "branch": branch
}

upload_url = f"https://api.github.com/repos/{username}/{repo}/contents/{new_file_path}"
upload_response = requests.put(upload_url, headers=headers, json=upload_payload)

if upload_response.status_code == 201:
    print(f"New file '{new_file_path}' uploaded successfully.")
else:
    print(f"Error uploading file: {upload_response.status_code}")
    print(upload_response.text)
