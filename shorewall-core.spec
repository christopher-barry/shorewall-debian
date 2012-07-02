%define name shorewall-core
%define version 4.5.5
%define release 3

Summary: Shoreline Firewall is an iptables-based firewall for Linux systems.
Name: %{name}
Version: %{version}
Release: %{release}
License: GPLv2
Packager: Tom Eastep <teastep@shorewall.net>
Group: Networking/Utilities
Source: %{name}-%{version}.tgz
URL: http://www.shorewall.net/
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-root1
Requires: iptables iproute perl
Provides: shoreline_firewall = %{version}-%{release}

%description

The Shoreline Firewall, more commonly known as "Shorewall", is a Netfilter
(iptables) based firewall that can be used on a dedicated firewall system,
a multi-function gateway/ router/server or on a standalone GNU/Linux system.
%prep

%setup

%build

%install

./configure.pl --host=%{_vendor} \
               --prefix=%{_prefix} \
               --tmpdir=%{_tmpdir} \
               --perllibdir=%{perl_vendorlib} \
               --libexecdir=%{_libexecdir}

DESTDIR=%{buildroot} ./install.sh

%clean

rm -rf $RPM_BUILD_ROOT

%post

[ -f ~/.shorewallrc ] || cp /usr/share/shorewall/shorewallrc ~/.shorewallrc

%preun

%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) %dir /usr/share/shorewall

%attr(0644,root,root) /usr/share/shorewall/coreversion
%attr(-   ,root,root) /usr/share/shorewall/functions
%attr(0644,root,root) /usr/share/shorewall/lib.base
%attr(0644,root,root) /usr/share/shorewall/lib.cli
%attr(0644,root,root) /usr/share/shorewall/lib.common
%attr(0644,root,root) /usr/share/shorewall/shorewallrc
%attr(0755,root,root) /usr/lib/shorewall/wait4ifup

%doc COPYING INSTALL changelog.txt releasenotes.txt

%changelog
* Thu Jun 28 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.5-3
* Fri Jun 22 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.5-2
* Tue Jun 12 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.5-1
* Sat Jun 09 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.6-0Beta1
* Wed Jun 06 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.5-0base
* Tue Jun 05 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.5-0RC1
* Sat Jun 02 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.5-0Beta2
* Thu May 24 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.5-0Beta1
* Thu May 24 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.4-0base
* Tue May 22 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.4-0RC2
* Fri May 18 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.4-0RC1
* Thu May 17 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.4-0Beta3
* Tue May 15 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.4-0Beta2
* Sun May 13 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.4-0Beta2
* Thu May 10 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.4-0Beta1
* Sun May 06 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.3-0base
* Thu May 03 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.3-0RC1
* Fri Apr 27 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.3-0Beta2
* Tue Apr 10 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.2-1
* Sat Apr 07 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.2-0base
* Wed Apr 04 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.2-0RC2
* Sun Apr 01 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.2-0RC1
* Thu Mar 29 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.2-0Beta5
* Mon Mar 26 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.2-0Beta4
* Tue Mar 20 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.2-0Beta3
- Added /usr/share/shorewall/shorewallrc
* Sat Mar 17 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.2-0Beta2
* Wed Mar 14 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.2-0Beta1
* Sat Mar 10 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.1-0base
* Sat Mar 03 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.1-0RC1
* Thu Feb 23 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.1-0Beta3
* Sun Feb 19 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.1-0Beta2
* Fri Feb 03 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.1-0Beta1
* Wed Jan 18 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.0-0RC1
* Sun Jan 15 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.0-0Beta4
* Thu Jan 05 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.0-0Beta3
* Mon Jan 02 2012 Tom Eastep tom@shorewall.net
- Version to 4.5.0-0Beta2
* Sun Jan 01 2012 Tom Eastep tom@shorewall.net
- Created in 4.5.0-0Beta1


