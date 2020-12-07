#!/bin/zsh

CACHE_PATH=${XDG_CACHE_HOME:-"$HOME/.cache"}
PACKAGES_PATH=$CACHE_PATH/ros-aur-helper/packages

for i in $(ls $PACKAGES_PATH);
do
	if pikaur -Si $i | egrep -q 'cpp|boost'; then
		echo "$i contains c++ code"
		if ! grep "('any')" $PACKAGES_PATH/$i/PKGBUILD; then
			echo "$i already has a correct arch=() array"
			continue;
		fi
		cd $PACKAGES_PATH/$i
		sed -i "s/arch=('any')/arch=('i686' 'x86_64' 'aarch64' 'armv7h' 'armv6h')/g" PKGBUILD
		grep "pkgrel" PKGBUILD | IFS="=" read -r name value
		(( pkgrel = $value + 1 ))
		sed -i "s/pkgrel=$value/pkgrel=$pkgrel/g" PKGBUILD
		makepkg --printsrcinfo > .SRCINFO
		git add PKGBUILD .SRCINFO
		git commit -m "Fixed arch=() array"
		git push origin master
		cd -;
	else
		echo "$i does NOT contain c++ code";
	fi
done
