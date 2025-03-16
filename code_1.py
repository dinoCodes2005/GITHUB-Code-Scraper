from bs4 import BeautifulSoup
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

#edit this as per your choice
repo_owner = "dinoCodes2005"
repo_name = "InkVara"
branch_name = "main"

#edit the key points that need to be found in the code base
things_to_fetch = ["API_KEY","Blog"]

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("Github Token is Invalid !!")

API_URL = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees/{branch_name}?recursive=1"


#clearing the file before writing on it
with open("htmlcode.txt", "w", encoding="utf-8") as file:
    try:
        file.write("")
    except Exception as e:
         print(e)

#scraping the code from the dynamically generated file_path
def scrape_code(file_path):
    url = f"https://github.com/{repo_owner}/{repo_name}/blob/{branch_name}/{file_path}"
    print(url)
    try:
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "lxml")

        #tag containing the code 
        script = soup.find("script",{"data-target" :"react-app.embeddedData"})

        #crucial part - converts the JSON string to Python dictionary
        jsonValue = json.loads(script.text)
        code_block = jsonValue["payload"]["blob"]["rawLines"]
        code_string = ""

        fetched_output = []
        for things in things_to_fetch:
            for code in code_block:
                if things.lower() in code.lower():
                    fetched_output += [code]
        print(fetched_output)

        # for code in code_block:
        #     code_string += code +"\n"
        # print(code_string)
        
        #append the outputs to the file
        with open("htmlcode.txt", "a", encoding="utf-8") as file:
            try:
                for code in fetched_output:
                    file.write(code.strip()+"\n")
            except Exception as e:
                print(e)
    except Exception as e:
        print(f"skipping - {file_path}\n")      

#getting the repo structure using github api
def repo_structure():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(API_URL,headers=headers)
    response_dict = json.loads(response.text)
    response_tree = response_dict["tree"]
    try:
        files = []
        for data in response_tree:
            file_url = data["path"]
            #excluding image and log files
            if (not file_url.endswith((".jpg", ".png", ".xml")) and not file_url.endswith((".md", ".txt", ".pyc"))):
                files.append(file_url)
            
        return files
    except Exception as e:
        print("Unable to fetch the Response Tree")

#looping through all the file_urls to scrape the code
file_urls = repo_structure()
for urls in file_urls:
    scrape_code(urls)
    
