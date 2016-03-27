%define name shorewall
%define version 5.0.7
%define release 0base

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
Requires: iptables iproute perl shorewall-core perl-Digest-SHA1
Provides: shoreline_firewall = %{version}-%{release}
Obsoletes: shorewall-common shorewall-perl shorewall-shell

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
rm -rf %{buildroot}

%post

if [ $1 -eq 1 ]; then
	if [ -x /usr%{_sbindir}/insserv ]; then
		/usr%{_sbindir}/insserv %{_initddir}/shorewall
	elif [ -x /usr%{_sbindir}/chkconfig ]; then
		%{_sbindir}/chkconfig --add shorewall;
	fi
fi

%preun

if [ $1 = 0 ]; then
	if [ -x %{_sbindir}/insserv ]; then
		%{_sbindir}/insserv -r %{_initddir}/shorewall
	elif [ -x %{_sbindir}/chkconfig ]; then
		%{_sbindir}/chkconfig --del shorewall
	fi

	rm -f /etc/shorewall/startup_disabled

fi

%triggerpostun  -- shorewall-common < 4.4.0

if [ -x %{_sbindir}/insserv ]; then
    %{_sbindir}/insserv /etc/rc.d/shorewall
elif [ -x %{_sbindir}/chkconfig ]; then
    %{_sbindir}/chkconfig --add shorewall;
fi

%files
%defattr(0644,root,root,0755)
%attr(0544,root,root) %{_initddir}/shorewall
%attr(0755,root,root) %dir /etc/shorewall
%ghost %attr(0644,root,root) /etc/shorewall/isusable
%ghost %attr(0644,root,root) /etc/shorewall/notrack
%attr(0755,root,root) %dir /usr/share/shorewall/configfiles
%attr(0700,root,root) %dir /var/lib/shorewall
%attr(0600,root,root) %config(noreplace) /etc/shorewall/*

%attr(0755,root,root) %dir /etc/sysconfig/
%attr(0600,root,root) %config(noreplace) /etc/sysconfig/shorewall

%attr(0644,root,root) /etc/logrotate.d/shorewall

%attr(0755,root,root) %{_sbindir}/shorewall

%attr(0644,root,root) /usr/share/shorewall/version
%attr(0644,root,root) /usr/share/shorewall/actions.std
%attr(0644,root,root) /usr/share/shorewall/action.Broadcast
%attr(0644,root,root) /usr/share/shorewall/action.DNSAmp
%attr(0644,root,root) /usr/share/shorewall/action.Drop
%attr(0644,root,root) /usr/share/shorewall/action.DropSmurfs
%attr(0644,root,root) /usr/share/shorewall/action.A_Drop
%attr(0644,root,root) /usr/share/shorewall/action.AutoBL
%attr(0644,root,root) /usr/share/shorewall/action.AutoBLL
%attr(0644,root,root) /usr/share/shorewall/action.Established
%attr(0644,root,root) /usr/share/shorewall/action.GlusterFS
%attr(0644,root,root) /usr/share/shorewall/action.IfEvent
%attr(0644,root,root) /usr/share/shorewall/action.Invalid
%attr(0644,root,root) /usr/share/shorewall/action.New
%attr(0644,root,root) /usr/share/shorewall/action.NotSyn
%attr(0644,root,root) /usr/share/shorewall/action.RST
%attr(0644,root,root) /usr/share/shorewall/action.Reject
%attr(0644,root,root) /usr/share/shorewall/action.Related
%attr(0644,root,root) /usr/share/shorewall/action.A_Reject
%attr(0644,root,root) /usr/share/shorewall/action.ResetEvent
%attr(0644,root,root) /usr/share/shorewall/action.SetEvent
%attr(0644,root,root) /usr/share/shorewall/action.TCPFlags
%attr(0644,root,root) /usr/share/shorewall/action.allowInvalid
%attr(0644,root,root) /usr/share/shorewall/action.dropInvalid
%attr(0644,root,root) /usr/share/shorewall/action.mangletemplate
%attr(0644,root,root) /usr/share/shorewall/action.template
%attr(0644,root,root) /usr/share/shorewall/action.Untracked
%attr(0644,root,root) /usr/share/shorewall/lib.cli-std
%attr(0644,root,root) /usr/share/shorewall/lib.core
%attr(0644,root,root) /usr/share/shorewall/macro.*
%attr(0644,root,root) /usr/share/shorewall/modules*
%attr(0644,root,root) /usr/share/shorewall/helpers
%attr(0644,root,root) /usr/share/shorewall/configpath

%attr(755,root,root) %{_libexecdir}/shorewall/compiler.pl
%attr(755,root,root) %{_libexecdir}/shorewall/getparams
%attr(0644,root,root) /usr/share/shorewall/prog.*
%attr(0644,root,root) %{perl_vendorlib}/Shorewall/*.pm

%attr(0644,root,root) /usr/share/shorewall/configfiles/*

%attr(0644,root,root) %{_mandir}/man5/*
%attr(0644,root,root) %{_mandir}/man8/*

%doc COPYING INSTALL changelog.txt releasenotes.txt Contrib/* Samples

%changelog
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
