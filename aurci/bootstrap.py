from github import Github
from git import Repo
import os.path as p


class Clone:
    def __init__(self, package):
        self.package = package
        self.path = p.join("./packages/{0}".format(self.package))
        self.url = "git@github.com:ros-melodic-arch/{0}.git".format(self.package)

    def cloning(self):
        Repo.clone_from(self.url, self.path)

    def clone(self):
        if self.package=="all":
            g = Github("YOUR_OAUTH_KEY")
            o = g.get_organization("ros-melodic-arch")
            repos = o.get_repos(type="all", sort="full_name", direction="desc")
            for repo in repos:
                Clone(repo.name).cloning()
        else:
            self.cloning()
