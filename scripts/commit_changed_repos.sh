#!/bin/bash

CACHE_PATH=${XDG_CACHE_HOME:-"$HOME/.cache"}
PACKAGES_PATH=$CACHE_PATH/ros-aur-helper/packages

for dir in $(ls $PACKAGES_PATH);
do
    cd $PACKAGES_PATH/$dir
    if git status | grep -q '.SRCINFO'; then
        git add .SRCINFO PKGBUILD
        git commit -m "Updated package"
        git push origin master;
    fi
    cd -;
done
