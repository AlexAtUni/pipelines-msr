import requests;
from github import Github;

g = Github('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') #in this object we input the token that allows us to do more api requests to the github api

query = f'filename:".gitlab-ci" extension:yml' #this query respect a github convention for searching code on the platform. Here we look for files that have ".gitlab-ci" in the filename and have the .yml extension
result = g.search_code(query, order='desc') #this requests to github api files that match our query. 
print(f'Found {result.totalCount} file(s)')

for file in result:
    print(file.html_url) #here we print the html url for each file we found. you might hit a rate limit exception
    
#the next lines have been copied from 'https://gist.github.com/yershalom/a7c08f9441d1aadb13777bce4c7cdc3b' to test information retrieval on commits 

base_url = 'https://api.github.com'


def get_all_commits_count(owner, repo, sha):
    first_commit = get_first_commit(owner, repo)
    compare_url = '{}/repos/{}/{}/compare/{}...{}'.format(base_url, owner, repo, first_commit, sha)

    commit_req = requests.get(compare_url)
    commit_count = commit_req.json()['total_commits'] + 1
    print(commit_count)
    return commit_count


def get_first_commit(owner, repo):
    url = '{}/repos/{}/{}/commits'.format(base_url, owner, repo)
    req = requests.get(url)
    json_data = req.json()

    if req.headers.get('Link'):
        page_url = req.headers.get('Link').split(',')[1].split(';')[0].split('<')[1].split('>')[0]
        req_last_commit = requests.get(page_url)
        first_commit = req_last_commit.json()
        first_commit_hash = first_commit[-1]['sha']
    else:
        first_commit_hash = json_data[-1]['sha']
    return first_commit_hash
