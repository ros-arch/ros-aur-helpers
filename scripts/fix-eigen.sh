#!/bin/zsh

CACHE_PATH=${XDG_CACHE_HOME:-"$HOME/.cache"}
PACKAGES_PATH=$CACHE_PATH/ros-aur-helper/packages

for i in $(ls $PACKAGES_PATH);
do
	if grep 'eigen3' $PACKAGES_PATH/$i/PKGBUILD; then
		echo "$i depends on eigen3"
		cd $PACKAGES_PATH/$i
		sed -i "s/eigen3/eigen/g" PKGBUILD
		grep "pkgrel" PKGBUILD | IFS="=" read -r name value
		(( pkgrel = $value + 1 ))
		sed -i "s/pkgrel=$value/pkgrel=$pkgrel/g" PKGBUILD
		makepkg --printsrcinfo > .SRCINFO
		git add PKGBUILD .SRCINFO
		git commit -m "Rename dep eigen3 to eigen"
		git push origin master
		cd -;
	else
		echo "$i doesn't depend on eigen3";
	fi
done
