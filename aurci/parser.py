import sys
import argparse
from aurci.bootstrap import Clone, Pull
from aurci.build import Packages
from aurci.update import Update


def commands(option, package, verbosity, output):
    args = {
        "clone"  : Clone(package, verbosity, output).clone,
        "pull"   : Pull(package, verbosity, output).pull,
        "build"  : Packages(package, verbosity, output).build,
        "deploy" : Packages(package, verbosity, output).deploy,
        "update" : Update(package, verbosity, output).update_pkgbuild
    }
    args[option]()


def main(argv):
    parser=argparse.ArgumentParser(prog='aurci', add_help=True)
    exclu_group = parser.add_mutually_exclusive_group()
    
    parser.add_argument('command', choices=['clone', 'pull', 'build', 'deploy', 'update'])
    parser.add_argument('package', type=str)
    exclu_group.add_argument('-v', '--verbose', help='Increase verbosity', action="store_true")
    exclu_group.add_argument('-q', '--quiet', help='Suppress output', action="store_false")

    args = parser.parse_args(argv)
    commands(args.command, args.package, args.verbose, args.quiet)


if __name__=='__main__':
    main(sys.argv)