import sys
import argparse
import bootstrap


def commands(option, package):
    args = {
        "clone"  : bootstrap.clone
    }
    args[option](package)


def main(argv):
    parser=argparse.ArgumentParser(prog='dockerctl', add_help=True)
    
    parser.add_argument('command', choices=['clone', 'build'])

    args = parser.parse_args(argv)
    commands(args.command, args.package)


if __name__=='__main__':
    main(sys.argv)