#!/bin/zsh

for i in `ls packages`;
do
	if grep 'eigen3' packages/$i/PKGBUILD; then
		echo "$i depends on eigen3"
		cd packages/$i
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
