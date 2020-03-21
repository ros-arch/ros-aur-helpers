from github import Github
from git import Repo
from aurci import sed
import os


class Clone:
    def __init__(self, package, verbosity, output):
        self.package = package
        self.path = os.path.join("./packages/{0}".format(self.package))
        self.url = "git@github.com:ros-melodic-arch/{0}.git".format(self.package)
        self.verbosity = verbosity
        self.output = output

    def cloning(self):
        Repo.clone_from(self.url, self.path)

    def clone(self):
        if self.package=="all":
            g = Github("YOUR_OAUTH_KEY")
            o = g.get_organization("ros-melodic-arch")
            repos = o.get_repos(type="all", sort="full_name", direction="desc")
            for repo in repos:
                Clone(repo.name, self.verbosity, self.output).cloning()
        else:
            self.cloning()


class Pull:
    def __init__(self, package, verbosity, output):
        self.package = package
        self.path = "./packages/{0}/".format(package)
        self.verbosity = verbosity
        self.output = output

    def pull(self):
        if self.package=="all":
            for folder in os.listdir("./packages"):
                Pull(folder, self.verbosity, self.output).pull()
        else:
            Repo(path=self.path).git.stash()
            Repo(path=self.path).git.stash("clear")
            try:
                Repo(path=self.path).remote("origin").pull()
            except:
                if self.output:
                    print("Pulling of {0} failed".format(self.package))

            sed.rmlinematch(self.package, "success.txt", dryrun=False)
