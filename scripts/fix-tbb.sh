#!/bin/zsh

for i in `ls packages`;
do
	if grep 'intel-tbb' packages/$i/PKGBUILD; then
		echo "$i depends on intel-tbb"
		cd packages/$i
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
