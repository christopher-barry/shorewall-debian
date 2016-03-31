%define name shorewall-init
%define version 5.0.7
%define release 2

Summary: Shorewall-init adds functionality to Shoreline Firewall (Shorewall).
Name: %{name}
Version: %{version}
Release: %{release}
License: GPLv2
Packager: Tom Eastep <teastep@shorewall.net>
Group: Networking/Utilities
Source: %{name}-%{version}.tgz
URL: http://www.shorewall.net/
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: shoreline_firewall >= 4.5.0

%description

The Shoreline Firewall, more commonly known as "Shorewall", is a Netfilter
(iptables) based firewall that can be used on a dedicated firewall system,
a multi-function gateway/ router/server or on a standalone GNU/Linux system.

Shorewall Init is a companion product to Shorewall that allows for tigher
control of connections during boot and that integrates Shorewall with
ifup/ifdown and NetworkManager.

%prep

%setup

%build

%install

./configure.pl --host=%{_vendor} \
               --prefix=%{_prefix} \
               --tmpdir=%{_tmpdir} \
               --perllibdir=%{perl_vendorlib} \
               --libexecdir=%{_libexecdir} \
               --sbindir=%{_sbindir}

DESTDIR=%{buildroot} ./install.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post

if [ $1 -eq 1 ]; then
    if [ -x %{_sbindir}/insserv ]; then
	%{_sbindir}/insserv %{_initddir}/shorewall-init
    elif [ -x %{_sbindir}/chkconfig ]; then
	%{_sbindir}/chkconfig --add shorewall-init;
    fi
fi

if [ -f /etc/SuSE-release ]; then
    cp -pf %{_libexecdir}/shorewall-init/ifupdown /etc/sysconfig/network/if-up.d/shorewall
    cp -pf %{_libexecdir}/shorewall-init/ifupdown /etc/sysconfig/network/if-down.d/shorewall
    if [ -d /etc/ppp ]; then
	for directory in ip-up.d ip-down.d ipv6-up.d ipv6-down.d; do
	    mkdir -p /etc/ppp/$directory
	    cp -pf %{_libexecdir}/shorewall-init/ifupdown /etc/ppp/$directory/shorewall
	done
    fi
else
    if [ -f %{_sbindir}/ifup-local -o -f %{_sbindir}/ifdown-local ]; then
	if ! grep -q Shorewall %{_sbindir}/ifup-local || ! grep -q Shorewall %{_sbindir}/ifdown-local; then
	    echo "WARNING: %{_sbindir}/ifup-local and/or %{_sbindir}/ifdown-local already exist; ifup/ifdown events will not be handled" >&2
	else
	    cp -pf %{_libexecdir}/shorewall-init/ifupdown %{_sbindir}/ifup-local
	    cp -pf %{_libexecdir}/shorewall-init/ifupdown %{_sbindir}/ifdown-local
	fi
    else
	cp -pf %{_libexecdir}/shorewall-init/ifupdown %{_sbindir}/ifup-local
	cp -pf %{_libexecdir}/shorewall-init/ifupdown %{_sbindir}/ifdown-local
    fi

    if [ -d /etc/ppp ]; then
	if [ -f /etc/ppp/ip-up.local -o -f /etc/ppp/ip-down.local ]; then
	    if ! grep -q Shorewall-based /etc/ppp/ip-up.local || ! grep -q Shorewall-based /etc/ppp//ip-down.local; then
		echo "WARNING: /etc/ppp/ip-up.local and/or /etc/ppp/ip-down.local already exist; ppp devices will not be handled" >&2
	    fi
	else
	    cp -pf %{_libexecdir}/shorewall-init/ifupdown /etc/ppp/ip-up.local
	    cp -pf %{_libexecdir}/shorewall-init/ifupdown /etc/ppp/ip-down.local
	fi
    fi

    if [ -d /etc/NetworkManager/dispatcher.d/ ]; then
	cp -pf %{_libexecdir}/shorewall-init/ifupdown /etc/NetworkManager/dispatcher.d/01-shorewall
    fi
fi

%preun

