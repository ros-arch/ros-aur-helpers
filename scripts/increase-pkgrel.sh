#!/bin/zsh

CACHE_PATH=${XDG_CACHE_HOME:-"$HOME/.cache"}
PACKAGES_PATH=$CACHE_PATH/ros-aur-helper/packages

git_commit_and_push() {
    # http://zsh.sourceforge.net/Doc/Release/Shell-Builtin-Commands.html#index-read
    if read -q "choice?Press Y/y to continue with commit and push "; then
        set -x
	makepkg --printsrcinfo > .SRCINFO
	git add PKGBUILD .SRCINFO
	git commit -m "Increase pkgrel"
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
	cd $PACKAGES_PATH/$i
	git pull origin master
	grep "pkgrel" PKGBUILD | IFS="=" read -r name value
	(( pkgrel = $value + 1 ))
	sed -i "s/pkgrel=$value/pkgrel=$pkgrel/g" PKGBUILD
	git diff PKGBUILD
	git_commit_and_push
	cd -;
done
