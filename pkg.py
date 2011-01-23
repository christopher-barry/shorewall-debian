#!/usr/bin/python -u
# vim: set fileencoding=utf-8:
#
# Shorewall Debian package build script
#
###############################################################################
#
# This program is under GPLv2, or later
# [http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt]
#
# (c) 2009,2011 - Roberto C. Sanchez <roberto@connexer.com>
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

import sys, os, re, getopt
# For manipulating the Git repo programmatically with git-buildpackage
import gbp.git_utils, gbp.deb_utils
# For accessing the Debian BTS and programmatically manipulating the bugs
import debianbts

def usage():
    print '''
pkg.py - Build the Debian packages of Shorewall

Usage summary: pkg.py [import|build|tag|upload] [options]

    common options:

    -h
        Print this help message and exit

    -l
        List available packages and exit

    -v
        Print verbose output

    -d
        Dry run: do not make any changes or commits to the repository

    import: import a new upstream tarball into the repository

    import options:

    -n <tarball>
        New upstream tarball to import (cannot be specified with -a, -b, -o,
        or -p)

    build: build one or more packages

    build options:

    -a
        Build or tag all the source packages (used in place of -p with
        multiple packages; overrides -p)

    -b <program>
        The program to use to build the packages (default: pdebuild)

    -o "<options>"
        Options to pass to the build program (must be enclosed in quotes if
        there are spaces)
        Example: -o "--debbuildopts --sa" to force inclusion of .orig.tar.gz

    -p "<package(s)>"
        The package(s) to build or tag (must be space separated and enclosed
        in quotes)

    tag: tag one or more packages

    tag options:

    -a
        Build or tag all the source packages (used in place of -p with
        multiple packages; overrides -p)

    -p "<package(s)>"
        The package(s) to build or tag (must be space separated and enclosed
        in quotes)
'''


def pkg_list(packages):
    print "Packages available for building or tagging:"
    for p in packages: print "    %s" % p

def illegal_option(o, op):
    print "Option %s is not allowed with operation %s!" % (o, op)
    sys.exit(1)

try:
    # Get the options from the command line
    opts, args = getopt.gnu_getopt(sys.argv[1:], 'adb:hln:o:p:tv')
except getopt.GetoptError, err:
    print str(err)
    usage()
    sys.exit(1)

# Set some defaults for the global variables used in the script
ops = ['import', 'build', 'tag', 'upload']
op = ''
packages = ['shorewall', 'shorewall6', 'shorewall-lite', 'shorewall6-lite', 'shorewall-init', 'shorewall-doc']
packages_to_process = []
build_prog = '/usr/bin/pdebuild'
build_prog_opts = ''
import_tarball = ''
dry_run = False
verbose = False
# Need to check for verbosity first, since it could be specified at the end
if ('-v', '') in opts: verbose = True

# Check to make sure only one positional argument is specified
if len(args) > 1:
    print "Only one operation is allowed!"
    print "Please use one of:",
    for o in ops: print o,
    sys.exit(1)

# Check to make sure no unrecognized positional argument is specified
for a in args:
    if not a in ops:
        print "Unrecognized operation (%s) specified!" % a
        print "Please use one of:",
        for o in ops: print o,
        sys.exit(1)
    op = a

# Process the options and set the needed variables for use within the script
for o, v in opts:
    if o == '-v':
        verbose = True
    elif o == '-h':
        usage()
        sys.exit()
    elif o == '-l':
        pkg_list(packages)
        sys.exit()
    elif o == '-d':
        dry_run = True
        print "Program executing in DRY RUN mode.  No commits or changes."
    elif o == '-a':
        if (op != 'build') and (op != 'tag'): illegal_option(o, op)
        packages_to_process = packages
        if verbose: print "Building packages: %s" % packages_to_process
    elif o == '-b':
        if op != 'build': illegal_option(o, op)
        build_prog = v
        if verbose: print "Using %s to build packages" % build_prog
    elif o == '-n':
        if op != 'import': illegal_option(o, op)
        import_tarball = v
        print "Importing new upstream tarball: %s" % import_tarball
    elif o == '-o':
        if op != 'build': illegal_option(o, op)
        build_prog_opts = v
        if verbose: print "Extra build program options: %s" % build_prog_opts
    elif o == '-p':
        if (op != 'build') and (op != 'tag'): illegal_option(o, op)
        if len(packages_to_process) == 0:
            packages_to_process = v.split(' ')
            for p in packages_to_process:
                if not p in packages:
                    print "%s is not a recognized package!" % p
                    pkg_list(packages)
                    sys.exit(1)
            if verbose: print "Processing packages: %s" % packages_to_process
    else:
        print "Unknown argument (%s)!" % o
        sys.exit(1)

