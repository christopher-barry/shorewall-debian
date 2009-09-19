#!/bin/bash
#
# Shorewall Debian package build script
#
###############################################################################
#
# This program is under GPLv2, or later
# [http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt]
#
# (c) 2009 - Roberto C. Sanchez <roberto@connexer.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
###############################################################################


###############################################################################
# Subroutines
###############################################################################

print_help() {
  echo -e ""
  echo -e "build.sh - Build the Debian packages of Shorewall"
  echo -e ""
  echo -e "Usage summary: ./build.sh [options]"
  echo -e ""
  echo -e "    -a"
  echo -e "        Build all the source packages"
  echo -e ""
  echo -e "    -b <program>"
  echo -e "        The program to use to build the packages, with full path specified (default: pdebuild)"
  echo -e ""
  echo -e "    -h"
  echo -e "        Print this help message and exit"
  echo -e ""
  echo -e "    -l"
  echo -e "        List available packages and exit"
  echo -e ""
  echo -e "    -o \"<options>\""
  echo -e "        options to pass to the build program (must be enclosed in quotes)"
  echo -e ""
  echo -e "    -p \"<package(s)>\""
  echo -e "        The package(s) to build (must be space separated and enclosed in quotes)"
  echo -e ""
  echo -e "    -v"
  echo -e "        Print verbose output"
  echo -e ""
}

list_packages() {
  git-branch |cut -f3 -d' ' |grep shorewall |cut -f1 -d'/' |sort -u
}

fatal_error() {
  echo "   ERROR: $@" >&2
  exit 1
}

###############################################################################
# Main script
###############################################################################

# Parse options

while getopts "ab:hlo:p:v" opt; do
  case $opt in
    a)
      PKGS_TO_BUILD="shorewall shorewall-lite shorewall6 shorewall6-lite shorewall-doc"
      ;;
    b)
      BUILD_PROG="$OPTARG"
      ;;
    h)
      print_help
      exit
      ;;
    l)
      list_packages
      exit
      ;;
    o)
      BUILD_PROG_OPTS="$OPTARG"
      ;;
    p)
      [ -z "$PKGS_TO_BUILD" ] && PKGS_TO_BUILD="$OPTARG"
      ;;
    v)
      VERBOSE="yes"
      ;;
    \?)
      fatal_error "Unrecognized option -$OPTARG"
      ;;
    :)
      fatal_error "Option -$OPTARG requires an argument."
      ;;
  esac
done

[ -d ../build-area ] || fatal_error "Please create the directory ../build-area for exporting from the repository"
[ -z "$PKGS_TO_BUILD" ] && fatal_error "Please specify one or more packages to build"

# Check for required programs

[ -z "$BUILD_PROG" ] && BUILD_PROG="/usr/bin/pdebuild" && BUILD_PROG_OPTS="--use-pdebuild-internal $BUILD_PROG_OPTS"

[ -z "$VERBOSE" ] || echo "Checking for required programs ..."
for i in /usr/bin/git-buildpackage /usr/bin/pristine-tar "$BUILD_PROG" ; do
  [ -z "$VERBOSE" ] || echo "   Checking for $i"
  [ -x $i ] || fatal_error "Required program $i not found"
done

[ -z "$VERBOSE" ] || echo "Preparing to build packages: $PKGS_TO_BUILD"

for i in $PKGS_TO_BUILD ; do
  [ -z "$VERBOSE" ] || echo "Building package $i"
  BUILD_CMD="git-buildpackage --git-upstream-branch=$i/upstream --git-debian-branch=$i/master --git-export-dir=../build-area --git-builder=$BUILD_PROG $BUILD_PROG_OPTS"
  [ -z "$VERBOSE" ] || echo "Issuing command:"
  [ -z "$VERBOSE" ] || echo "   $BUILD_CMD"
  git-checkout $i/master
  $BUILD_CMD
done

[ -z "$VERBOSE" ] || echo "Checking out back to master branch"

git-checkout master

[ -z "$VERBOSE" ] || echo "Package build complete."

###############################################################################
# Command lines
###############################################################################

# Build
# git-buildpackage --git-upstream-branch=shorewall/upstream --git-debian-branch=shorewall/master --git-builder="~/bin/my-pdebuild.sh" --git-export-dir=../build-area
# pdebuild --configfile /etc/pbuilder/pbuilderrc-$DISTRO --buildsourceroot fakeroot --pbuilderroot sudo --buildresult /var/lib/chroot/pbuilder-$DISTRO/results --use-pdebuild-internal "$@"

# Tag
# git-buildpackage --git-upstream-branch=shorewall/upstream --git-debian-branch=shorewall/master --git-tag --git-tag-only --git-debian-tag=shorewall/debian/4.4.1.2-2

