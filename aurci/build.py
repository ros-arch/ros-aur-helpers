import subprocess
import os
import glob
import shutil
from git import Repo

class Packages:
    def __init__(self, package):
        self.package = package
        self.path = "./packages/{0}/".format(package)


    def dmakepkg(self):
        if os.path.isfile(self.path + "PKGBUILD"):
            try:
                subprocess.run(["dmakepkg", "-xy"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, cwd=self.path, check=True)
                with open("success.txt", "a") as fobj:
                    fobj.write(self.package + "\n")
                print("Building of {0} finished".format(self.package))
            except subprocess.CalledProcessError:
                with open("failed.txt", "a") as fobj:
                    fobj.write(self.package + "\n")
                    raise RuntimeWarning("Building of {0} failed".format(self.package))
        else:
            raise BaseException("No PKBUILD existing: ", self.path)

    def build(self):
        if os.path.exists("failed.txt"):
            os.remove("failed.txt")
        if self.package=="all":
            for folder in os.listdir("./packages"):
                Packages(folder).dmakepkg()
        else:
            self.dmakepkg()

    def mvpkg(self):
        for pkg_path in glob.iglob(self.path + "/*pkg.tar*"):
            shutil.copy(pkg_path, "./repository/")
    
    def aur_push(self):
        try:
            pkg_repo = Repo(path=self.path).remote(name='aur')
        except ValueError:
            pkg_repo = Repo(path=self.path).create_remote('aur', "aur@aur.archlinux.org:/{0}.git".format(self.package))
        pkg_repo.fetch()
        pkg_repo.push()

    def deploy(self):
        if os.path.exists("failed.txt"):
            os.remove("failed.txt")
        if self.package=="all":
            for folder in os.listdir("./packages"):
                with open('success.txt', "r") as fobj:
                    if folder in fobj.read():
                        pass
                    else:
                        try:
                            Packages(folder).deploy()
                        except RuntimeWarning:
                            print("Building of {0} failed".format(self.package))
                            pass
        else:
            try:
                self.dmakepkg()
                self.mvpkg()
                self.aur_push()
            except RuntimeWarning:
                print("Building of {0} failed".format(self.package))
                pass
