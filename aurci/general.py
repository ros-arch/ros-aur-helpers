from aurci import sed
from github import Github
import os
import requests
import shutil
import yaml
import re
import configparser

class Routines:

    def __init__(self, package=None, verbosity=False, output=True):
        self.package = package
        self.verbosity = verbosity
        self.output = output
        self.path = os.path.join("./packages/{0}".format(self.package))
        config = self.get_config()
        self.gh = Github(config['CI']['GH_OAUTH_TOKEN'])
        self.gh_organization_name = config['CI']['GH_ORGANIZATION']
        self.gh_organization = self.gh.get_organization(self.gh_organization_name)

    @staticmethod
    def get_config():
        config = configparser.ConfigParser()
        if not os.path.exists('config.ini'):
            shutil.copy('config_distribute.ini', 'config.ini')
        config.read('config.ini')
        return config

    def delete_package_line(self, file):
        sed.rmlinematch(self.package, file)

    @staticmethod
    def build_metainfo_dict():
        rosdistro_url = \
        'https://raw.githubusercontent.com/ros/rosdistro/master/melodic/distribution.yaml'
        rosdistro = yaml.load(requests.get(rosdistro_url, allow_redirects=True).content,
                              Loader=yaml.BaseLoader)['repositories']
        ros_dict = {}
        for repo in rosdistro:
        #Go through distro, and make entry for each package in a repository
            d = rosdistro[repo]
            if 'source' in d:
                src = d['source']['url']
            elif 'release' in d:
                src = d['release']['url']
            target = re.sub(r'\.git', '', src.split('/')[3] + '/' + src.split('/')[4])
            pkgver = d.get('release', {'version': None}).get('version', None)
            if pkgver:
                pkgver = pkgver.split('-')[0]
            if 'github' in src:
                dl = 'https://github.com/' + target + '/archive/' + pkgver +'.tar.gz' \
                    if pkgver else None
                url = 'https://github.com/' + target + '/archive/${pkgver}.tar.gz'
            else:
                dl = None
            pkg_list = d.get('release', {'packages': [repo]}).get('packages', [repo])
            for pkg in pkg_list:
                siblings = len(pkg_list)-1
                pkgname = 'ros-melodic-{}'.format(re.sub('_', '-', pkg))
                ros_dict[pkgname] = {'repo': repo, 'siblings': siblings, 'orig_name': pkg,
                                     'pkgname': pkgname, 'src': src, 'pkgver': pkgver, 'dl': dl, 'url': url}
        return ros_dict

    @staticmethod
    def get_ros_distro():
        config = Routines.get_config()
        return config['CI']['GH_ORGANIZATION'].rstrip("arch")

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
