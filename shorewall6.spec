%define name shorewall6
%define version 4.5.21
%define release 0base

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
               --libexecdir=%{_libexecdir}

DESTDIR=%{buildroot} ./install.sh

touch %{buildroot}/etc/shorewall6/isusable
touch %{buildroot}/etc/shorewall6/notrack

%clean
rm -rf $RPM_BUILD_ROOT

%post

if [ $1 -eq 1 ]; then
	if [ -x /sbin/insserv ]; then
		/sbin/insserv /etc/rc.d/shorewall6
	elif [ -x /sbin/chkconfig ]; then
		/sbin/chkconfig --add shorewall6;
	fi
fi

%preun

if [ $1 = 0 ]; then
	if [ -x /sbin/insserv ]; then
		/sbin/insserv -r %{_initddir}/shorewall6
	elif [ -x /sbin/chkconfig ]; then
		/sbin/chkconfig --del shorewall6
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
%attr(0644,root,root) %config(noreplace) /etc/shorewall6/*

%attr(0600,root,root) /etc/shorewall6/Makefile

%attr(0644,root,root) /etc/logrotate.d/shorewall6

%attr(0755,root,root) /sbin/shorewall6

%attr(0644,root,root) /usr/share/shorewall6/version
%attr(0644,root,root) /usr/share/shorewall6/actions.std
%attr(0644,root,root) /usr/share/shorewall6/action.AllowICMPs
%attr(0644,root,root) /usr/share/shorewall6/action.A_AllowICMPs
%attr(0644,root,root) /usr/share/shorewall6/action.Broadcast
%attr(0644,root,root) /usr/share/shorewall6/action.Drop
%attr(0644,root,root) /usr/share/shorewall6/action.A_Drop
%attr(0644,root,root) /usr/share/shorewall6/action.Reject
%attr(0644,root,root) /usr/share/shorewall6/action.A_Reject
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
* Thu Dec 13 2012 Tom Eastep tom@shorewall.net
- Updated to 4.4.11-0Beta3
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
* Sun Jul 29 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.7-0RC1
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
- Updated to 4.5.0-0Beta2
* Sun Jan 01 2012 Tom Eastep tom@shorewall.net
- Updated to 4.5.0-0Beta1
* Sun Dec 25 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.27-0base
* Fri Dec 23 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.27-0RC2
* Sat Dec 17 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.27-0RC1
* Sun Dec 11 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.27-0Beta3
* Mon Dec 05 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.27-0Beta2
* Sat Dec 03 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.27-0Beta1
* Sat Dec 03 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.26-1
* Tue Nov 29 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.26-0base
* Sun Nov 20 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.26-0RC1
* Sat Nov 19 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.26-0Beta4
* Thu Nov 17 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.26-0Beta3
* Sat Nov 12 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.26-0Beta2
* Wed Nov 02 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.26-0Beta1
* Sun Oct 30 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.25-1
* Thu Oct 27 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.25-0base
* Sun Oct 23 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.25-0RC1
* Sat Oct 22 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.25-0Beta4
* Tue Oct 18 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.25-0Beta3
* Tue Oct 11 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.25-0Beta2
* Tue Oct 04 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.25-0Beta1
* Sat Oct 01 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.24-0RC1
* Mon Sep 26 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.24-0Beta4
* Wed Sep 21 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.24-0Beta3
* Sun Sep 18 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.24-0Beta2
* Thu Sep 15 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.24-0Beta1
* Tue Sep 13 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.23-3
* Fri Sep 09 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.23-2
* Wed Sep 07 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.23-1
* Sat Sep 03 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.23-0base
* Fri Sep 02 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.23-0RC2
* Mon Aug 29 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.23-0RC1
* Sat Aug 27 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.23-0Beta4
* Sun Aug 21 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.23-0Beta3
* Wed Aug 17 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.23-0Beta2
* Fri Aug 05 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.23-0Beta1
* Wed Aug 03 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.22-2
* Tue Aug 02 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.22-1
* Sat Jul 30 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.22-0base
* Sat Jul 30 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.22-0RC2
* Fri Jul 22 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.22-0RC1
* Thu Jul 21 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.22-0Beta3
* Mon Jul 18 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.22-0Beta2
* Mon Jul 04 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.22-0Beta1
* Wed Jun 29 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.21-0base
* Thu Jun 23 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.21-0RC1
* Sun Jun 19 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.21-0Beta3
* Sat Jun 18 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.21-0Beta2
* Tue Jun 07 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.21-0Beta1
* Mon Jun 06 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.20-1
* Tue May 31 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.20-0base
* Fri May 27 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.20-0RC1
* Tue May 24 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.20-0Beta5
* Sun May 22 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.20-0Beta4
* Thu May 19 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.20-0Beta3
* Wed May 18 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.20-0Beta2
* Sat Apr 16 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.20-0Beta1
* Wed Apr 13 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.19-1
* Sat Apr 09 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.19-0base
* Sun Apr 03 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.19-0RC1
* Sun Apr 03 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.19-0Beta5
* Sat Apr 02 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.19-0Beta4
* Sat Mar 26 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.19-0Beta3
* Sat Mar 05 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.19-0Beta1
* Wed Mar 02 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.18-0base
* Mon Feb 28 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.18-0RC1
* Sun Feb 20 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.18-0Beta4
* Sat Feb 19 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.18-0Beta3
* Sun Feb 13 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.18-0Beta2
* Sat Feb 05 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.18-0Beta1
* Fri Feb 04 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.17-0base
* Sun Jan 30 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.17-0RC1
* Fri Jan 28 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.17-0Beta3
* Wed Jan 19 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.17-0Beta2
* Sat Jan 08 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.17-0Beta1
* Mon Jan 03 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.16-0base
* Thu Dec 30 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.16-0RC1
* Thu Dec 30 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.16-0Beta8
* Sun Dec 26 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.16-0Beta7
* Mon Dec 20 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.16-0Beta6
* Fri Dec 10 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.16-0Beta5
* Sat Dec 04 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.16-0Beta4
* Fri Dec 03 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.16-0Beta3
* Fri Dec 03 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.16-0Beta2
* Tue Nov 30 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.16-0Beta1
* Fri Nov 26 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.15-0base
* Mon Nov 22 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.15-0RC1
* Mon Nov 15 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.15-0Beta2
* Sat Oct 30 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.15-0Beta1
* Sat Oct 23 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.14-0base
* Wed Oct 06 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.14-0RC1
* Fri Oct 01 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.14-0Beta4
* Sun Sep 26 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.14-0Beta3
* Thu Sep 23 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.14-0Beta2
* Tue Sep 21 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.14-0Beta1
* Fri Sep 17 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.13-0RC1
* Fri Sep 17 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.13-0Beta6
* Mon Sep 13 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.13-0Beta5
* Sat Sep 04 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.13-0Beta4
* Mon Aug 30 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.13-0Beta3
* Wed Aug 25 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.13-0Beta2
* Wed Aug 18 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.13-0Beta1
* Sun Aug 15 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.12-0base
* Fri Aug 06 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.12-0RC1
* Sun Aug 01 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.12-0Beta4
* Sat Jul 31 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.12-0Beta3
* Sun Jul 25 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.12-0Beta2
* Wed Jul 21 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.12-0Beta1
* Fri Jul 09 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.11-0base
* Mon Jul 05 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.11-0RC1
* Sat Jul 03 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.11-0Beta3
* Thu Jul 01 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.11-0Beta2
* Sun Jun 06 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.11-0Beta1
* Sat Jun 05 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.10-0base
* Fri Jun 04 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.10-0RC2
* Thu May 27 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.10-0RC1
* Wed May 26 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.10-0Beta4
* Tue May 25 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.10-0Beta3
* Thu May 20 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.10-0Beta2
* Thu May 20 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.10-0Beta2
* Thu May 13 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.10-0Beta1
* Mon May 03 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.9-0base
* Sun May 02 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.9-0RC2
* Sun Apr 25 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.9-0RC1
* Sat Apr 24 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.9-0Beta5
* Fri Apr 16 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.9-0Beta4
* Fri Apr 09 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.9-0Beta3
* Thu Apr 08 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.9-0Beta2
* Sat Mar 20 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.9-0Beta1
* Fri Mar 19 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.8-0base
* Tue Mar 16 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.8-0RC2
* Mon Mar 08 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.8-0RC1
* Sun Feb 28 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.8-0Beta2
* Thu Feb 11 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.8-0Beta1
* Fri Feb 05 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.7-0base
* Tue Feb 02 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.7-0RC2
* Wed Jan 27 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.7-0RC1
* Mon Jan 25 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.7-0Beta4
* Fri Jan 22 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.7-0Beta3
* Fri Jan 22 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.7-0Beta2
- Added helpers file
* Sun Jan 17 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.7-0Beta1
* Wed Jan 13 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.6-0base
* Tue Jan 12 2010 Tom Eastep tom@shorewall.net
- Updated to 4.4.6-0Beta1
* Thu Dec 24 2009 Tom Eastep tom@shorewall.net
- Updated to 4.4.5-0base
* Sat Nov 21 2009 Tom Eastep tom@shorewall.net
- Updated to 4.4.4-0base
* Fri Nov 13 2009 Tom Eastep tom@shorewall.net
- Updated to 4.4.4-0Beta2
* Wed Nov 11 2009 Tom Eastep tom@shorewall.net
- Updated to 4.4.4-0Beta1
* Fri Oct 02 2009 Tom Eastep tom@shorewall.net
- Updated to 4.4.3-0base
* Sun Sep 06 2009 Tom Eastep tom@shorewall.net
- Updated to 4.4.2-0base
* Fri Sep 04 2009 Tom Eastep tom@shorewall.net
- Updated to 4.4.2-0base
* Fri Aug 14 2009 Tom Eastep tom@shorewall.net
- Updated to 4.4.1-0base
* Mon Aug 03 2009 Tom Eastep tom@shorewall.net
- Updated to 4.4.0-0base
* Tue Jul 28 2009 Tom Eastep tom@shorewall.net
- Updated to 4.4.0-0RC2
* Sun Jul 12 2009 Tom Eastep tom@shorewall.net
- Updated to 4.4.0-0RC1
* Thu Jul 09 2009 Tom Eastep tom@shorewall.net
- Updated to 4.4.0-0Beta4
* Sat Jun 27 2009 Tom Eastep tom@shorewall.net
- Updated to 4.4.0-0Beta3
* Mon Jun 15 2009 Tom Eastep tom@shorewall.net
- Updated to 4.4.0-0Beta2
* Fri Jun 12 2009 Tom Eastep tom@shorewall.net
- Updated to 4.4.0-0Beta1
* Sun Jun 07 2009 Tom Eastep tom@shorewall.net
- Updated to 4.3.13-0base
* Fri Jun 05 2009 Tom Eastep tom@shorewall.net
- Updated to 4.3.12-0base
* Sun May 10 2009 Tom Eastep tom@shorewall.net
- Updated to 4.3.11-0base
* Sun Apr 19 2009 Tom Eastep tom@shorewall.net
- Updated to 4.3.10-0base
* Sat Apr 11 2009 Tom Eastep tom@shorewall.net
- Updated to 4.3.9-0base
* Tue Mar 17 2009 Tom Eastep tom@shorewall.net
- Updated to 4.3.8-0base
* Sun Mar 01 2009 Tom Eastep tom@shorewall.net
- Updated to 4.3.7-0base
* Fri Feb 27 2009 Tom Eastep tom@shorewall.net
- Updated to 4.3.6-0base
* Sun Feb 22 2009 Tom Eastep tom@shorewall.net
- Updated to 4.3.5-0base
* Sat Feb 21 2009 Tom Eastep tom@shorewall.net
- Updated to 4.2.7-0base
* Wed Feb 05 2009 Tom Eastep tom@shorewall.net
- Added 'restored' script
* Wed Feb 04 2009 Tom Eastep tom@shorewall.net
- Updated to 4.2.6-0base
* Thu Jan 29 2009 Tom Eastep tom@shorewall.net
- Updated to 4.2.6-0base
* Tue Jan 06 2009 Tom Eastep tom@shorewall.net
- Updated to 4.2.5-0base
* Thu Dec 25 2008 Tom Eastep tom@shorewall.net
- Updated to 4.2.4-0base
* Sun Dec 21 2008 Tom Eastep tom@shorewall.net
- Updated to 4.2.4-0RC2
* Wed Dec 17 2008 Tom Eastep tom@shorewall.net
- Updated to 4.2.4-0RC1
* Tue Dec 16 2008 Tom Eastep tom@shorewall.net
- Updated to 4.3.4-0base
* Sat Dec 13 2008 Tom Eastep tom@shorewall.net
- Updated to 4.3.3-0base
* Fri Dec 12 2008 Tom Eastep tom@shorewall.net
- Updated to 4.3.2-0base
* Thu Dec 11 2008 Tom Eastep tom@shorewall.net
- Updated to 4.3.1-0base
* Wed Dec 10 2008 Tom Eastep tom@shorewall.net
- Updated to 4.3.0-0base
* Wed Dec 10 2008 Tom Eastep tom@shorewall.net
- Updated to 2.3.0-0base
* Tue Dec 09 2008 Tom Eastep tom@shorewall6.net
- Initial Version