#!/bin/zsh

for i in `ls packages`;
do
	if pacman -Si $i | egrep -q 'cpp|boost'; then
		echo "$i contains c++ code"
		cd packages/$i
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