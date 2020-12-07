from aurci import sed
from github import Github
from pathlib import Path
import os
import requests
import shutil
import yaml
import re
import configparser


class Routines:
    CONFIG_ROOT = os.environ.get(
        "XDG_CONFIG_HOME", os.path.join(Path.home(), ".config/"))
    CACHE_ROOT = os.environ.get(
        "XDG_CACHE_HOME", os.path.join(Path.home(), ".cache/"))

    def __init__(self, package=None, verbosity=False, output=True):
        self.verbosity = verbosity
        self.output = output
        self.config_path = os.path.join(Routines.CONFIG_ROOT, 'ros-aur-helper')
        self.cache_path = os.path.join(Routines.CACHE_ROOT, 'ros-aur-helper')
        self.check_and_create_path(self.config_path)
        self.check_and_create_path(self.cache_path)
        if package:
            self.package = package
            self.repos_path = os.path.join(
                self.cache_path, "packages", self.package)
        config = self.get_config()
        self.gh = Github(config['CI']['GH_OAUTH_TOKEN'])
        self.gh_organization_name = config['CI']['GH_ORGANIZATION']
        self.gh_organization = self.gh.get_organization(
            self.gh_organization_name)

    @staticmethod
    def check_and_create_path(path):
        if not (os.path.exists(path)):
            Path.mkdir(path)

    def get_config(self):
        configfile_path = os.path.join(self.config_path, 'config.ini')
        if not os.path.exists(configfile_path):
            shutil.copy('config_example.ini', configfile_path)
        config = configparser.ConfigParser()
        config.read(configfile_path)
        return config

    def delete_package_line(self, file):
        if os.path.isfile(file):
            sed.rmlinematch(self.package, file)

    def build_metainfo_dict(self):
        rosdistro_url = \
            f'https://raw.githubusercontent.com/ros/rosdistro/master/{self.get_ros_distro()}/distribution.yaml'
        rosdistro = yaml.load(requests.get(rosdistro_url, allow_redirects=True).content,
                              Loader=yaml.BaseLoader)['repositories']
        ros_dict = {}
        for repo in rosdistro:
            # Go through distro, and make entry for each package in a repository
            d = rosdistro[repo]
            if 'source' in d:
                src = d['source']['url']
            elif 'release' in d:
                src = d['release']['url']
            target = re.sub(r'\.git', '', src.split(
                '/')[3] + '/' + src.split('/')[4])
            pkgver = d.get('release', {'version': None}).get('version', None)
            if pkgver:
                pkgver = pkgver.split('-')[0]
            if 'github' in src:
                dl = 'https://github.com/' + target + '/archive/' + pkgver + '.tar.gz' \
                    if pkgver else None
                url = 'https://github.com/' + \
                    target + '/archive/${pkgver}.tar.gz'
            else:
                dl = None
            pkg_list = d.get('release', {'packages': [repo]}).get(
                'packages', [repo])
            for pkg in pkg_list:
                siblings = len(pkg_list)-1
                pkgname = 'ros-melodic-{}'.format(re.sub('_', '-', pkg))
                ros_dict[pkgname] = {'repo': repo, 'siblings': siblings, 'orig_name': pkg,
                                     'pkgname': pkgname, 'src': src, 'pkgver': pkgver, 'dl': dl, 'url': url}
        return ros_dict

    def get_ros_distro(self):
        config = self.get_config()
        return config['CI']['GH_ORGANIZATION'].split('-')[1]

    @staticmethod
    def query_yes_no(question, default="yes"):
        """
        Ask a yes/no question via input() and return their answer.
        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).
        The "answer" return value is one of "yes" or "no".
        """
        valid = {"yes": "yes", "y": "yes", "ye": "yes",
                 "no": "no", "n": "no"}
        if not default:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)
        while True:
            print(question + prompt)
            choice = input().lower()
            if default is not None and choice == '':
                return default
            elif choice in valid.keys():
                return valid[choice]
            else:
                print("Please respond with 'yes' or 'no' (or 'y' or 'n').")
