ros-aur-helpers
==

A helper tool and a collection of various scripts making building, updating and collaborating of/on Arch Linux ROS packages easier.

Installation
=
Prequisites: Python>=3.8, git, devtools  
[Set up ABS build chroot](https://wiki.archlinux.org/index.php/DeveloperWiki:Building_in_a_clean_chroot#Handling_major_rebuilds)  
Set a folder where the built packages should get into.(Config in /etc/makepkg.conf)  
Add this folder as repo. (Config in $CHROOT/root/etc/pacman.conf)  

Usage
=
```
usage: rosaur [-h] [-v | -q] {clone,pull,build,deploy,update} package

positional arguments:
  clone		Clone a package to packages/package_name
  pull		Pull the latest version of a package
  build		Build a package in a clean chroot
  deploy	Build package and push to AUR if build was successfull
  update	Update a Package to the latest available version on ROSIndex, optional commit and push
  package 	Package name (Use 'all' if you want all)

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase verbosity
  -q, --quiet           Suppress output
```

`scripts/` contains various helper scripts needed once, names should be self-explaining
