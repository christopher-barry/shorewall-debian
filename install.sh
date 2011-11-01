#!/bin/sh
#
# Script to install Shoreline6 Firewall
#
#     This program is under GPL [http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt]
#
#     (c) 2000-2011 - Tom Eastep (teastep@shorewall.net)
#
#       Shorewall documentation is available at http://shorewall.net
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of Version 2 of the GNU General Public License
#       as published by the Free Software Foundation.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

VERSION=4.4.25.1

usage() # $1 = exit status
{
    ME=$(basename $0)
    echo "usage: $ME"
    echo "       $ME -v"
    echo "       $ME -h"
    echo "       $ME -s"
    echo "       $ME -a"
    exit $1
}

split() {
    local ifs
    ifs=$IFS
    IFS=:
    set -- $1
    echo $*
    IFS=$ifs
}

qt()
{
    "$@" >/dev/null 2>&1
}

mywhich() {
    local dir

    for dir in $(split $PATH); do
	if [ -x $dir/$1 ]; then
	    echo $dir/$1
	    return 0
	fi
    done

    return 2
}

run_install()
{
    if ! install $*; then
	echo
	echo "ERROR: Failed to install $*" >&2
	exit 1
    fi
}

cant_autostart()
{
    echo
    echo  "WARNING: Unable to configure shorewall6 to start automatically at boot" >&2
}

delete_file() # $1 = file to delete
{
    rm -f $1
}

install_file() # $1 = source $2 = target $3 = mode
{
    run_install $OWNERSHIP -m $3 $1 ${2}
}

[ -n "$DESTDIR" ] || DESTDIR="$PREFIX"

#
# Parse the run line
#
# DEST is the SysVInit script directory
# INIT is the name of the script in the $DEST directory
# ARGS is "yes" if we've already parsed an argument
#
ARGS=""

if [ -z "$DEST" ] ; then
	DEST="/etc/init.d"
fi

if [ -z "$INIT" ] ; then
	INIT="shorewall6"
fi

ANNOTATED=
CYGWIN=
MAC=
MACHOST=
MANDIR=${MANDIR:-"/usr/share/man"}
SPARSE=
INSTALLD='-D'
[ -n "${LIBEXEC:=/usr/share}" ]
[ -n "${PERLLIB:=/usr/share/shorewall}" ]

