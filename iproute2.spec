#
# TODO:
# - fix build @ uClibc
# - fix iface_descr patch
#
# Conditional build
%bcond_without	doc		# don't build documentation
%bcond_without	tc		# don't build tc program (it breaks static linkage)
%bcond_without	atm		# disable ATM support for tc
%bcond_with	uClibc		# do some hacks to build with uClibc
%bcond_with	iface_descr	# build with interface description support

Summary:	Advanced IP routing and network device configuration tools
Summary(es.UTF-8):	Herramientas para encaminamiento avanzado y configuración de interfaces de red
Summary(pl.UTF-8):	Narzędzie do konfigurowania sieci
Summary(pt_BR.UTF-8):	Ferramentas para roteamento avançado e configuração de interfaces de rede
Name:		iproute2
Version:	4.2.0
Release:	1
License:	GPL v2+
Group:		Networking/Admin
Source0:	https://www.kernel.org/pub/linux/utils/net/iproute2/%{name}-%{version}.tar.xz
# Source0-md5:	51c54cc3245eff451154938fbc0f64f5
Source1:	%{name}.tmpfiles
Patch0:		%{name}-arp.patch
Patch1:		%{name}-iptables.patch
Patch2:		%{name}-iptables64.patch
Patch3:		%{name}-LDFLAGS.patch
Patch4:		fix-bashisms.patch
Patch5:		%{name}-build.patch
# extensions
Patch10:	%{name}-2.2.4-wrr.patch
Patch11:	esfq-%{name}.patch
Patch12:	001-net-dev-iface-descr-0.1.diff
Patch13:	%{name}-q_atm_c.patch
Patch14:	%{name}-q_srr.v0.4.patch
Patch15:	%{name}-ip_route_get.patch
URL:		http://www.linuxfoundation.org/collaborate/workgroups/networking/iproute2
BuildRequires:	bison
BuildRequires:	db-devel
BuildRequires:	flex
BuildRequires:	iptables-devel >= 0:1.4.5
# for netlink/* headers used in ip
BuildRequires:	libnl1-devel
%if %{with atm}
BuildRequires:	linux-atm-devel
%endif
BuildRequires:	linux-libc-headers >= 7:2.6.12.0-15
%if %{with doc}
BuildRequires:	psutils
BuildRequires:	sgml-tools
BuildRequires:	texlive-dvips
BuildRequires:	texlive-fonts-cmsuper
BuildRequires:	texlive-fonts-jknappen
BuildRequires:	texlive-latex
BuildRequires:	texlive-tex-babel
%endif
Requires:	iptables-libs >= 0:1.4.5
Obsoletes:	ifstat
Obsoletes:	iproute
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_sysconfdir	/etc/iproute2

%description
The iproute package contains networking utilities (ip, tc and rtmon,
for example) which are designed to use the advanced networking
capabilities of the Linux 2.4.x and 2.6.x kernel.

%description -l es.UTF-8
Linux mantiene compatibilidad con los utilitarios estándares de
configuración de la red, pero se necesitan nuevos utilitarios para
usar los recursos y características del nuevo núcleo. Este paquete
incluye los nuevos utilitarios.

%description -l pl.UTF-8
Ten pakiet zawiera programy (m.in. ip, tc, rtmon) pozwalające na
kontrolę routingu i innych aspektów dotyczących sieci z wykorzystaniem
zaawansowanych możliwości jąder Linuksa 2.4.x i 2.6.x.

%description -l pt_BR.UTF-8
O Linux mantém compatibilidade com os utilitários padrão de
configuração da rede, mas novos utilitários são necessários para fazer
uso das características e recursos da nova kernel. This package
includes the new utilities.

%package -n libnetlink-devel
Summary:	Library for the netlink interface
Summary(pl.UTF-8):	Biblioteka do interfejsu netlink
Group:		Development/Libraries

%description -n libnetlink-devel
This library provides an interface for kernel-user netlink interface.

%description -n libnetlink-devel -l pl.UTF-8
Ta biblioteka udostępnia interfejs do interfejsu netlink między jądrem
a przestrzenią użytkownika.

%package doc
Summary:	ip and tc documentation with examples
Summary(pl.UTF-8):	Dokumentacja do ip i tc z przykładami
License:	GPL v2+
Group:		Applications/System

%description doc
The iproute documentation contains howtos and examples of settings.

%description doc -l pl.UTF-8
Dokumentacja do iproute zawiera "howto" oraz przykłady ustawień.

