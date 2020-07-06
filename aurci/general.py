from PythonSed import Sed, SedException
from github import Github
import os
import requests
import yaml
import re
import configparser

class Routines:

    def __init__(self, package=None, verbosity=False, output=True):
        self.package = package
        self.verbosity = verbosity
        self.output = output
        self.path = os.path.join("./packages/{0}".format(self.package))
        config = configparser.ConfigParser()
        config.read('config.ini')
        g = Github(config['CI']['GH_OAUTH_TOKEN'])
        self.gh_organization_name = config['CI']['GH_ORGANIZATION']
        self.gh_organization = g.get_organization(self.gh_organization_name)

    def delete_package_line(self, file):
        sed = Sed()
        try:
            sed.no_autoprint = True
            sed.regexp_extended = False
            sed.load_string("/{0}/d".format(self.package))
            sed.apply(file, "test.txt")
        except SedException as e:
            print(e.message)

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
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config['CI']['GH_ORGANIZATION'].rstrip("arch")