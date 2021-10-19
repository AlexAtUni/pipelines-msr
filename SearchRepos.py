import requests;
from github import Github;

g = Github('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') #in this object we input the token that allows us to do more api requests to the github api

query = f'filename:".gitlab-ci" extension:yml' #this query respect a github convention for searching code on the platform. Here we look for files that have ".gitlab-ci" in the filename and have the .yml extension
result = g.search_code(query, order='desc') #this requests to github api files that match our query. 
print(f'Found {result.totalCount} file(s)')

for file in result:
    print(file.html_url) #here we print the html url for each file we found. you might hit a rate limit exception
    

