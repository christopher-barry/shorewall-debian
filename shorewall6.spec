%define name shorewall6
%define version 5.0.7
%define release 2

Summary: Shoreline Firewall 6 is an ip6tables-based firewall for Linux systems.
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
Requires: iptables iproute shorewall >= 4.5.0-0
Provides: shoreline_firewall = %{version}-%{release}

%description

The Shoreline Firewall 6, more commonly known as "Shorewall6", is a Netfilter
(ip6tables) based IPv6 firewall that can be used on a dedicated firewall system,
a multi-function gateway/ router/server or on a standalone GNU/Linux system.

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

touch %{buildroot}/etc/shorewall6/isusable
touch %{buildroot}/etc/shorewall6/notrack

%clean
rm -rf $RPM_BUILD_ROOT

%post

if [ $1 -eq 1 ]; then
	if [ -x %{_sbindir}/insserv ]; then
		%{_sbindir}/insserv /etc/rc.d/shorewall6
	elif [ -x %{_sbindir}/chkconfig ]; then
		%{_sbindir}/chkconfig --add shorewall6;
	fi
fi

%preun

if [ $1 = 0 ]; then
	if [ -x %{_sbindir}/insserv ]; then
		%{_sbindir}/insserv -r %{_initddir}/shorewall6
	elif [ -x %{_sbindir}/chkconfig ]; then
		%{_sbindir}/chkconfig --del shorewall6
	fi

	rm -f /etc/shorewall/startup_disabled

fi

%files
%defattr(0644,root,root,0755)
%attr(0544,root,root) %{_initddir}/shorewall6
%attr(0755,root,root) %dir /etc/shorewall6
%ghost %(attr 0644,root,root) /etc/shorewall6/isusable
%ghost %(attr 0644,root,root) /etc/shorewall6/notrack
%attr(0755,root,root) %dir /usr/share/shorewall6
%attr(0755,root,root) %dir /usr/share/shorewall6/configfiles
%attr(0700,root,root) %dir /var/lib/shorewall6
%attr(0600,root,root) %config(noreplace) /etc/shorewall6/*

%attr(0755,root,root) %dir /etc/sysconfig/
%attr(0600,root,root) %config(noreplace) /etc/sysconfig/shorewall6

%attr(0600,root,root) /etc/shorewall6/Makefile

%attr(0644,root,root) /etc/logrotate.d/shorewall6

%attr(0755,root,root) %{_sbindir}/shorewall6

%attr(0644,root,root) /usr/share/shorewall6/version
%attr(0644,root,root) /usr/share/shorewall6/actions.std
%attr(0644,root,root) /usr/share/shorewall6/action.AllowICMPs
%attr(0644,root,root) /usr/share/shorewall6/action.A_AllowICMPs
%attr(0644,root,root) /usr/share/shorewall6/action.Broadcast
%attr(0644,root,root) /usr/share/shorewall6/action.Drop
%attr(0644,root,root) /usr/share/shorewall6/action.A_Drop
%attr(0644,root,root) /usr/share/shorewall6/action.Reject
%attr(0644,root,root) /usr/share/shorewall6/action.A_Reject
%attr(0644,root,root) /usr/share/shorewall6/action.mangletemplate
%attr(0644,root,root) /usr/share/shorewall6/action.template
%attr(-   ,root,root) /usr/share/shorewall6/functions
%attr(0644,root,root) /usr/share/shorewall6/lib.base
%attr(0644,root,root) /usr/share/shorewall6/macro.*
%attr(0644,root,root) /usr/share/shorewall6/modules*
%attr(0644,root,root) /usr/share/shorewall6/helpers
%attr(0644,root,root) /usr/share/shorewall6/configpath

%attr(0644,root,root) /usr/share/shorewall6/configfiles/*

%attr(0644,root,root) %{_mandir}/man5/*
%attr(0644,root,root) %{_mandir}/man8/shorewall6.8.gz

%doc COPYING INSTALL changelog.txt releasenotes.txt tunnel ipsecvpn ipv6 Samples6

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
- Updated to 5.0.6-0RC1
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