case "$LIBEXEC" in
    /*)
	;;
    *)
	LIBEXEC=/usr/${LIBEXEC}
	;;
esac

case "$PERLLIB" in
    /*)
	;;
    *)
	PERLLIB=/usr/${PERLLIB}
	;;
esac

case $(uname) in
    CYGWIN*)
	if [ -z "$DESTDIR" ]; then
	    DEST=
	    INIT=
	fi

	OWNER=$(id -un)
	GROUP=$(id -gn)
	CYGWIN=Yes
	SPARSE=Yes
	;;
    Darwin)
	if [ -z "$DESTDIR" ]; then
	    DEST=
	    INIT=
	    SPARSE=Yes
	fi

	[ -z "$OWNER" ] && OWNER=root
	[ -z "$GROUP" ] && GROUP=wheel
	MAC=Yes
	MACHOST=Yes
	INSTALLD=
	;;	
    *)
	[ -z "$OWNER" ] && OWNER=root
	[ -z "$GROUP" ] && GROUP=root
	;;
esac

OWNERSHIP="-o $OWNER -g $GROUP"

finished=0

while [ $finished -eq 0 ]; do
    option=$1

    case "$option" in
	-*)
	    option=${option#-}
	    
	    while [ -n "$option" ]; do
		case $option in
		    h)
			usage 0
			;;
		    v)
			echo "Shorewall6 Firewall Installer Version $VERSION"
			exit 0
			;;
		    s*)
			SPARSE=Yes
			option=${option#s}
			;;
		    a*)
			ANNOTATED=Yes
			option=${option#a}
			;;
		    p*)
			ANNOTATED=
			option=${option#p}
			;;
		    *)
			usage 1
			;;
		esac
	    done

	    shift
	    ;;
	*)
	    [ -n "$option" ] && usage 1
	    finished=1
	    ;;
    esac
done

PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/bin:/usr/local/sbin

#
# Determine where to install the firewall script
#

if [ -n "$DESTDIR" ]; then
    if [ -z "$CYGWIN" ]; then
	if [ `id -u` != 0 ] ; then
	    echo "Not setting file owner/group permissions, not running as root."
	    OWNERSHIP=""
	fi    
    fi
	
    install -d $OWNERSHIP -m 755 ${DESTDIR}/sbin
    install -d $OWNERSHIP -m 755 ${DESTDIR}${DEST}
   
    CYGWIN=
    MAC=
else
    [ -x /usr/share/shorewall/compiler.pl ] || \
	{ echo "   ERROR: Shorewall >= 4.3.5 is not installed" >&2; exit 1; }
    if [ -n "$CYGWIN" ]; then
	echo "Installing Cygwin-specific configuration..."
    elif [ -n "$MAC" ]; then
	echo "Installing Mac-specific configuration..."	
    else
	if [ -d /etc/apt -a -e /usr/bin/dpkg ]; then
	    echo "Installing Debian-specific configuration..."
	    DEBIAN=yes
	    SPARSE=yes
        elif [ -f /etc/redhat-release ]; then
	    echo "Installing Redhat/Fedora-specific configuration..."
	    FEDORA=yes
	elif [ -f /etc/slackware-version ] ; then
	    echo "Installing Slackware-specific configuration..."
	    DEST="/etc/rc.d"
		SLACKWARE=yes
	    INIT="rc.firewall"
	elif [ -f /etc/arch-release ] ; then
	    echo "Installing ArchLinux-specific configuration..."
	    DEST="/etc/rc.d"
	    INIT="shorewall6"
	    ARCHLINUX=yes
	fi
    fi
fi

if [ -z "$DESTDIR" ]; then
    if [ -f /lib/systemd/system ]; then
	SYSTEMD=Yes
    fi
elif [ -n "$SYSTEMD" ]; then
    mkdir -p ${DESTDIR}/lib/systemd/system
fi

#
# Change to the directory containing this script
#
cd "$(dirname $0)"

echo "Installing Shorewall6 Version $VERSION"

#
# Check for /sbin/shorewall6
#
if [ -f ${DESTDIR}/sbin/shorewall6 ]; then
    first_install=""
else
    first_install="Yes"
fi

if [ -z "$CYGWIN" ]; then
   install_file shorewall6 ${DESTDIR}/sbin/shorewall6 0755 ${DESTDIR}/var/lib/shorewall6-${VERSION}.bkout
   if [ -z "$MACHOST" ]; then
       eval sed -i \'s\|g_libexec=.\*\|g_libexec=$LIBEXEC\|\' ${DESTDIR}/sbin/shorewall6
       eval sed -i \'s\|g_perllib=.\*\|g_perllib=$PERLLIB\|\' ${DESTDIR}/sbin/shorewall6
   else
       eval sed -i \'\' -e \'s\|g_libexec=.\*\|g_libexec=$LIBEXEC\|\' ${DESTDIR}/sbin/shorewall6
       eval sed -i \'\' -e \'s\|g_perllib=.\*\|g_perllib=$PERLLIB\|\' ${DESTDIR}/sbin/shorewall6
   fi
   echo "shorewall6 control program installed in ${DESTDIR}/sbin/shorewall6"
else
   install_file shorewall6 ${DESTDIR}/bin/shorewall6 0755 ${DESTDIR}/var/lib/shorewall6-${VERSION}.bkout
   eval sed -i \'s\|g_libexec=.\*\|g_libexec=$LIBEXEC\|\' ${DESTDIR}/bin/shorewall6
   eval sed -i \'s\|g_perllib=.\*\|g_perllib=$PERLLIB\|\' ${DESTDIR}/bin/shorewall6
   echo "shorewall6 control program installed in ${DESTDIR}/bin/shorewall6"
fi


#
# Install the Firewall Script
#
if [ -n "$DEBIAN" ]; then
    install_file init.debian.sh /etc/init.d/shorewall6 0544 ${DESTDIR}/usr/share/shorewall6-${VERSION}.bkout
elif [ -n "$FEDORA" ]; then
    install_file init.fedora.sh /etc/init.d/shorewall6 0544 ${DESTDIR}/usr/share/shorewall6-${VERSION}.bkout
elif [ -n "$SLACKWARE" ]; then
    install_file init.slackware.shorewall6.sh ${DESTDIR}${DEST}/rc.shorewall6 0544 ${DESTDIR}/usr/share/shorewall6-${VERSION}.bkout
elif [ -n "$ARCHLINUX" ]; then
    install_file init.archlinux.sh ${DESTDIR}${DEST}/$INIT 0544 ${DESTDIR}/usr/share/shorewall6-${VERSION}.bkout
elif [ -n "$INIT" ]; then
    install_file init.sh ${DESTDIR}${DEST}/$INIT 0544 ${DESTDIR}/usr/share/shorewall6-${VERSION}.bkout
fi

[ -n "$INIT" ] && echo  "Shorewall6 script installed in ${DESTDIR}${DEST}/$INIT"

#
# Create /etc/shorewall, /usr/share/shorewall and /var/lib/shorewall6 if needed
#
mkdir -p ${DESTDIR}/etc/shorewall6
mkdir -p ${DESTDIR}${LIBEXEC}/shorewall6
mkdir -p ${DESTDIR}${PERLLIB}/
mkdir -p ${DESTDIR}/usr/share/shorewall6/configfiles
mkdir -p ${DESTDIR}/var/lib/shorewall6

chmod 755 ${DESTDIR}/etc/shorewall6
chmod 755 ${DESTDIR}/usr/share/shorewall6
chmod 755 ${DESTDIR}/usr/share/shorewall6/configfiles

if [ -n "$DESTDIR" ]; then
    mkdir -p ${DESTDIR}/etc/logrotate.d
    chmod 755 ${DESTDIR}/etc/logrotate.d
fi

#
# Install the .service file
#
if [ -n "$SYSTEMD" ]; then
    run_install $OWNERSHIP -m 600 shorewall6.service ${DESTDIR}/lib/systemd/system/shorewall6.service
    echo "Service file installed as ${DESTDIR}/lib/systemd/system/shorewall6.service"
fi

delete_file ${DESTDIR}/usr/share/shorewall6/compiler
delete_file ${DESTDIR}/usr/share/shorewall6/lib.accounting
delete_file ${DESTDIR}/usr/share/shorewall6/lib.actions
delete_file ${DESTDIR}/usr/share/shorewall6/lib.dynamiczones
delete_file ${DESTDIR}/usr/share/shorewall6/lib.maclist
delete_file ${DESTDIR}/usr/share/shorewall6/lib.nat
delete_file ${DESTDIR}/usr/share/shorewall6/lib.providers
delete_file ${DESTDIR}/usr/share/shorewall6/lib.proxyarp
delete_file ${DESTDIR}/usr/share/shorewall6/lib.tc
delete_file ${DESTDIR}/usr/share/shorewall6/lib.tcrules
delete_file ${DESTDIR}/usr/share/shorewall6/lib.tunnels
delete_file ${DESTDIR}/usr/share/shorewall6/prog.header6
delete_file ${DESTDIR}/usr/share/shorewall6/prog.footer6

#
# Install wait4ifup
#

install_file wait4ifup ${DESTDIR}${LIBEXEC}/shorewall6/wait4ifup 0755

echo
echo "wait4ifup installed in ${DESTDIR}${LIBEXEC}/shorewall6/wait4ifup"

#
# Install the Modules file
#
run_install $OWNERSHIP -m 0644 modules ${DESTDIR}/usr/share/shorewall6/modules
echo "Modules file installed as ${DESTDIR}/usr/share/shorewall6/modules"

for f in modules.*; do
    run_install $OWNERSHIP -m 0644 $f ${DESTDIR}/usr/share/shorewall6/$f
    echo "Modules file $f installed as ${DESTDIR}/usr/share/shorewall6/$f"
done

#
# Install the Module Helpers file
#
run_install $OWNERSHIP -m 0644 helpers ${DESTDIR}/usr/share/shorewall6/helpers
echo "Helper modules file installed as ${DESTDIR}/usr/share/shorewall6/helpers"

#
# Install the default config path file
#
install_file configpath ${DESTDIR}/usr/share/shorewall6/configpath 0644
echo "Default config path file installed as ${DESTDIR}/usr/share/shorewall6/configpath"
#
# Install the Standard Actions file
#
install_file actions.std ${DESTDIR}/usr/share/shorewall6/actions.std 0644
echo "Standard actions file installed as ${DESTDIR}/usr/shared/shorewall6/actions.std"

cd configfiles

if [ -n "$ANNOTATED" ]; then
    suffix=.annotated
else
    suffix=
fi

#
# Install the config file
#
run_install $OWNERSHIP -m 0644 shorewall6.conf           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 shorewall6.conf.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/


if [ ! -f ${DESTDIR}/etc/shorewall6/shorewall6.conf ]; then
   run_install $OWNERSHIP -m 0644 shorewall6.conf${suffix} ${DESTDIR}/etc/shorewall6/shorewall6.conf

   if [ -n "$DEBIAN" ] && mywhich perl; then
       #
       # Make a Debian-like shorewall6.conf
       #
       perl -p -w -i -e 's|^STARTUP_ENABLED=.*|STARTUP_ENABLED=Yes|;' ${DESTDIR}/etc/shorewall6/shorewall6.conf
   fi

   echo "Config file installed as ${DESTDIR}/etc/shorewall6/shorewall6.conf"
fi


if [ -n "$ARCHLINUX" ] ; then
   sed -e 's!LOGFILE=/var/log/messages!LOGFILE=/var/log/messages.log!' -i ${DESTDIR}/etc/shorewall6/shorewall6.conf
fi

#
# Install the init file
#
run_install $OWNERSHIP -m 0644 init ${DESTDIR}/usr/share/shorewall6/configfiles/init

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/init ]; then
    run_install $OWNERSHIP -m 0600 init ${DESTDIR}/etc/shorewall6/init
    echo "Init file installed as ${DESTDIR}/etc/shorewall6/init"
fi

#
# Install the zones file
#
run_install $OWNERSHIP -m 0644 zones           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 zones.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/zones ]; then
    run_install $OWNERSHIP -m 0644 zones${suffix} ${DESTDIR}/etc/shorewall6/zones
    echo "Zones file installed as ${DESTDIR}/etc/shorewall6/zones"
fi

#
# Install the policy file
#
run_install $OWNERSHIP -m 0644 policy           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 policy.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/policy ]; then
    run_install $OWNERSHIP -m 0600 policy${suffix} ${DESTDIR}/etc/shorewall6/policy
    echo "Policy file installed as ${DESTDIR}/etc/shorewall6/policy"
fi
#
# Install the interfaces file
#
run_install $OWNERSHIP -m 0644 interfaces           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 interfaces.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/interfaces ]; then
    run_install $OWNERSHIP -m 0600 interfaces${suffix} ${DESTDIR}/etc/shorewall6/interfaces
    echo "Interfaces file installed as ${DESTDIR}/etc/shorewall6/interfaces"
fi

#
# Install the hosts file
#
run_install $OWNERSHIP -m 0644 hosts           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 hosts.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/hosts ]; then
    run_install $OWNERSHIP -m 0600 hosts${suffix} ${DESTDIR}/etc/shorewall6/hosts
    echo "Hosts file installed as ${DESTDIR}/etc/shorewall6/hosts"
fi
#
# Install the rules file
#
run_install $OWNERSHIP -m 0644 rules           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 rules.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/rules ]; then
    run_install $OWNERSHIP -m 0600 rules${suffix} ${DESTDIR}/etc/shorewall6/rules
    echo "Rules file installed as ${DESTDIR}/etc/shorewall6/rules"
fi
#
# Install the Parameters file
#
run_install $OWNERSHIP -m 0644 params          ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 params.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -f ${DESTDIR}/etc/shorewall6/params ]; then
    chmod 0644 ${DESTDIR}/etc/shorewall6/params
else
    run_install $OWNERSHIP -m 0644 params${suffix} ${DESTDIR}/etc/shorewall6/params
    echo "Parameter file installed as ${DESTDIR}/etc/shorewall6/params"
fi
#
# Install the Stopped Routing file
#
run_install $OWNERSHIP -m 0644 routestopped           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 routestopped.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/routestopped ]; then
    run_install $OWNERSHIP -m 0600 routestopped${suffix} ${DESTDIR}/etc/shorewall6/routestopped
    echo "Stopped Routing file installed as ${DESTDIR}/etc/shorewall6/routestopped"
fi
#
# Install the Mac List file
#
run_install $OWNERSHIP -m 0644 maclist           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 maclist.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/maclist ]; then
    run_install $OWNERSHIP -m 0600 maclist${suffix} ${DESTDIR}/etc/shorewall6/maclist
    echo "MAC list file installed as ${DESTDIR}/etc/shorewall6/maclist"
fi

#
# Install the TC Rules file
#
run_install $OWNERSHIP -m 0644 tcrules           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 tcrules.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/tcrules ]; then
    run_install $OWNERSHIP -m 0600 tcrules${suffix} ${DESTDIR}/etc/shorewall6/tcrules
    echo "TC Rules file installed as ${DESTDIR}/etc/shorewall6/tcrules"
fi

#
# Install the TC Interfaces file
#
run_install $OWNERSHIP -m 0644 tcinterfaces           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 tcinterfaces.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/tcinterfaces ]; then
    run_install $OWNERSHIP -m 0600 tcinterfaces${suffix} ${DESTDIR}/etc/shorewall6/tcinterfaces
    echo "TC Interfaces file installed as ${DESTDIR}/etc/shorewall6/tcinterfaces"
fi

#
# Install the TC Priority file
#
run_install $OWNERSHIP -m 0644 tcpri           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 tcpri.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/tcpri ]; then
    run_install $OWNERSHIP -m 0600 tcpri${suffix} ${DESTDIR}/etc/shorewall6/tcpri
    echo "TC Priority file installed as ${DESTDIR}/etc/shorewall6/tcpri"
fi

#
# Install the TOS file
#
run_install $OWNERSHIP -m 0644 tos           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 tos.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/tos ]; then
    run_install $OWNERSHIP -m 0600 tos${suffix} ${DESTDIR}/etc/shorewall6/tos
    echo "TOS file installed as ${DESTDIR}/etc/shorewall6/tos"
fi
#
# Install the Tunnels file
#
run_install $OWNERSHIP -m 0644 tunnels           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 tunnels.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/tunnels ]; then
    run_install $OWNERSHIP -m 0600 tunnels${suffix} ${DESTDIR}/etc/shorewall6/tunnels
    echo "Tunnels file installed as ${DESTDIR}/etc/shorewall6/tunnels"
fi
#
# Install the blacklist file
#
run_install $OWNERSHIP -m 0644 blacklist           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 blacklist.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/blacklist ]; then
    run_install $OWNERSHIP -m 0600 blacklist${suffix} ${DESTDIR}/etc/shorewall6/blacklist
    echo "Blacklist file installed as ${DESTDIR}/etc/shorewall6/blacklist"
fi
#
# Install the Providers file
#
run_install $OWNERSHIP -m 0644 providers           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 providers.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/providers ]; then
    run_install $OWNERSHIP -m 0600 providers${suffix} ${DESTDIR}/etc/shorewall6/providers
    echo "Providers file installed as ${DESTDIR}/etc/shorewall6/providers"
fi

#
# Install the Route Rules file
#
run_install $OWNERSHIP -m 0644 route_rules           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 route_rules.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/route_rules ]; then
    run_install $OWNERSHIP -m 0600 route_rules${suffix} ${DESTDIR}/etc/shorewall6/route_rules
    echo "Routing rules file installed as ${DESTDIR}/etc/shorewall6/route_rules"
fi

#
# Install the tcclasses file
#
run_install $OWNERSHIP -m 0644 tcclasses           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 tcclasses.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/tcclasses ]; then
    run_install $OWNERSHIP -m 0600 tcclasses${suffix} ${DESTDIR}/etc/shorewall6/tcclasses
    echo "TC Classes file installed as ${DESTDIR}/etc/shorewall6/tcclasses"
fi

#
# Install the tcdevices file
#
run_install $OWNERSHIP -m 0644 tcdevices           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 tcdevices.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/tcdevices ]; then
    run_install $OWNERSHIP -m 0600 tcdevices${suffix} ${DESTDIR}/etc/shorewall6/tcdevices
    echo "TC Devices file installed as ${DESTDIR}/etc/shorewall6/tcdevices"
fi

#
# Install the tcfilters file
#
run_install $OWNERSHIP -m 0644 tcfilters           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 tcfilters.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/tcfilters ]; then
    run_install $OWNERSHIP -m 0600 tcfilters${suffix} ${DESTDIR}/etc/shorewall6/tcfilters
    echo "TC Filters file installed as ${DESTDIR}/etc/shorewall6/tcfilters"
fi

#
# Install the Notrack file
#
run_install $OWNERSHIP -m 0644 notrack           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 notrack.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/notrack ]; then
    run_install $OWNERSHIP -m 0600 notrack${suffix} ${DESTDIR}/etc/shorewall6/notrack
    echo "Notrack file installed as ${DESTDIR}/etc/shorewall6/notrack"
fi

#
# Install the Secmarks file
#
run_install $OWNERSHIP -m 0644 secmarks ${DESTDIR}/usr/share/shorewall6/configfiles/secmarks

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/secmarks ]; then
    run_install $OWNERSHIP -m 0600 secmarks ${DESTDIR}/etc/shorewall6/secmarks
    echo "Secmarks file installed as ${DESTDIR}/etc/shorewall6/secmarks"
fi
#
# Install the start file
#
run_install $OWNERSHIP -m 0644 start ${DESTDIR}/usr/share/shorewall6/configfiles/start

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/start ]; then
    run_install $OWNERSHIP -m 0600 start ${DESTDIR}/etc/shorewall6/start
    echo "Start file installed as ${DESTDIR}/etc/shorewall6/start"
fi
#
# Install the stop file
#
run_install $OWNERSHIP -m 0644 stop ${DESTDIR}/usr/share/shorewall6/configfiles/stop

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/stop ]; then
    run_install $OWNERSHIP -m 0600 stop ${DESTDIR}/etc/shorewall6/stop
    echo "Stop file installed as ${DESTDIR}/etc/shorewall6/stop"
fi
#
# Install the stopped file
#
run_install $OWNERSHIP -m 0644 stopped ${DESTDIR}/usr/share/shorewall6/configfiles/stopped

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/stopped ]; then
    run_install $OWNERSHIP -m 0600 stopped ${DESTDIR}/etc/shorewall6/stopped
    echo "Stopped file installed as ${DESTDIR}/etc/shorewall6/stopped"
fi
#
# Install the Accounting file
#
run_install $OWNERSHIP -m 0644 accounting           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 accounting.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/accounting ]; then
    run_install $OWNERSHIP -m 0600 accounting${suffix} ${DESTDIR}/etc/shorewall6/accounting
    echo "Accounting file installed as ${DESTDIR}/etc/shorewall6/accounting"
fi
#
# Install the Started file
#
run_install $OWNERSHIP -m 0644 started ${DESTDIR}/usr/share/shorewall6/configfiles/started

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/started ]; then
    run_install $OWNERSHIP -m 0600 started ${DESTDIR}/etc/shorewall6/started
    echo "Started file installed as ${DESTDIR}/etc/shorewall6/started"
fi
#
# Install the Restored file
#
run_install $OWNERSHIP -m 0644 restored ${DESTDIR}/usr/share/shorewall6/configfiles/restored

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/restored ]; then
    run_install $OWNERSHIP -m 0600 restored ${DESTDIR}/etc/shorewall6/restored
    echo "Restored file installed as ${DESTDIR}/etc/shorewall6/restored"
fi
#
# Install the Clear file
#
run_install $OWNERSHIP -m 0644 clear ${DESTDIR}/usr/share/shorewall6/configfiles/clear

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/clear ]; then
    run_install $OWNERSHIP -m 0600 clear ${DESTDIR}/etc/shorewall6/clear
    echo "Clear file installed as ${DESTDIR}/etc/shorewall6/clear"
fi
#
# Install the Isusable file
#
run_install $OWNERSHIP -m 0644 isusable ${DESTDIR}/usr/share/shorewall6/configfiles/isusable

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/isusable ]; then
    run_install $OWNERSHIP -m 0600 isusable ${DESTDIR}/etc/shorewall6/isusable
    echo "Isusable file installed as ${DESTDIR}/etc/shorewall/isusable"
fi
#
# Install the Refresh file
#
run_install $OWNERSHIP -m 0644 refresh ${DESTDIR}/usr/share/shorewall6/configfiles/refresh

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/refresh ]; then
    run_install $OWNERSHIP -m 0600 refresh ${DESTDIR}/etc/shorewall6/refresh
    echo "Refresh file installed as ${DESTDIR}/etc/shorewall6/refresh"
fi
#
# Install the Refreshed file
#
run_install $OWNERSHIP -m 0644 refreshed ${DESTDIR}/usr/share/shorewall6/configfiles/refreshed

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/refreshed ]; then
    run_install $OWNERSHIP -m 0600 refreshed ${DESTDIR}/etc/shorewall6/refreshed
    echo "Refreshed file installed as ${DESTDIR}/etc/shorewall6/refreshed"
fi
#
# Install the Tcclear file
#
run_install $OWNERSHIP -m 0644 tcclear           ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/tcclear ]; then
    run_install $OWNERSHIP -m 0600 tcclear ${DESTDIR}/etc/shorewall6/tcclear
    echo "Tcclear file installed as ${DESTDIR}/etc/shorewall6/tcclear"
fi
#
# Install the Scfilter file
#
run_install $OWNERSHIP -m 0644 scfilter ${DESTDIR}/usr/share/shorewall6/configfiles/scfilter

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/scfilter ]; then
    run_install $OWNERSHIP -m 0600 scfilter ${DESTDIR}/etc/shorewall6/scfilter
    echo "Scfilter file installed as ${DESTDIR}/etc/shorewall6/scfilter"
fi

#
# Install the Providers file
#
run_install $OWNERSHIP -m 0644 providers           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 providers.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/providers ]; then
    run_install $OWNERSHIP -m 0600 providers${suffix} ${DESTDIR}/etc/shorewall6/providers
    echo "Providers file installed as ${DESTDIR}/etc/shorewall6/providers"
fi
#
# Install the Proxyndp file
#
run_install $OWNERSHIP -m 0644 proxyndp           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 proxyndp.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/proxyndp ]; then
    run_install $OWNERSHIP -m 0600 proxyndp${suffix} ${DESTDIR}/etc/shorewall6/proxyndp
    echo "Proxyndp file installed as ${DESTDIR}/etc/shorewall6/proxyndp"
fi

#
# Install the Actions file
#
run_install $OWNERSHIP -m 0644 actions           ${DESTDIR}/usr/share/shorewall6/configfiles/
run_install $OWNERSHIP -m 0644 actions.annotated ${DESTDIR}/usr/share/shorewall6/configfiles/

if [ -z "$SPARSE" -a ! -f ${DESTDIR}/etc/shorewall6/actions ]; then
    run_install $OWNERSHIP -m 0644 actions${suffix} ${DESTDIR}/etc/shorewall6/actions
    echo "Actions file installed as ${DESTDIR}/etc/shorewall6/actions"
fi

cd ..

#
# Install the  Makefiles
#
run_install $OWNERSHIP -m 0644 Makefile-lite ${DESTDIR}/usr/share/shorewall6/configfiles/Makefile

if [ -z "$SPARSE" ]; then
    run_install $OWNERSHIP -m 0600 Makefile ${DESTDIR}/etc/shorewall6/Makefile
    echo "Makefile installed as ${DESTDIR}/etc/shorewall6/Makefile"
fi
#
# Install the Action files
#
for f in action.* ; do
    install_file $f ${DESTDIR}/usr/share/shorewall6/$f 0644
    echo "Action ${f#*.} file installed as ${DESTDIR}/usr/share/shorewall6/$f"
done

# Install the Macro files
#
for f in macro.* ; do
    install_file $f ${DESTDIR}/usr/share/shorewall6/$f 0644
    echo "Macro ${f#*.} file installed as ${DESTDIR}/usr/share/shorewall6/$f"
done
#
# Install the libraries
#
for f in lib.* ; do
    if [ -f $f ]; then
	install_file $f ${DESTDIR}/usr/share/shorewall6/$f 0644
	echo "Library ${f#*.} file installed as ${DESTDIR}/usr/share/shorewall6/$f"
    fi
done
#
# Symbolically link 'functions' to lib.base
#
ln -sf lib.base ${DESTDIR}/usr/share/shorewall6/functions
#
# Create the version file
#
echo "$VERSION" > ${DESTDIR}/usr/share/shorewall6/version
chmod 644 ${DESTDIR}/usr/share/shorewall6/version
#
# Remove and create the symbolic link to the init script
#

if [ -z "$DESTDIR" ]; then
    rm -f /usr/share/shorewall6/init
    ln -s ${DEST}/${INIT} /usr/share/shorewall6/init
fi

#
# Install the Man Pages
#

cd manpages

[ -n "$INSTALLD" ] || mkdir -p ${DESTDIR}${MANDIR}/man5/ ${DESTDIR}${MANDIR}/man8/

for f in *.5; do
    gzip -c $f > $f.gz
    run_install $INSTALLD  -m 0644 $f.gz ${DESTDIR}${MANDIR}/man5/$f.gz
    echo "Man page $f.gz installed to ${DESTDIR}${MANDIR}/man5/$f.gz"
done

for f in *.8; do
    gzip -c $f > $f.gz
    run_install $INSTALLD  -m 0644 $f.gz ${DESTDIR}${MANDIR}/man8/$f.gz
    echo "Man page $f.gz installed to ${DESTDIR}${MANDIR}/man8/$f.gz"
done

cd ..

echo "Man Pages Installed"

if [ -d ${DESTDIR}/etc/logrotate.d ]; then
    run_install $OWNERSHIP -m 0644 logrotate ${DESTDIR}/etc/logrotate.d/shorewall6
    echo "Logrotate file installed as ${DESTDIR}/etc/logrotate.d/shorewall6"
fi

if [ -z "$DESTDIR" -a -n "$first_install" -a -z "${CYGWIN}${MAC}" ]; then
    if [ -n "$DEBIAN" ]; then
	run_install $OWNERSHIP -m 0644 default.debian /etc/default/shorewall6

	update-rc.d shorewall6 defaults

	echo "shorewall6 will start automatically at boot"
	echo "Set startup=1 in /etc/default/shorewall6 to enable"
	touch /var/log/shorewall6-init.log
	perl -p -w -i -e 's/^STARTUP_ENABLED=No/STARTUP_ENABLED=Yes/;s/^IP_FORWARDING=On/IP_FORWARDING=Keep/;s/^SUBSYSLOCK=.*/SUBSYSLOCK=/;' /etc/shorewall6/shorewall6.conf
    else
	if [ -n "$SYSTEMD" ]; then
	    if systemctl enable shorewall6; then
		echo "Shorewall6 will start automatically at boot"
	    fi
	elif [ -x /sbin/insserv -o -x /usr/sbin/insserv ]; then
	    if insserv /etc/init.d/shorewall6 ; then
		echo "shorewall6 will start automatically at boot"
		echo "Set STARTUP_ENABLED=Yes in /etc/shorewall6/shorewall6.conf to enable"
	    else
		cant_autostart
	    fi
	elif [ -x /sbin/chkconfig -o -x /usr/sbin/chkconfig ]; then
	    if chkconfig --add shorewall6 ; then
		echo "shorewall6 will start automatically in run levels as follows:"
		echo "Set STARTUP_ENABLED=Yes in /etc/shorewall6/shorewall6.conf to enable"
		chkconfig --list shorewall6
	    else
		cant_autostart
	    fi
	elif [ -x /sbin/rc-update ]; then
	    if rc-update add shorewall6 default; then
		echo "shorewall6 will start automatically at boot"
		echo "Set STARTUP_ENABLED=Yes in /etc/shorewall6/shorewall6.conf to enable"
	    else
		cant_autostart
	    fi
	elif [ "$INIT" != rc.firewall ]; then #Slackware starts this automatically
	    cant_autostart
	fi
    fi
fi

#
#  Report Success
#
echo "shorewall6 Version $VERSION Installed"
