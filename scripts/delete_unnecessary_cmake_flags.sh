#!/bin/zsh

CACHE_PATH=${XDG_CACHE_HOME:-"$HOME/.cache"}
PACKAGES_PATH=$CACHE_PATH/ros-aur-helper/packages

for i in $(ls $PACKAGES_PATH);
do
    if grep 'DPYTHON_LIBRARY' $PACKAGES_PATH/$i/PKGBUILD; then
        echo "$i has unnecessary cmake args"
        cd $PACKAGES_PATH/$i
        sed -i '/-DPYTHON_BASENAME/d' PKGBUILD
        sed -i '/-DPYTHON_LIBRARY/d' PKGBUILD
        sed -i '/-DPYTHON_INCLUDE_DIR/d' PKGBUILD
        grep "pkgrel" PKGBUILD | IFS="=" read -r name value
        (( pkgrel = $value + 1 ))
        sed -i "s/pkgrel=$value/pkgrel=$pkgrel/g" PKGBUILD
        makepkg --printsrcinfo > .SRCINFO
        git add PKGBUILD .SRCINFO
        git commit -m "Delete unnecessary cmake args"
        git push origin master
        cd -;
    else
        echo "$i doesn't have unnecessary cmake args";
    fi
done
