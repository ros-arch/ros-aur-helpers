import sys
import argparse
from aurci import bootstrap, build


def commands(option, package):
    args = {
        "clone"  : bootstrap.clone,
        "build"  : build.build
    }
    args[option](package)


def main(argv):
    parser=argparse.ArgumentParser(prog='dockerctl', add_help=True)
    
    parser.add_argument('command', choices=['clone', 'build'])
    parser.add_argument('package', type=str)

    args = parser.parse_args(argv)
    commands(args.command, args.package)


if __name__=='__main__':
    main(sys.argv)