%define name shorewall-core
%define version 4.6.3
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
* Wed Sep 10 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.3-3
* Sat Aug 30 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.3-2
* Thu Aug 21 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.3-1
* Thu Aug 14 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.3-0base
* Sun Aug 10 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.3-0RC1
* Sun Aug 03 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.3-0Beta2
* Fri Jul 25 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.3-0Beta1
* Fri Jul 18 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.2-2
* Fri Jul 18 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.2-1
* Sun Jul 13 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.2-0base
* Fri Jul 04 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.2-0RC1
* Wed Jul 02 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.2-0Beta2
* Wed Jun 18 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.2-0Beta1
* Sun Jun 08 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.1-1
* Wed Jun 04 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.1-0base
* Mon Jun 02 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.0-4
* Fri May 23 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.0-3
* Fri May 16 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.0-2
* Fri May 16 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.0-1
* Sat May 10 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.0-0base
* Wed May 07 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.0-0RC3
* Sun Apr 20 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.0-0RC2
* Sun Mar 23 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.0-0RC1
* Fri Mar 07 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.0-0Beta6
* Sat Feb 15 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.0-0Beta5
* Sat Feb 15 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.0-0Beta6
* Tue Feb 04 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.0-0Beta4
* Thu Jan 16 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.0-0Beta3
* Wed Jan 01 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.0-0Beta2
* Wed Nov 27 2013 Tom Eastep tom@shorewall.net
- Updated to 4.6.0-0Beta1
* Mon Nov 04 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.21-4
* Fri Oct 25 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.21-3
* Mon Oct 21 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.21-2
* Fri Oct 04 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.21-1
* Fri Sep 27 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.21-0base
* Thu Sep 19 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.21-0RC1
* Thu Sep 12 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.21-0Beta3
* Fri Sep 06 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.21-0Beta2
* Sun Sep 01 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.21-0Beta1
* Sun Aug 18 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.20-0base
* Sun Aug 11 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.20-0RC1
* Tue Aug 06 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.20-0Beta3
* Mon Jul 29 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.20-0Beta2
* Mon Jul 22 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.20-0Beta1
* Sun Jul 21 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.19-0base
* Mon Jul 15 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.19-0RC1
* Thu Jul 11 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.19-0Beta3
* Mon Jul 08 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.19-0Beta2
* Mon Jul 01 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.19-0Beta1
* Thu Jun 27 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.18-0base
* Mon Jun 24 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.18-0RC2
* Mon Jun 17 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.18-0RC1
* Tue Jun 11 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.18-0Beta3
* Tue Jun 04 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.18-0Beta2
* Thu May 30 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.18-0Beta1
* Mon May 27 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.17-0base
* Sun May 26 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.17-0RC2
* Wed May 22 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.17-0RC1
* Sun May 12 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.17-0Beta3
* Sat May 11 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.17-0Beta2
* Tue May 07 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.17-0Beta1
* Wed May 01 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.16-2
* Wed May 01 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.16-1
* Tue Apr 30 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.16-0base
* Fri Apr 26 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.16-0RC2
* Sat Apr 20 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.16-0RC1
* Sat Apr 20 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.16-0Beta6
* Wed Apr 17 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.16-0Beta5
* Mon Apr 15 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.16-0Beta4
* Thu Apr 11 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.16-0Beta3
* Fri Apr 05 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.16-0Beta2
* Fri Mar 29 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.16-0Beta1
* Thu Mar 28 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.15-0base
* Sun Mar 24 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.15-0RC1
* Fri Mar 22 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.15-0Beta3
* Sun Mar 17 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.15-0Beta2
* Tue Mar 05 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.15-0Beta1
* Sat Mar 02 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.14-0base
* Sat Feb 23 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.14-0RC1
* Sun Feb 17 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.14-0Beta3
* Wed Feb 13 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.14-0Beta2
* Tue Feb 12 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.14-0Beta1
* Fri Feb 08 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.13-0base
* Mon Feb 04 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.13-0RC3
* Sun Feb 03 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.13-0RC2
* Thu Jan 31 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.13-0RC1
* Tue Jan 29 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.13-0Beta4
* Mon Jan 21 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.13-0Beta3
* Sun Jan 20 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.13-0Beta2
* Tue Jan 15 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.13-0Beta1
* Tue Jan 15 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.12-0base
* Thu Jan 10 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.12-0RC1
* Tue Jan 08 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.12-0Beta5
* Sat Jan 05 2013 Tom Eastep tom@shorewall.net
- Updated to 4.5.12-0Beta4
* Mon Dec 31 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.12-0Beta3
* Thu Dec 27 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.12-0Beta2
* Wed Dec 26 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.12-0Beta1
* Wed Dec 19 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.11-0RC1
* Thu Dec 13 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.11-0Beta3
* Sun Dec 09 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.11-0Beta2
* Mon Dec 03 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.11-0Beta1
* Sun Dec 02 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.10-0base
* Wed Nov 28 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.10-0RC1
* Sat Nov 24 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.10-0Beta3
* Tue Nov 20 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.10-0Beta2
* Fri Nov 16 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.10-0Beta1
* Sun Nov 11 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.9-2
* Sat Nov 03 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.9-1
* Fri Oct 26 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.9-0base
* Sun Oct 21 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.9-0RC1
* Tue Oct 16 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.9-0Beta3
* Thu Oct 04 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.9-0Beta2
* Thu Sep 20 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.9-0Beta1
* Wed Sep 19 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.8-0base
* Thu Sep 13 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.8-0RC2
* Mon Sep 10 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.8-0RC1
* Tue Sep 04 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.8-0Beta3
* Mon Sep 03 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.8-0Beta2
* Thu Aug 09 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.8-0Beta1
* Tue Aug 07 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.7-0RC1
* Mon Aug 06 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.7-0Beta5
* Sun Aug 05 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.7-0Beta4
* Sat Aug 04 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.7-0Beta3
* Tue Jul 17 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.7-0Beta2
* Sun Jul 08 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.7-0Beta1
* Thu Jul 05 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.6-0base
* Sat Jun 30 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.6-0RC1
* Wed Jun 27 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.6-0Beta4
* Mon Jun 18 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.6-0Beta3
* Fri Jun 15 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.6-0Beta2
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


