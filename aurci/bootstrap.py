from github import Github
from git import Repo
from aurci.general import Routines
import os


class Clone(Routines):
    def __init__(self, package, verbosity, output):
        Routines.__init__(self, package, verbosity, output)
        self.url = "git@github.com:ros-melodic-arch/{0}.git".format(self.package)

    def cloning(self):
        Repo.clone_from(self.url, self.path)

    def clone(self):
        if self.package=="all":
            repos = self.gh_organization.get_repos(type="all", sort="full_name", direction="desc")
            for repo in repos:
                Clone(repo.name, self.verbosity, self.output).cloning()
        else:
            self.cloning()


class Pull(Routines):

    def pull(self):
        if self.package=="all":
            for folder in os.listdir("./packages"):
                Pull(folder, self.verbosity, self.output).pull()
        else:
            repo = Repo(path=self.path)
            repo.git.stash()
            repo.git.stash("clear")
            head_before = repo.head.object.hexsha
            try:
                repo.remote("origin").pull()
                if head_before != repo.head.object.hexsha:
                    self.delete_package_line("success.txt")
            except BaseException as e:
                if self.output:
                    print("Pulling of {0} failed".format(self.package))
                    if self.verbosity:
                        print(e)