if [ $1 -eq 0 ]; then
    if [ -x %{_sbindir}/insserv ]; then
	%{_sbindir}/insserv -r %{_initddir}/shorewall-init
    elif [ -x %{_sbindir}/chkconfig ]; then
	%{_sbindir}/chkconfig --del shorewall-init
    fi

    [ -f %{_sbindir}/ifup-local ]   && grep -q Shorewall %{_sbindir}/ifup-local   && rm -f %{_sbindir}/ifup-local
    [ -f %{_sbindir}/ifdown-local ] && grep -q Shorewall %{_sbindir}/ifdown-local && rm -f %{_sbindir}/ifdown-local

    [ -f /etc/ppp/ip-up.local ]   && grep -q Shorewall-based /etc/ppp/ip-up.local   && rm -f /etc/ppp/ip-up.local
    [ -f /etc/ppp/ip-down.local ] && grep -q Shorewall-based /etc/ppp/ip-down.local && rm -f /etc/ppp/ip-down.local

    rm -f /etc/NetworkManager/dispatcher.d/01-shorewall
fi

%files
%defattr(0644,root,root,0755)
%attr(0644,root,root) %config(noreplace) /etc/sysconfig/shorewall-init

%attr(0544,root,root) %{_initddir}/shorewall-init
%attr(0755,root,root) %dir %{_libexecdir}/shorewall-init

%attr(0644,root,root) /etc/logrotate.d/shorewall-init

%attr(0644,root,root) /usr/share/shorewall-init/version
%attr(0544,root,root) %{_libexecdir}/shorewall-init/ifupdown

%doc COPYING changelog.txt releasenotes.txt

%changelog
* Tue Mar 29 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.7-2
* Mon Mar 28 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.7-1
* Thu Mar 24 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.7-0base
* Fri Mar 18 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.7-0RC1
* Sun Mar 13 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.7-0Beta4
* Sun Mar 13 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.7-0Beta3
* Tue Mar 08 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.7-0Beta2
* Sat Mar 05 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.7-0Beta1
* Fri Mar 04 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.6-0Beta6
* Fri Mar 04 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.6-0Beta5
* Thu Mar 03 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.6-0Beta4
* Sat Feb 27 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.6-0Beta3
* Sun Feb 21 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.6-0Beta2
* Fri Feb 19 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.6-0Beta1
* Wed Feb 17 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.5-0base
* Mon Feb 15 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.5-0RC2
* Wed Feb 03 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.5-0RC1
* Fri Jan 29 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.5-0Beta2
* Wed Jan 20 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.5-0Beta1
* Wed Jan 20 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.4-0base
* Tue Jan 19 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.4-0RC2
* Mon Jan 11 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.4-0RC1
* Tue Jan 05 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.4-0Beta2
* Sat Jan 02 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.4-0Beta1
* Sun Dec 27 2015 Tom Eastep tom@shorewall.net
- Updated to 5.0.3-0base
* Thu Dec 24 2015 Tom Eastep tom@shorewall.net
- Updated to 5.0.3-0RC2
* Sun Dec 13 2015 Tom Eastep tom@shorewall.net
- Updated to 5.0.3-0RC1
* Sat Dec 05 2015 Tom Eastep tom@shorewall.net
- Updated to 5.0.3-0Beta2
* Sat Nov 28 2015 Tom Eastep tom@shorewall.net
- Updated to 5.0.3-0Beta1
* Sat Nov 21 2015 Tom Eastep tom@shorewall.net
- Updated to 5.0.2-1
* Sat Nov 07 2015 Tom Eastep tom@shorewall.net
- Updated to 5.0.2-0base
* Sun Nov 01 2015 Tom Eastep tom@shorewall.net
- Updated to 5.0.2-0RC1
* Mon Oct 26 2015 Tom Eastep tom@shorewall.net
- Updated to 5.0.2-0Beta2
* Mon Oct 26 2015 Tom Eastep tom@shorewall.net
- Updated to 5.0.2-0Beta1
* Tue Oct 13 2015 Tom Eastep tom@shorewall.net
- Updated to 5.0.1-1
* Mon Oct 12 2015 Tom Eastep tom@shorewall.net
- Updated to 5.0.1-0base
* Sat Oct 03 2015 Tom Eastep tom@shorewall.net
- Updated to 5.0.0-0base
* Mon Sep 21 2015 Tom Eastep tom@shorewall.net
- Updated to 5.0.0-0RC1
* Thu Sep 10 2015 Tom Eastep tom@shorewall.net
- Updated to 5.0.0-0Beta2
* Mon Jul 27 2015 Tom Eastep tom@shorewall.net
- Updated to 5.0.0-0Beta1
