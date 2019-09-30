import subprocess
import os


def dmakepkg(package):
    path = "./packages/{0}/".format(package)
    if os.path.isfile(path + "PKGBUILD"):
        try:
             process = subprocess.run(["dmakepkg", "-xy"], stderr=subprocess.PIPE, cwd=path, check=True)
             process
             return None
        except subprocess.CalledProcessError:
            return process.stderr
    
def build(package):
    if package=="all":
        for folder in os.listdir("./packages"):
            dmakepkg(folder)    
    else:
        dmakepkg(package)