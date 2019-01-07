# github_api_sample
A simple script that returns data from GitHub resourses.

The script is made in Python 3.6. To run it simply install the requirements.txt file and run app/app.py

GitHub API provides a number of 60 requests/hour if the caller isn't authenticated so it is advised to use a basic authentication with username and password. They can be passed in the GitHub class constructor and the request rate will jump to 5000 requests/hour (documented on 06/01/2019) 
