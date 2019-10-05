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
                return 0
            except subprocess.CalledProcessError:
                with open("failed.txt", "w") as fobj:
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
            Packages(self.package).dmakepkg()

    def mvpkg(self):
        for pkg_path in glob.iglob(self.path + "/*pkg.tar*"):
            shutil.copy(pkg_path, "./repository/")
    
    def aur_push(self):
        pkg_repo = Repo(path=self.path).create_remote('aur', "aur@aur.archlinux.org/{0}.git".format(self.package))
        pkg_repo.push

    def deploy(self):
        if os.path.exists("failed.txt"):
            os.remove("failed.txt")
        if self.package=="all":
            for folder in os.listdir("./packages"):
                try:
                    Packages(self.package).dmakepkg()
                    Packages(folder).mvpkg()
                    Packages(folder).aur_push()
                except RuntimeWarning:
                    print("Building of {0} failed".format(self.package))
                    pass
