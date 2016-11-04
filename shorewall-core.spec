%define name shorewall-core
%define version 5.0.14
%define release 0RC3

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
               --libexecdir=%{_libexecdir} \
               --sbindir=%{_sbindir}

DESTDIR=%{buildroot} ./install.sh

%clean

rm -rf $RPM_BUILD_ROOT

%post

cp /usr/share/shorewall/shorewallrc ~/.shorewallrc

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
* Mon Oct 31 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.14-0RC3
* Sat Oct 29 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.14-0RC2
* Thu Oct 27 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.14-0RC1
* Tue Oct 25 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.14-0Beta2
* Sun Oct 16 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.14-0Beta1
* Sun Oct 16 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.13-0base
* Sun Oct 16 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.13-0RC2
* Sun Oct 09 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.13-0RC1
* Tue Oct 04 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.13-0Beta2
* Sun Oct 02 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.13-0Beta1
* Sat Oct 01 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.12-0base
* Sat Oct 01 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.12-0RC3
* Tue Sep 27 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.12-0RC2
* Tue Sep 20 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.12-0RC1
* Tue Sep 13 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.12-0Beta2
* Sat Aug 13 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.12-0Beta1
* Sat Aug 06 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.11-0base
* Sat Jul 30 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.11-0RC1
* Wed Jul 27 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.11-0Beta2
* Tue Jul 19 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.11-0Beta1
* Fri Jul 08 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.10-1
* Sat Jun 25 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.10-0base
* Tue Jun 21 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.10-0RC1
* Tue Jun 14 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.10-0Beta2
* Mon Jun 06 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.10-0Beta1
* Thu May 12 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.9-0base
* Thu May 05 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.9-0RC1
* Thu Apr 28 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.9-0Beta2
* Mon Apr 18 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.9-0Beta1
* Fri Apr 15 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.8-0RC2
* Mon Apr 11 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.8-0RC1
* Thu Apr 07 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.8-0Beta4
* Sat Apr 02 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.8-0Beta3
* Fri Apr 01 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.8-0Beta2
* Sun Mar 27 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.8-0Beta1
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
