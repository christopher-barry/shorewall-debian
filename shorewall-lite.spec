%define name shorewall-lite
%define version 5.0.7
%define release 2
%define initdir /etc/init.d

Summary: Shoreline Firewall Lite is an iptables-based firewall for Linux systems.
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
Requires: iptables iproute shorewall-core
Provides: shoreline_firewall = %{version}-%{release}

%description

The Shoreline Firewall, more commonly known as "Shorewall", is a Netfilter
(iptables) based firewall that can be used on a dedicated firewall system,
a multi-function gateway/ router/server or on a standalone GNU/Linux system.

Shorewall Lite is a companion product to Shorewall that allows network
administrators to centralize the configuration of Shorewall-based firewalls.

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

%pre

if [ -f /etc/shorewall-lite/shorewall.conf ]; then
    cp -fa /etc/shorewall-lite/shorewall.conf /etc/shorewall-lite/shorewall.conf.rpmsave
fi

%post

if [ $1 -eq 1 ]; then
    if [ -x %{_sbindir}/insserv ]; then
	%{_sbindir}/insserv %{_initddir}/shorewall-lite
    elif [ -x %{_sbindir}/chkconfig ]; then
	%{_sbindir}/chkconfig --add shorewall-lite;
    fi
elif [ -f /etc/shorewall-lite/shorewall.conf.rpmsave ]; then
    mv -f /etc/shorewall-lite/shorewall-lite.conf /etc/shorewall-lite/shorewall-lite.conf.rpmnew
    mv -f /etc/shorewall-lite/shorewall.conf.rpmsave /etc/shorewall-lite/shorewall-lite.conf
    echo "/etc/shorewall-lite/shorewall.conf retained as /etc/shorewall-lite/shorewall-lite.conf"
    echo "/etc/shorewall-lite/shorewall-lite.conf installed as /etc/shorewall-lite/shorewall-lite.conf.rpmnew"
fi

%preun

if [ $1 -eq 0 ]; then
    if [ -x %{_sbindir}/insserv ]; then
	%{_sbindir}/insserv -r %{_initddir}/shorewall-lite
    elif [ -x %{_sbindir}/chkconfig ]; then
	%{_sbindir}/chkconfig --del shorewall-lite
    fi
fi

%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) %dir /etc/shorewall-lite
%attr(0644,root,root) %config(noreplace) /etc/shorewall-lite/shorewall-lite.conf
%attr(0644,root,root) /etc/shorewall-lite/Makefile
%attr(0544,root,root) %{_initddir}/shorewall-lite
%attr(0755,root,root) %dir /usr/share/shorewall-lite
%attr(0700,root,root) %dir /var/lib/shorewall-lite

%attr(0755,root,root) %dir /etc/sysconfig/
%attr(0600,root,root) %config(noreplace) /etc/sysconfig/shorewall-lite

%attr(0644,root,root) /etc/logrotate.d/shorewall-lite

%attr(0755,root,root) %{_sbindir}/shorewall-lite

%attr(0644,root,root) /usr/share/shorewall-lite/version
%attr(0644,root,root) /usr/share/shorewall-lite/configpath
%attr(-   ,root,root) /usr/share/shorewall-lite/functions
%attr(0644,root,root) /usr/share/shorewall-lite/lib.base
%attr(0644,root,root) /usr/share/shorewall-lite/modules*
%attr(0644,root,root) /usr/share/shorewall-lite/helpers
%attr(0544,root,root) %{_libexecdir}/shorewall-lite/shorecap

%attr(0644,root,root) %{_mandir}/man5/shorewall-lite.conf.5.gz
%attr(0644,root,root) %{_mandir}/man5/shorewall-lite-vardir.5.gz

%attr(0644,root,root) %{_mandir}/man8/shorewall-lite.8.gz

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
