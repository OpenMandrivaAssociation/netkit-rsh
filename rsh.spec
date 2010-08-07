Summary:	Clients for remote access commands (rsh, rlogin, rcp)
Name:		rsh
Version:	0.17
Release:	%mkrel 26
License:	BSD
Group:		Networking/Remote access
URL:		ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/
Source0:	ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-rsh-%{version}.tar.gz
Source1:	rexec.pam
Source2:	rlogin.pam
Source3:	rsh.pam
Source4:	http://www.tc.cornell.edu/~sadd/rexec-1.5.tar.gz
Source5:	rsh-xinetd
Source6:	rlogin-xinetd
Source7:	rexec-xinetd
Patch1:		netkit-rsh-0.17-sectty.patch
Patch2:		netkit-rsh-0.17-rexec.patch
Patch3:		netkit-rsh-0.10-stdarg.patch
Patch4:		netkit-rsh-0.16-jbj.patch
Patch8:		netkit-rsh-0.16-jbj4.patch
Patch9:		netkit-rsh-0.16-prompt.patch
Patch10:	netkit-rsh-0.16-rlogin=rsh.patch
Patch11:	netkit-rsh-0.16-nokrb.patch
Patch12:	netkit-rsh-0.17-pre20000412-jbj5.patch
Patch13:	netkit-rsh-0.17-userandhost.patch
Patch14:	netkit-rsh-0.17-strip.patch
Patch15:	netkit-rsh-0.17-lfs.patch
Patch16:	netkit-rsh-0.17-chdir.patch
Patch17:	netkit-rsh-0.17-pam-nologin.patch
Patch19:	netkit-rsh-0.17-rexec-netrc.patch
Patch20:	netkit-rsh-0.17-pam-sess.patch
Patch21:	netkit-rsh-0.17-errno.patch
Patch22:	netkit-rsh-0.17-rexec-sig.patch
Patch23:	netkit-rsh-0.17-nohost.patch
Patch24:	netkit-rsh-0.17-ignchld.patch
Patch25:	netkit-rsh-0.17-checkdir.patch
Patch26:	netkit-rsh-0.17-pam-conv.patch
Patch27:	netkit-rsh-0.17-rcp-largefile.patch
Patch28:	netkit-rsh-0.17-pam-rhost.patch
Patch29:	netkit-rsh-0.17-rlogin-linefeed.patch
Patch30:	netkit-rsh-0.17-ipv6.patch
Patch31:	netkit-rsh-0.17-pam_env.patch
Patch33:	netkit-rsh-0.17-dns.patch
Patch34:	netkit-rsh-0.17-nohostcheck-compat.patch
Patch35:	netkit-rsh-0.17-audit.patch
Patch36:	netkit-rsh-0.17-longname.patch
Patch37:	netkit-rsh-0.17-arg_max.patch
# (ahmad) check return value from close to catch errors on NFS filesystems
# https://bugzilla.redhat.com/show_bug.cgi?id=461903
Patch38:	netkit-rsh-0.17-rh461903.patch
# (ahmad) add check for return values
# https://bugzilla.redhat.com/show_bug.cgi?id=473492
Patch39:	netkit-rsh-0.17-rh473492.patch
BuildRequires:	libtermcap-devel
BuildRequires:	pam-devel
BuildRequires:	audit-libs-devel >= 1.5
Conflicts:	krb5-appl-clients
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The rsh package contains a set of programs which allow users to run commmands
on remote machines, login to other machines and copy files between machines
(rsh, rlogin and rcp). All three of these commands use rhosts style
authentication.  This package contains the clients needed for all of these
services. The rsh package should be installed to enable remote access to other
machines.

%package	server
Summary:	Servers for remote access commands (rsh, rlogin, rcp)
Group:		System/Servers
Requires:	pam >= 0.59
Requires:	xinetd

%description	server
The rsh-server package contains a set of programs which allow users to run
commmands on remote machines, login to other machines and copy files between
machines (rsh, rlogin and rcp). All three of these commands use rhosts style
authentication. This package contains the servers needed for all of these
services. It also contains a server for rexec, an alternate method of executing
remote commands. All of these servers are run by xinetd and configured using
/etc/xinetd.d/ and PAM.  All the server is disabled by default.

%prep

%setup -q -n netkit-rsh-%{version} -a 4

%patch1 -p1 -b .sectty
%patch2 -p1 -b .rexec
%patch3 -p1 -b .stdarg
%patch4 -p1 -b .jbj
%patch8 -p1 -b .jbj4
%patch9 -p1 -b .prompt
%patch10 -p1 -b .rsh
%patch11 -p1 -b .rsh.nokrb
%patch12 -p1 -b .jbj5
%patch13 -p1 -b .userandhost
%patch14 -p1 -b .strip
%patch15 -p1 -b .lfs
%patch16 -p1 -b .chdir
%patch17 -p1 -b .pam-nologin
%patch19 -p1 -b .rexec-netrc
%patch20 -p1 -b .pam-sess
%patch21 -p1 -b .errno
%patch22 -p1 -b .rexec-sig
%patch23 -p1 -b .nohost
%patch24 -p1 -b .ignchld
%patch25 -p1 -b .checkdir
%patch26 -p1 -b .pam-conv
%patch27 -p1 -b .largefile
%patch28 -p1 -b .pam-rhost
%patch29 -p1 -b .linefeed
%patch30 -p1 -b .ipv6
%patch31 -p1 -b .pam_env
%patch33 -p1 -b .dns
%patch34 -p1 -b .compat
%patch35 -p1 -b .audit
%patch36 -p1 -b .longname
%patch37 -p1 -b .arg_max
%patch38 -p1 -b .rh461903
%patch39 -p1 -b .rh473492

# No, I don't know what this is doing in the tarball.
rm -f rexec/rexec

%build
sh configure
%{__perl} -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS) -fpic -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -D_GNU_SOURCE,;
    s,^LDFLAGS=,LDFLAGS=-pie,;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/xinetd.d
install -d %{buildroot}%{_sysconfdir}/pam.d
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/{man1,man5,man8}

make INSTALLROOT=%{buildroot} MANDIR=%{_mandir} install

install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/rexec
install -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/rlogin
install -m0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/rsh

make INSTALLROOT=%{buildroot} MANDIR=%{_mandir} install -C rexec

install -m0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/xinetd.d/rsh
install -m0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/xinetd.d/rlogin
install -m0644 %{SOURCE7} %{buildroot}%{_sysconfdir}/xinetd.d/rexec

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/rexec
%attr(4755,root,root) %{_bindir}/rcp
%attr(4755,root,root) %{_bindir}/rlogin
%attr(4755,root,root) %{_bindir}/rsh
%{_mandir}/man1/*.1*

%files server
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/xinetd.d/*
%config(noreplace) %{_sysconfdir}/pam.d/*
%{_mandir}/man8/*.8*
%{_sbindir}/in.*
