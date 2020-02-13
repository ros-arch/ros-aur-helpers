#/bin/bash

for i in `ls packages`; do
	sed -i '/-DPYTHON_BASENAME/d' packages/$i/PKGBUILD
	sed -i '/-DPYTHON_LIBRARY/d' packages/$i/PKGBUILD