# Check to make sure an operation was specified
if len(op) == 0:
    print "An operation must be specified!"
    print "Please use one of:",
    for o in ops: print o,
    sys.exit(1)

# Instantiate a git-buildpackage repository object
gbp_repo = gbp.git_utils.GitRepository(os.getcwd())

# Set up our branch and tag nomenclature
upstream_branch = 'upstream'
debian_branch = 'master'
upstream_tag = 'upstream'
debian_tag = 'debian'

# Now do the actual work
if op == 'import':
    # Make sure the user specified the location of the tarball
    if len(import_tarball) == 0:
        print "Please specify the -n option for the import operation!"
        sys.exit(1)

    # Make sure we have read access to the file
    if not os.access(import_tarball, os.R_OK):
        print "Unable to access file: %s!" % import_tarball
        sys.exit(1)

    # Check to make sure that the file is properly named
    name_parts = import_tarball.split('/')
    if verbose: print "Base file name: %s" % name_parts[-1]
    if not re.compile('\.orig\.tar\.gz$').search(name_parts[-1], 1):
        print "There is a problem with: %s" % name_parts[-1]
        print "It does not have the correct extension (.orig.tar.gz)!"
        sys.exit(1)

    # Extract the name of the package and its version
    pkg_name, suffix = name_parts[-1].split('_')
    pkg_ver = suffix.split('.orig')[0]
    if verbose: print "Package: %s, Version: %s" % (pkg_name, pkg_ver)

    # Make sure we can process this package in this repo
    if not pkg_name in packages:
        print "Package %s cannot be processed in this repository!" % pkg_name
        pkg_list(packages)
        sys.exit(1)

    # Check if it actually is a new upstream version
    this_branch = pkg_name + '/' + upstream_branch
    latest_tag = gbp_repo.find_tag(this_branch)
    latest_ver = latest_tag.split('/')[2]
    if verbose: print "Searching branch: %s" % this_branch
    if verbose: print "Found tag: %s" % latest_tag
    if pkg_ver <= latest_ver:
        print "Unable to import %s!" % name_parts[-1]
        print "Version %s is less than or equal to %s." % (pkg_ver, latest_ver)
        sys.exit(1)

    # There does not appear to be a programmatic interface to git-import-orig,
    # so this hacky call to os.system() will have to do
    import_cmd = 'git-import-orig --sign-tags'
    import_cmd += ' --upstream-branch=' + pkg_name + '/' + upstream_branch
    import_cmd += ' --debian-branch=' + pkg_name + '/' + debian_branch
    if verbose: import_cmd += ' --verbose'
    import_cmd += ' --pristine-tar'
    import_cmd += ' --upstream-tag=' + pkg_name + '/' + upstream_tag
    import_cmd += '/' + pkg_ver + ' --upstream-version=' + pkg_ver
    import_cmd += ' ' + import_tarball
    if verbose: print "Importing with this command:\n%s" % import_cmd
    if dry_run:
        print "DRY RUN: command not executed"
    else:
        if os.system(import_cmd) == 0:
            if verbose: print "Command executed successfully!"
        else:
            print "Command execution failed! Bailing out ..."
            sys.exit(1)

    # Pull bug reports, and remind user to check for closures
    bugs_fixed_upstream = debianbts.get_bugs('package', pkg_name, 'tag', 'fixed-upstream')
    bugs_upstream = debianbts.get_bugs('package', pkg_name, 'tag', 'upstream')
    bugs_all = debianbts.get_bugs('package', pkg_name)
    print "\n" + "**********" * 8
    if len(bugs_fixed_upstream) > 0: print "\nBugs tagged 'fixed-upstream':"
    for b in bugs_fixed_upstream:
        if b in bugs_all: bugs_all.remove(b) # avoid repeats below
        s = debianbts.get_status(b)
        print "\tBug %s (status: %s): %s" % (s[0].nr, s[0].status, s[0].summary)
    if len(bugs_upstream) > 0: print "\nBugs tagged 'upstream':"
    for b in bugs_upstream:
        if b in bugs_all: bugs_all.remove(b) # avoid repeats below
        s = debianbts.get_status(b)
        print "\tBug %s (status: %s): %s" % (s[0].nr, s[0].status, s[0].summary)
    if len(bugs_all) > 0: print "\nAll other bugs:"
    for b in bugs_all:
        s = debianbts.get_status(b)
        print "\tBug %s (status: %s): %s" % (s[0].nr, s[0].status, s[0].summary)
    print "\nPlease remember to check for and make note of closed bugs\n"
    print "**********" * 8 + "\n"
    os.system('git-status')

