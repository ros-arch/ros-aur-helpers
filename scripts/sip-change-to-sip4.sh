#!/bin/zsh

CACHE_PATH=${XDG_CACHE_HOME:-"$HOME/.cache"}
PACKAGES_PATH=$CACHE_PATH/ros-aur-helper/packages

git_commit_and_push() {
    # http://zsh.sourceforge.net/Doc/Release/Shell-Builtin-Commands.html#index-read
    if read -q "choice?Press Y/y to continue with commit and push "; then
        set -x
	makepkg --printsrcinfo > .SRCINFO
	git add PKGBUILD .SRCINFO
	git commit -m "Change sip dep to sip4"
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
	if grep -qzP 'sip\n' $PACKAGES_PATH/$i/PKGBUILD; then
		echo "$i sip detected, changing to sip4"
		cd $PACKAGES_PATH/$i
		git stash && git stash clear
		git pull origin master
		sed -i 's/sip$/sip4/g' PKGBUILD
		grep "pkgrel" PKGBUILD | IFS="=" read -r name value
		(( pkgrel = $value + 1 ))
		sed -i "s/pkgrel=$value/pkgrel=$pkgrel/g" PKGBUILD
		git diff PKGBUILD
		git_commit_and_push
		cd -;
	else
		echo "$i doesn't have sip as dep or already depends on sip4";
	fi
done
