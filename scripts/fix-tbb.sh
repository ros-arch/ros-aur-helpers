#!/bin/zsh

CACHE_PATH=${XDG_CACHE_HOME:-"$HOME/.cache"}
PACKAGES_PATH=$CACHE_PATH/ros-aur-helper/packages

for i in $(ls $PACKAGES_PATH);
do
	if grep 'intel-tbb' $PACKAGES_PATH/$i/PKGBUILD; then
		echo "$i depends on intel-tbb"
		cd $PACKAGES_PATH/$i
		sed -i "s/intel-tbb/tbb/g" PKGBUILD
		grep "pkgrel" PKGBUILD | IFS="=" read -r name value
		(( pkgrel = $value + 1 ))
		sed -i "s/pkgrel=$value/pkgrel=$pkgrel/g" PKGBUILD
		makepkg --printsrcinfo > .SRCINFO
		git add PKGBUILD .SRCINFO
		git commit -m "Rename dep intel-tbb to tbb"
		git push origin master
		cd -;
	else
		echo "$i doesn't depend on intel-tbb";
	fi
done
