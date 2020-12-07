#!/bin/zsh

CACHE_PATH=${XDG_CACHE_HOME:-"$HOME/.cache"}
PACKAGES_PATH=$CACHE_PATH/ros-aur-helper/\$PACKAGES_PATH

for i in $(ls $PACKAGES_PATH);
do
	if grep '/bin/python2' $PACKAGES_PATH/$i/PKGBUILD; then
		echo "$i links against python2"
		cd $PACKAGES_PATH/$i
		sed -i "s!/bin/python2!/bin/python3!g" PKGBUILD
		sed -i "s/-v 2/-v 3/g" PKGBUILD
		grep "pkgrel" PKGBUILD | IFS="=" read -r name value
		(( pkgrel = $value + 1 ))
		sed -i "s/pkgrel=$value/pkgrel=$pkgrel/g" PKGBUILD
		makepkg --printsrcinfo > .SRCINFO
		git add PKGBUILD .SRCINFO
		git commit -m "Set python version to 3"
		git push origin master
		cd -;
	else
		echo "$i doesn't link against python2";
	fi
done
