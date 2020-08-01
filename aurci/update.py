from aurci.general import Routines
import os
import sys
import re
import subprocess
import tarfile
import urllib


class Update(Routines):

    # packages that are missing information or are special cases
    skip = ['fcl', 'libviso2', 'viso2_ros', 'opencv3', 'roscpp_git', 'message_filters_git',
        'ivcon', 'stage', 'nodelet_tutorial_math', 'common_tutorials',
        'turtle_actionlib', 'pluginlib_tutorials', 'rosbag_migration_rule',
        'actionlib_tutorials', 'ompl', 'bfl', 'convex_decomposition', 'mavlink']

    def __init__(self, package, verbosity, ouput):
        Routines.__init__(self, package, verbosity, ouput)
        self.metainfo_dict = self.build_metainfo_dict()
        if not package == None:
            self.package_info = self.metainfo_dict[self.package]

    def update_pkgbuild(self):
        os.chdir(os.path.join("./packages", self.package))
        if not self.package_info.get('pkgver', None):
            print('pkgver not in dict: {}'.format(self.package))
            return (self.package, 'no_tag')

        old_pkgver = re.findall(r"^pkgver=.*", open('PKGBUILD').read(), re.MULTILINE)
        old_pkgrel = re.findall(r"^pkgrel=\d", open('PKGBUILD').read(), re.MULTILINE)
        old_dir = re.findall(r"^_dir=.*", open('PKGBUILD').read(), re.MULTILINE)
        old_src = re.findall(r"^source=\(.*\"", open('PKGBUILD').read(), re.MULTILINE)
        old_sha = re.findall(r"^sha256sums=\(.*\'", open('PKGBUILD').read(), re.MULTILINE)

        if all((old_dir, old_src, old_sha, old_pkgver, old_pkgrel)):
            old_pkgver = old_pkgver[0]
            old_pkgrel = old_pkgrel[0]
            old_dir = old_dir[0]
            old_src = old_src[0]
            old_sha = old_sha[0]
        else:
            raise RuntimeError('getting PKGBUILD lines failed: {}'.format(self.package) + "\n \
                                Maybe diffrent quotes than needed for regex?")

        new_pkgver = "pkgver='{}'".format(self.package_info['pkgver'])
        new_src = 'source=("${{pkgname}}-${{pkgver}}.tar.gz"::"{}"'.format(self.package_info['url'])

        if old_pkgver == new_pkgver and old_dir == new_dir and old_src == new_src:
            print('already matches: {}'.format(self.package))
            sys.exit(0)

        print('starting: {}'.format(self.package))
        fname = '{}-{}.tar.gz'.format(self.package, self.package_info['pkgver'])
        #Trying to download tar archive to generate checksum
        try:
            urllib.request.urlretrieve(self.package_info['dl'], fname)
        except urllib.error.HTTPError:
            raise RuntimeError('download failed: {}'.format(self.package))

        sha256 = subprocess.run(['sha256sum', fname], check=True, capture_output=True)
        new_sha = "sha256sums=('{}'".format(sha256.stdout.decode('utf-8').split(' ')[0])

        # TODO:
        #   - Error checking
        #   - Probably use with ...: notation
        #   - Check, whether main_dir is only one string (should be)
        archive = tarfile.open(fname, "r:gz")
        main_dir = os.path.commonprefix(archive.getnames())
        new_dir = '_dir="{}"'.format(main_dir)
        archive.close()

        os.remove(fname)

        with open('PKGBUILD', 'r') as f:
            lines = f.readlines()

        with open('PKGBUILD', 'w') as f:
            for line in lines:
                line = re.sub(re.escape(old_pkgver), new_pkgver, line)
                line = re.sub(re.escape(old_pkgrel), 'pkgrel=1', line)
                line = re.sub(re.escape(old_src), new_src, line)
                line = re.sub(re.escape(old_dir), new_dir, line)
                line = re.sub(re.escape(old_sha), new_sha, line)
                f.write(line)

        with open('.SRCINFO', "w") as outfile:
            subprocess.call(['makepkg', '--printsrcinfo'], stdout=outfile)

        subprocess.call(['git', 'diff', 'PKGBUILD'])
        if self.query_yes_no("Commit and push changes") == 'yes':
            subprocess.call(['git', 'add', 'PKGBUILD', '.SRCINFO'])
            subprocess.call(['git', 'commit', '-m', 'Update package'])
            subprocess.call(['git', 'push', 'origin', 'master'])


    def print_metainfo_dict(self):
        #rosdistro = yaml.load(requests.get(self.rosdistro_url, allow_redirects=True).content,
        #             Loader=yaml.BaseLoader)['repositories']
        #for repo in rosdistro:
        #    print (rosdistro[repo])
        for pkg in self.metainfo_dict:
            print("\n" + pkg + ":\n")
            print(self.metainfo_dict[pkg], end="\n")

    def get_nested_package_path(self):
        """Give back the first path containing the package name."""
        repo_name = self.package_info['src'].lstrip('https://github.com/')[:-4]
        repo = self.gh.get_repo(repo_name)
        contents = repo.get_contents(".")
        for content in contents:
            if self.package_info['orig_name'] in content.path and content.type == 'dir':
                return content.path
            if content.type == 'dir':
                contents.extend(repo.get_contents(content.path))
        raise RuntimeError("Can't find nested path: " + self.package)


def main():
    Update(None, None, None).print_metainfo_dict()


if __name__ == "__main__":
    main()