elif op == 'build':
    # Make sure that the user specified one or more packages to build
    if len(packages_to_process) == 0:
        print "Please specify packages to build!"
        sys.exit(1)
    for p in packages_to_process:
        p_debian_branch = p + '/' + debian_branch
        p_upstream_branch = p + '/' + upstream_branch
        if verbose: print "Checking out to branch: %s" % p_debian_branch
        gbp_repo.set_branch(p_debian_branch)
        # There does not appear to be a programmatic interface to
        # git-buildpackage for actually building packages, so this hacky call
        # to os.system() will have to do
        build_cmd = 'git-buildpackage --git-debian-branch=' + p_debian_branch
        build_cmd += ' --git-upstream-branch=' + p_upstream_branch
        build_cmd += ' --git-builder="' + build_prog + '"'
        if verbose: build_cmd += ' --git-verbose'
        build_cmd += ' --git-export-dir=../build-area --git-pristine-tar '
        build_cmd += build_prog_opts
        if verbose: print "Building with this command:\n%s" % build_cmd
        if dry_run:
            print "DRY RUN: command not executed"
        else:
            if os.system(build_cmd) == 0:
                if verbose: print "Command executed successfully!"
            else:
                print "Command execution failed! Bailing out ..."
                sys.exit(1)
    if verbose: print "Checking out to branch: master"
    gbp_repo.set_branch('master')

elif op == 'tag':
    # Make sure that the user specified one or more packages to tag
    if len(packages_to_process) == 0:
        print "Please specify packages to tag!"
        sys.exit(1)
    for p in packages_to_process:
        p_debian_branch = p + '/' + debian_branch
        p_upstream_branch = p + '/' + upstream_branch
        if verbose: print "Checking out to branch: %s" % p_debian_branch
        gbp_repo.set_branch(p_debian_branch)
        tag_ver = gbp.deb_utils.parse_changelog('debian/changelog')['Version']
        p_debian_tag = p + '/' + debian_tag + '/' + tag_ver
        # There does not appear to be a programmatic interface to
        # git-buildpackage for actually building packages, so this hacky call
        # to os.system() will have to do
        tag_cmd = 'git-buildpackage --git-debian-branch=' + p_debian_branch
        tag_cmd += ' --git-upstream-branch=' + p_upstream_branch
        tag_cmd += ' --git-tag --git-tag-only --git-sign-tags'
        tag_cmd += ' --git-debian-tag=' + p_debian_tag
        if verbose: tag_cmd += ' --git-verbose'
        if verbose: print "Tagging with this command:\n%s" % tag_cmd
        if dry_run:
            print "DRY RUN: command not executed"
        else:
            if os.system(tag_cmd) == 0:
                if verbose: print "Command executed successfully!"
            else:
                print "Command execution failed! Bailing out ..."
                sys.exit(1)
    if verbose: print "Checking out to branch: master"
    gbp_repo.set_branch('master')

elif op == 'upload':
    print "Pushing to SourceForge repository"
    push_cmd = 'git-push --mirror ssh://el_cubano@shorewall.git.sourceforge.net/gitroot/shorewall/debian'
    if verbose: print "Pushing with this command:\n%s" % push_cmd
    if dry_run:
        print "DRY RUN: command not executed"
    else:
        if os.system(push_cmd) == 0:
            if verbose: print "Command executed successfully!"
        else:
            print "Command execution failed! Bailing out ..."
            sys.exit(1)

else:
    print "No known operation was specified!"
    sys.exit(1)

# vim:et:ts=4:sw=4:et:sts=4:ai:set list listchars=tab\:»·,trail\:·:
