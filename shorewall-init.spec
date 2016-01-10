%define name shorewall-init
%define version 5.0.3
%define release 1

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
* Sat Jan 02 2016 Tom Eastep tom@shorewall.net
- Updated to 5.0.3-1
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
* Mon Jul 13 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.12-0Beta2
* Wed Jul 08 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.12-0Beta1
* Fri Jul 03 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.11-0base
* Mon Jun 29 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.11-0RC1
* Fri Jun 26 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.11-0Beta3
* Mon Jun 22 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.11-0Beta2
* Sun May 31 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.11-0Beta1
* Fri May 29 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.10-0base
* Mon May 25 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.10-0RC1
* Sun May 17 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.10-0Beta2
* Tue May 05 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.10-0Beta1
* Tue May 05 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.9-0base
* Tue May 05 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.9-0RC2
* Mon Apr 27 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.9-0RC1
* Fri Apr 17 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.9-0Beta3
* Mon Apr 06 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.9-0Beta2
* Fri Apr 03 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.9-0Beta1
* Sun Mar 29 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.8-0base
* Tue Mar 24 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.8-0RC1
* Tue Mar 17 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.8-0Beta3
* Sat Mar 14 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.8-0Beta2
* Fri Mar 06 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.8-0Beta1
* Thu Mar 05 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.7-0base
* Tue Mar 03 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.7-0RC1
* Sat Jan 17 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.7-0Beta1
* Sat Jan 10 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.6-0base
* Tue Jan 06 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.6-0RC1
* Fri Jan 02 2015 Tom Eastep tom@shorewall.net
- Updated to 4.6.6-0Beta3
* Fri Dec 26 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.6-0Beta2
* Fri Dec 19 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.6-0Beta1
* Mon Dec 15 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.5-3
* Sat Nov 15 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.5-2
* Fri Nov 14 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.5-1
* Thu Nov 06 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.5-0base
* Sat Nov 01 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.5-0RC1
* Thu Oct 30 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.5-0Beta3
* Mon Oct 20 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.5-0Beta2
* Wed Oct 08 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.5-0Beta1
* Mon Oct 06 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.4-0base
* Thu Oct 02 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.4-0RC1
* Sun Sep 28 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.4-0Beta3
* Wed Sep 24 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.4-0Beta2
* Sun Aug 24 2014 Tom Eastep tom@shorewall.net
- Updated to 4.6.4-0Beta1
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
* Wed May 18 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.20-0Beta3
* Wed May 18 2011 Tom Eastep tom@shorewall.net
- Updated to 4.4.20-0Beta2
* Sat Apr 16 2011 Tom Eastep tom@shorewall.net
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
* Tue May 18 2010 Tom Eastep tom@shorewall.net
- Initial version