%prep
%setup -q

# conflict with atm-vbr patched linux-libc-headers
%{__rm} include/linux/atm.h
#%{__rm} -r include/linux

%patch0 -p1
%if "%{_lib}" == "lib64"
%patch2 -p1
%else
%patch1 -p1
%endif
%patch3 -p1
%patch4 -p1
%patch5 -p1
# extensions:
%patch10 -p1
%patch11 -p1
%{?with_iface_descr:%patch12 -p1}
%patch13 -p0
%patch14 -p1
%patch15 -p1

%build
%{__make} \
%if %{with uClibc}
	CC="%{_target_cpu}-uclibc-gcc" \
	LD="%{_target_cpu}-uclibc-gcc" \
%else
	CC="%{__cc}" \
	LD="%{__cc}" \
%endif
	HOSTCC="%{__cc}" \
	CCOPTS="%{rpmcflags} %{rpmcppflags} -Wno-unused-result" \
	LDFLAGS="%{rpmldflags} -Wl,-export-dynamic" \
	LIBDIR=%{_libdir} \
	%{!?with_tc:SUBDIRS="lib ip misc"}

%{?with_doc:%{__make} -C doc}

# make sure we don't produce broken ip binary
./ip/ip link add type vlan help 2>&1 | grep -q "VLANID :=" || exit 1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},/var/run/netns,%{systemdtmpfilesdir}}

%{__make} install \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

# omitted by make install
install -Dp man/man7/tc-hfsc.7 $RPM_BUILD_ROOT%{_mandir}/man7/tc-hfsc.7

# arpd is not packaged here
%{__rm} $RPM_BUILD_ROOT%{_sbindir}/arpd $RPM_BUILD_ROOT%{_mandir}/man8/arpd.8

cp -p lib/libnetlink.a $RPM_BUILD_ROOT%{_libdir}
cp -p include/libnetlink.h $RPM_BUILD_ROOT%{_includedir}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%if %{with doc}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%endif

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/iproute2

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README README.decnet README.iproute2+tc README.distribution README.lnstat
%attr(755,root,root) %{_sbindir}/bridge
%attr(755,root,root) %{_sbindir}/ctstat
%attr(755,root,root) %{_sbindir}/genl
%attr(755,root,root) %{_sbindir}/ifcfg
%attr(755,root,root) %{_sbindir}/ifstat
%attr(755,root,root) %{_sbindir}/ip
%attr(755,root,root) %{_sbindir}/lnstat
%attr(755,root,root) %{_sbindir}/nstat
%attr(755,root,root) %{_sbindir}/routef
%attr(755,root,root) %{_sbindir}/routel
%attr(755,root,root) %{_sbindir}/rtacct
%attr(755,root,root) %{_sbindir}/rtmon
%attr(755,root,root) %{_sbindir}/rtpr
%attr(755,root,root) %{_sbindir}/rtstat
%attr(755,root,root) %{_sbindir}/ss
%attr(755,root,root) %{_sbindir}/tipc
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ematch_map
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/group
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nl_protos
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rt_dsfield
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rt_protos
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rt_realms
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rt_scopes
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rt_tables
%{_mandir}/man8/bridge.8*
%{_mandir}/man8/ip.8*
%{_mandir}/man8/ip-*.8*
%{_mandir}/man8/ctstat.8*
%{_mandir}/man8/lnstat.8*
%{_mandir}/man8/nstat.8*
%{_mandir}/man8/routef.8*
%{_mandir}/man8/routel.8*
%{_mandir}/man8/rtacct.8*
%{_mandir}/man8/rtmon.8*
%{_mandir}/man8/rtstat.8*
%{_mandir}/man8/ss.8*
%if %{with tc}
%attr(755,root,root) %{_sbindir}/tc
%dir %{_libdir}/tc
%attr(755,root,root) %{_libdir}/tc/*.so
%{_libdir}/tc/*.dist
%{_mandir}/man7/tc-hfsc.7*
%{_mandir}/man8/tc.8*
%{_mandir}/man8/tc-*.8*
%endif
%{systemdtmpfilesdir}/%{name}.conf
%dir %attr(750,root,root) /var/run/netns

%files -n libnetlink-devel
%defattr(644,root,root,755)
%{_libdir}/libnetlink.a
%{_includedir}/libnetlink.h
%{_mandir}/man3/libnetlink.3*

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc doc/*.ps
%{_examplesdir}/%{name}-%{version}
%endif
