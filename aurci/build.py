import subprocess
import os


def dmakepkg(package):
    path = "./packages/{0}/".format(package)
    if os.path.isfile(path + "PKGBUILD"):
        try:
            subprocess.run(["dmakepkg", "-xy"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, cwd=path, check=True)
        except subprocess.CalledProcessError:
            with open("failed.txt", "w") as fobj:
                fobj.write(package + "\n")
                pass
    
def build(package):
    if os.path.exists("failed.txt"):
        os.remove("failed.txt")
    if package=="all":
        for folder in os.listdir("./packages"):
            dmakepkg(folder)    
    else:
        dmakepkg(package)