#!/bin/zsh

for i in `ls packages`;
do
    if grep 'DPYTHON_LIBRARY' packages/$i/PKGBUILD; then
        echo "$i has unnecessary cmake args"
        cd packages/$i
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
