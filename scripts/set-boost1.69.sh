#!/bin/zsh

CACHE_PATH=${XDG_CACHE_HOME:-"$HOME/.cache"}
PACKAGES_PATH=$CACHE_PATH/ros-aur-helper/packages

for i in $(ls $PACKAGES_PATH);
do
	if grep -q 'boost' $PACKAGES_PATH/$i/PKGBUILD && ! grep -q 'boost1.69' $PACKAGES_PATH/$i/PKGBUILD; then
		echo "$i links against wrong boost"
		cd $PACKAGES_PATH/$i
		sed -i "s/boost/boost1.69/g" PKGBUILD
		sed -i 's!-DSETUPTOOLS_DEB_LAYOUT=OFF!-DSETUPTOOLS_DEB_LAYOUT=OFF \\\n\t\t -DBOOST_ROOT=/opt/boost1.69!g' PKGBUILD
		grep "pkgrel" PKGBUILD | IFS="=" read -r name value
		(( pkgrel = $value + 1 ))
		sed -i "s/pkgrel=$value/pkgrel=$pkgrel/g" PKGBUILD
		makepkg --printsrcinfo > .SRCINFO
		git add PKGBUILD .SRCINFO
		git commit -m "Hardcode Boost Version to 1.69"
		git push origin master
		cd -;
	else
		echo "$i doesn't link against boost or already against version 1.69";
	fi
done
