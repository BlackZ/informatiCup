#!/bin/bash

# version of your package
VERSION_isyenv=

# dependencies of this recipe
DEPS_isyenv=(kivy requests futures)

# url of the package
URL_isyenv=

# md5 of the package
MD5_isyenv=

# default build path
BUILD_isyenv=$BUILD_PATH/isyenv/isyenv

# default recipe path
RECIPE_isyenv=$RECIPES_PATH/isyenv

# function called for preparing source code if needed
# (you can apply patch etc here.)
function prebuild_isyenv() {
	true
}

# function called to build the source code
function build_isyenv() {
	$HOSTPYTHON setup.py install
}

# function called after all the compile have been done
function postbuild_isyenv() {
	true
}
