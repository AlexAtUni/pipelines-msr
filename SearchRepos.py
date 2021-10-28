import requests;
from github import Github;
import pandas;
import numpy as np;
access_token='' # input here access token. 

#!!!! do not commit with token visible !!!!

g = Github(access_token) #in this object we input the token that allows us to do more api requests to the github api

 #here we print the html url for each file we found. you might hit a rate limit exception
def populateWithNewRepos(DataFrame):
    query = f'filename:".gitlab-ci" extension:yml' #this query respect a github convention for searching code on the platform. Here we look for files that have ".gitlab-ci" in the filename and have the .yml extension
    result = g.search_code(query, order='desc') #this requests to github api, files that match our query. 
    print(f'Found {result.totalCount} file(s)')
    for file in result:
        html_url= file.html_url
        file_name= file.name
        repo = file.repository.name
        user = file.repository.owner.login
        newRow = {"user":user, "repo": repo, "file":file_name, "repos html url": html_url}
        DataFrame.append(newRow, ignore_index=True)
    DataFrame.dropduplicates()
        #add here a way to add rows in the csv file 

def get_creation_date(user, repo):
    url='https://api.github.com/repos/{}/{}'.format(user, repo)
    req = requests.get(url)
    json_data= req.json()
    return json_data['created_at']    
# we could write the file.html_url directly into the csv file and do same operation as in google sheet.
reposDF= pandas.read_csv("Repos.csv")

for row in reposDF.iterrows():
    date=get_creation_date(row["user"], row["repo"])
    row["Date of creation"]=date


#TODO:
# get from the reposDF the user and repos and delete duplicates in the repository name for each owner               DONE
# loop hrough each of them and get the creation date                                                                DONE
# then go again through each user and repo to get the commits date ##json_data[-1]['commit']['author']['date']      
# compare the comit date with today to get number of commits during a period of time


#the next lines have been copied from 'https://gist.github.com/yershalom/a7c08f9441d1aadb13777bce4c7cdc3b' to test information retrieval on commits 

'''
def get_all_commits_count(owner, repo, sha):
    first_commit = get_first_commit(owner, repo)
    compare_url = '{}/repos/{}/{}/compare/{}...{}'.format(base_url, owner, repo, first_commit, sha)

    commit_req = requests.get(compare_url)
    commit_count = commit_req.json()['total_commits'] + 1
    print(commit_count)
    return commit_count


def get_first_commit(owner, repo):
    url = '{}/repos/{}/{}/commits'.format(base_url, owner, repo)
    req = requests.get(url) #this retrieves all information about al the committs from the given owenr and repo
    json_data = req.json()

    if req.headers.('Link'):
        page_url = req.headers.get('Link').split(',')[1].split(';')[0].split('<')[1].split('>')[0]
        req_last_commit = requests.get(page_url)
        first_commit = req_last_commit.json()
        first_commit_hash = first_commit[-1]['sha']
    else:
        first_commit_hash = json_data[-1]['sha']
    return first_commit_hash
'''
