import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse
from requests.exceptions import HTTPError


class GitHub():

    
    def __init__(self, owner, repo, resources):
        self.owner = owner
        self.repo = repo
        self.resources = resources

        self.username = ""
        self.password = ""

        self.flow = {
            "pages": {
                "next": 1,
                "current": 0,
                "last": 0,
            },
            "repository": 0,
            "resource": 0
        }


    def update_flow(self, request):
        next_page_link = request.links["next"]["url"]
        self.flow["pages"]["next"] = urlparse(next_page_link).query.split("&")[1][5:]
        last_page_link = request.links["last"]["url"]
        self.flow["pages"]["last"] = urlparse(last_page_link).query.split("&")[1][5:]
        self.flow["pages"]["current"] += 1


        if self.flow["pages"]["current"] == self.flow["pages"]["last"]:
            self.flow["pages"]["next"] = 1
            self.flow["pages"]["last"] = 0
            self.flow["pages"]["current"] = 0
            self.flow["resource"] += 1
            if self.flow["resource"] > len(self.resources):
                self.flow["resource"] = 0
                self.flow["repository"] += 1
                if self.flow["repository"] > len(self.repo):
                    self.flow = {
                        "pages": {
                            "next": 1,
                            "current": 0,
                            "last": 0,
                        },
                        "repository": 0,
                        "resource": 0
                    }

                    print("All data has been read ! You can start all over again now by calling the 'read' method again.")


    def read(self):
        url = "https://api.github.com/repos/{}/{}/{}".format(self.owner, self.repo[self.flow["repository"]], self.resources[self.flow["resource"]])
        auth = HTTPBasicAuth(self.username, self.password)
        params = {
            'per_page': '50',
            'page': str(self.flow["pages"]["next"]),
        }

        try:
            r = requests.get(url, auth=auth, params=params)
        except HTTPError as e:
            print(e)

        self.update_flow(r)
        
        return r.json()



if __name__ == "__main__":

    gh = GitHub(owner="moby",
            repo=["moby", "buildkit", "tool"], 
            resources=["commits", "pulls", "issues"])


    print(gh.read())
    print(gh.read())
