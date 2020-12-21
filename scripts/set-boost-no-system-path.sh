#!/bin/zsh

CACHE_PATH=${XDG_CACHE_HOME:-"$HOME/.cache"}
PACKAGES_PATH=$CACHE_PATH/ros-aur-helper/packages

git_commit_and_push() {
    # http://zsh.sourceforge.net/Doc/Release/Shell-Builtin-Commands.html#index-read
    if read -q "choice?Press Y/y to continue with commit and push "; then
        set -x
	makepkg --printsrcinfo > .SRCINFO
	git add PKGBUILD .SRCINFO
	git commit -m "Set -DBoost_NO_SYSTEM_PATHS=TRUE as cmake flag"
	git push origin master
	{ set +x; } 2>/dev/null
    else
        echo
        echo "'$choice' not 'Y' or 'y'. Exiting..."
	git reset --hard
    fi
}

for i in $(ls $PACKAGES_PATH);
do
	if grep -q 'DBOOST_ROOT=/opt/boost1.69' $PACKAGES_PATH/$i/PKGBUILD && ! grep -q 'DBoost_NO_SYSTEM_PATHS' $PACKAGES_PATH/$i/PKGBUILD; then
		echo "$i BOOST_ROOT set but not DBoost_NO_SYSTEM_PATHS"
		cd $PACKAGES_PATH/$i
		git pull origin master
		sed -i 's!-DBOOST_ROOT=/opt/boost1.69!-DBOOST_ROOT=/opt/boost1.69 \\\n\t\t -DBoost_NO_SYSTEM_PATHS=TRUE!g' PKGBUILD
		grep "pkgrel" PKGBUILD | IFS="=" read -r name value
		(( pkgrel = $value + 1 ))
		sed -i "s/pkgrel=$value/pkgrel=$pkgrel/g" PKGBUILD
		git diff PKGBUILD
		git_commit_and_push
		cd -;
	else
		echo "$i doesn't have BOOST_ROOT set or already DBoost_NO_SYSTEM_PATHS appended";
	fi
done
