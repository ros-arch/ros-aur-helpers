#!/bin/bash

for dir in $(ls packages);
do
    cd packages/$dir
    if git status | grep -q '.SRCINFO'; then
        git add .SRCINFO PKGBUILD
        git commit -m "Updated package"
        git push origin master;
    fi
    cd -;
done
