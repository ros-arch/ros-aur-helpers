import subprocess
import os

class Build:
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
                    return 1
        else:
            raise BaseException("No PKBUILD existing: ", self.path)

    def build(self):
        if os.path.exists("failed.txt"):
            os.remove("failed.txt")
        if self.package=="all":
            for folder in os.listdir("./packages"):
                Build(folder).dmakepkg
        else:
            Build(self.package).dmakepkg()
