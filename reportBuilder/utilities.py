import datetime
import os
import re
import requests

from .graphQL import PR_JSON
from .url import GRAPHQL_URL

def get_dates(weeks):
    #Get the dates for the API query
    until = datetime.datetime.now().strftime("%Y-%m-%d") 
    since = (datetime.datetime.strptime(until, "%Y-%m-%d") - datetime.timedelta(weeks=weeks)).strftime("%Y-%m-%d")

    return since, until

def get_pull_request_data(repo, since, until):
    github_token = os.getenv('GITHUB_API_TOKEN')

    #Create the API query
    headers = {'Authorization': 'token %s' % github_token}
    json_body = PR_JSON

    try: 
        #Send the request
        response = requests.post(GRAPHQL_URL, json={'query': json_body.format(repo=repo, since=since, until=until)}, headers=headers)
        json_response = response.json()

        #Parse the response
        raw_pr_data = json_response["data"]["search"]["nodes"]
        pr_data = []

        for info in raw_pr_data:
            title = info["title"]
            body_html = info["bodyHTML"]
            created_at = info["createdAt"]
            merged_at = info["mergedAt"]
            changed_files = info["files"]["nodes"]
            author_name = info["author"]["name"]
            
            pr_info = {
                "title": title,
                "body_html": body_html,
                "created_at": created_at,
                "merged_at": merged_at,
                "author_name": author_name,
                "files": []
            }

            print("Title:", title)
            print("Body HTML:", body_html)
            print("Created At:", created_at)
            print("Merged At:", merged_at)
            print("Author Name:", author_name)
        
            for file in changed_files:
                path = file["path"]
                additions = file["additions"]
                deletions = file["deletions"]
                change_type = file["changeType"]
                
                file_info = {
                    "path": path,
                    "additions": additions,
                    "deletions": deletions,
                    "change_type": change_type
                }

                pr_info["files"].append(file_info)

                print("File Path:", path)
                print("Additions:", additions)
                print("Deletions:", deletions)
                print("Change Type:", change_type)
            
            pr_data.append(pr_info)
    
        return pr_data
    
    # Error handling
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request error: {str(e)}")
    
    except (ValueError, KeyError) as e:
        raise ValueError(f"Response error: {str(e)}")

def get_general_info_dictionary(summary, since, until):
    #Create a dictionary with general info about the pull requests

    date_range = since + " to " + until

    general_info = {
        "summary": summary,
        "date_range": date_range
    }

    return general_info

def get_images(pr_data):
    #Get the first two images from each pull request
    pattern = r'<img[^>]*src="([^"]+)"[^>]*>'

    for pr_info in pr_data:
        image_links = re.findall(pattern, pr_info["body_html"])

        try:
            pr_info["images"] = {
                "first_link": image_links[0] if len(image_links) > 0 else None,
                "second_link": image_links[1] if len(image_links) > 1 else None
            }
        except IndexError:
            #Handle the case where there are no images
            pr_info["images"] = {
                "first_link": None,
                "second_link": None
            }

def get_user_email(username):
    github_token = os.getenv('GITHUB_API_TOKEN')

    headers = {
        'Authorization': f'Token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(f'https://api.github.com/users/{username}', headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        email = user_data.get('email')
        return email
    else:
        return None