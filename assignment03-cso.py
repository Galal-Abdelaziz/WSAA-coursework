"""
Weekly Assignment 03
Author: Galal Abdelaziz
File Name: assignment03-cso.py
Task: Write a program that retrieves the dataset for the "exchequer account (historical series)" from the CSO, and stores it into a file called "cso.json".
Dataset found on this URL "https://data.cso.ie/table/FIQ02"
"""

import requests
import json

# URL for the "Exchequer Account (Historical Series)" dataset
url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/FIQ02/JSON-stat/2.0/en"

# Fetch the dataset
response = requests.get(url)

# Check for successful response
if response.status_code == 200:
    data = response.json()
    
    # Save the dataset to a file with indentation for readability
    with open("cso.json", "w") as file:
        json.dump(data, file, indent=4)
        
    print("Data saved to cso.json")
else:
    print(f"Error: Unable to fetch data (status code: {response.status_code})")