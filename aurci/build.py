import subprocess
import os
import sys
import glob
import shutil
from git import Repo
from aurci.general import Routines

REPO_ADD_BIN = '/usr/bin/repo-add'
MAKECHROOTPKG_BIN = '/usr/bin/makechrootpkg'


class Packages(Routines):

    FAILED_FILE = "failed.txt"
    SUCCESS_FILE = "success.txt"

    def __init__(self, package, verbosity, output):
        Routines.__init__(self, package, verbosity, output)
        self.chroot = os.environ.get(
            'CHROOT', os.path.join(self.cache_path, "chroot"))
        self.check_and_create_path(self.chroot)
        self.localrepo_path = os.path.join(self.cache_path, 'repo')
        self.check_and_create_path(self.localrepo_path)

    def makepkg(self):
        if os.path.isfile(os.path.join(self.repos_path, "PKGBUILD")):
            try:
                subprocess.run([MAKECHROOTPKG_BIN, '-c', '-d', self.localrepo_path, '-r',
                                self.chroot], stdout=(None if self.verbosity else subprocess.DEVNULL),
                               stderr=subprocess.STDOUT, cwd=self.repos_path, check=True)
                with open("success.txt", "a") as fobj:
                    fobj.write(self.package + "\n")
                if self.output:
                    print("Building of {0} finished".format(self.package))
                self.delete_package_line(self.FAILED_FILE)
            except subprocess.CalledProcessError:
                with open("failed.txt", "a") as fobj:
                    fobj.write(self.package + "\n")
                raise RuntimeWarning(
                    "Building of {0} failed".format(self.package))
        else:
            raise FileNotFoundError("No PKBUILD existing: ", self.repos_path)
        try:
            subprocess.run([REPO_ADD_BIN, 'localhost.db.tar.zst'] + glob.glob(os.path.join(self.localrepo_path, '*.pkg.tar.*')),
                           check=True, cwd=self.localrepo_path)
        except subprocess.CalledProcessError as e:
            print(e.stdout, file=sys.stderr)

    def build(self):
        if self.package == "all":
            for folder in os.listdir("./packages"):
                Packages(folder, self.verbosity, self.output).makepkg()
        else:
            self.makepkg()

    def del_old_pkg(self):
        for pkg in glob.iglob("./repository/*{0}-?.*-?-*.pkg.tar.*".format(self.package)):
            os.remove(pkg)

    def mvpkg(self):
        for pkg_path in glob.iglob(self.repos_path + "/*pkg.tar*"):
            shutil.move(pkg_path, "./repository/")

    def aur_push(self):
        try:
            pkg_repo = Repo(path=self.repos_path).remote(name='aur')
        except ValueError:
            pkg_repo = Repo(path=self.repos_path).create_remote(
                'aur', "aur@aur.archlinux.org:/{0}.git".format(self.package))
        pkg_repo.fetch()
        try:
            pkg_repo.push()
        except BaseException as e:
            if self.output:
                print("Push failed, aur remote is broken")
                if self.verbosity:
                    print(e)

    def deploy(self):
        DeprecationWarning(
            "deploy command replaced by https://github.com/bionade24/abs-cd")
        if self.package == "all":
            os.remove(self.FAILED_FILE)
            os.mknod(self.FAILED_FILE)
            for folder in os.listdir("./packages"):
                with open(self.SUCCESS_FILE, "r") as fobj:
                    if folder in fobj.read():
                        pass
                    else:
                        try:
                            Packages(folder, self.verbosity,
                                     self.output).deploy()
                        except RuntimeWarning:
                            print("Building of {0} failed".format(
                                self.package))
        else:
            try:
                self.makepkg()
                self.del_old_pkg()
                self.mvpkg()
                self.aur_push()
            except RuntimeWarning:
                if self.output:
                    print("Building of {0} failed".format(self.package))
