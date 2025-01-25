#
# TODO:
# - fix build @ uClibc
# - fix iface_descr patch
#
# Conditional build
%bcond_without	tc		# don't build tc program (it breaks static linkage)
%bcond_with	uClibc		# do some hacks to build with uClibc
%bcond_with	iface_descr	# build with interface description support

Summary:	Advanced IP routing and network device configuration tools
Summary(es.UTF-8):	Herramientas para encaminamiento avanzado y configuración de interfaces de red
Summary(pl.UTF-8):	Narzędzie do konfigurowania sieci
Summary(pt_BR.UTF-8):	Ferramentas para roteamento avançado e configuração de interfaces de rede
Name:		iproute2
Version:	6.13.0
Release:	1
License:	GPL v2+
Group:		Networking/Admin
Source0:	https://www.kernel.org/pub/linux/utils/net/iproute2/%{name}-%{version}.tar.xz
# Source0-md5:	1603d25120d03feeaba9b360d03ffaec
Source1:	%{name}.tmpfiles
Patch3:		%{name}-LDFLAGS.patch

Patch5:		%{name}-build.patch
Patch6:		%{name}-print_cache_route_entries.patch
# extensions
Patch10:	%{name}-2.2.4-wrr.patch
Patch11:	esfq-%{name}.patch
Patch12:	001-net-dev-iface-descr-0.1.diff
Patch14:	%{name}-q_srr.v0.4.patch
Patch15:	%{name}-ip_route_get.patch
URL:		https://wiki.linuxfoundation.org/networking/iproute2
BuildRequires:	bison
BuildRequires:	db-devel
# libelf
BuildRequires:	elfutils-devel
BuildRequires:	flex
BuildRequires:	iptables-devel >= 0:1.4.5
BuildRequires:	libbpf-devel >= 0.1.0
BuildRequires:	libbsd-devel
BuildRequires:	libcap-devel
BuildRequires:	libmnl-devel
BuildRequires:	libselinux-devel
BuildRequires:	libtirpc-devel
BuildRequires:	linux-libc-headers >= 7:2.6.12.0-15
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Suggests:	%{name}-routel = %{version}-%{release}
Suggests:	%{name}-ss = %{version}-%{release}
Suggests:	%{name}-tc = %{version}-%{release}
Obsoletes:	ifstat < 1.2
Obsoletes:	iproute
Obsoletes:	iproute2-doc < 4.14.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_defaultconfdir	%{_datadir}/iproute2

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

%package routel
Summary:	routel - list routes with pretty output format
Requires:	%{name} = %{version}-%{release}
Requires:	python3
Requires:	python3-modules

%description routel
The routel script will list routes in a format that some might
consider easier to interpret then the ip route list equivalent.

%package ss
Summary:	ss - another utility to investigate sockets

%description ss
ss is used to dump socket statistics. It allows showing information
similar to netstat. It can display more TCP and state information than
other tools.

%package tc
Summary:	tc - show / manipulate traffic control settings
Requires:	iptables-libs >= 0:1.4.5

%description tc
Tc is used to configure Traffic Control in the Linux kernel.

%package devel
Summary:	Header file for tc plugins development
Summary(pl.UTF-8):	Plik nagłówkowy do tworzenia wtyczek programu tc
Group:		Development/Libraries
# doesn't require base

%description devel
Header file for tc plugins development.

%description devel -l pl.UTF-8
Plik nagłówkowy do tworzenia wtyczek programu tc.

%package -n libnetlink-devel
Summary:	Library for the netlink interface
Summary(pl.UTF-8):	Biblioteka do interfejsu netlink
Group:		Development/Libraries

%description -n libnetlink-devel
This library provides an interface for kernel-user netlink interface.

%description -n libnetlink-devel -l pl.UTF-8
Ta biblioteka udostępnia interfejs do interfejsu netlink między jądrem
a przestrzenią użytkownika.

%package -n bash-completion-iproute2
Summary:	Bash completion for iproute2 commands
Summary(pl.UTF-8):	Bashowe dopełnianie parametrów poleceń iproute2
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-iproute2
Bash completion for iproute2 commands (currently devlink and tc).

%description -n bash-completion-iproute2 -l pl.UTF-8
Bashowe dopełnianie parametrów poleceń iproute2 (obecnie devlink i
tc).

%prep
%setup -q

# conflict with atm-vbr patched linux-libc-headers
%{__rm} include/uapi/linux/atm.h

%patch3 -p1

%patch5 -p1
%patch6 -p1
# extensions:
%patch10 -p1
%patch11 -p1
%{?with_iface_descr:%patch12 -p1}
%patch14 -p1
%patch15 -p1

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' ip/routel

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
	CCOPTS="%{rpmcflags} %{rpmcppflags} -Wno-unused-result -DXT_LIB_DIR=\\\"%{_libdir}/xtables\\\"" \
	LDFLAGS="%{rpmldflags} -Wl,-export-dynamic" \
	LIBDIR=%{_libdir} \
	%{!?with_tc:SUBDIRS="lib ip misc"} \
	V=1

# make sure we don't produce broken ip binary
./ip/ip link add type vlan help 2>&1 | grep -q "VLANID :=" || exit 1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/iproute2/{protodown_reasons,rt_protos,rt_tables}.d \
	$RPM_BUILD_ROOT%{_defaultconfdir}/{protodown_reasons,rt_protos,rt_tables}.d \
	$RPM_BUILD_ROOT{%{_includedir},/var/run/netns,%{systemdtmpfilesdir}}

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

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- iproute2 < 6.6.0-2
for c in bpf_pinning ematch_map group nl_protos rt_dsfield rt_protos rt_realms rt_scopes rt_tables; do
	if [ -f /etc/iproute2/$c.rpmsave ] && [ ! -e /etc/iproute2/$c ]; then
		%{__mv} -f /etc/iproute2/$c.rpmsave /etc/iproute2/$c
	fi
done

%files
%defattr(644,root,root,755)
%doc README examples
%attr(755,root,root) %{_sbindir}/bridge
%attr(755,root,root) %{_sbindir}/ctstat
%attr(755,root,root) %{_sbindir}/dcb
%attr(755,root,root) %{_sbindir}/devlink
%attr(755,root,root) %{_sbindir}/genl
%attr(755,root,root) %{_sbindir}/ifstat
%attr(755,root,root) %{_sbindir}/ip
%attr(755,root,root) %{_sbindir}/lnstat
%attr(755,root,root) %{_sbindir}/nstat
%attr(755,root,root) %{_sbindir}/rdma
%attr(755,root,root) %{_sbindir}/rtacct
%attr(755,root,root) %{_sbindir}/rtmon
%attr(755,root,root) %{_sbindir}/rtstat
%attr(755,root,root) %{_sbindir}/tipc
%attr(755,root,root) %{_sbindir}/vdpa
# default configs
%dir %{_defaultconfdir}
%{_defaultconfdir}/bpf_pinning
%{_defaultconfdir}/ematch_map
%{_defaultconfdir}/group
%{_defaultconfdir}/nl_protos
%{_defaultconfdir}/rt_dsfield
%{_defaultconfdir}/rt_protos
%{_defaultconfdir}/rt_realms
%{_defaultconfdir}/rt_scopes
%{_defaultconfdir}/rt_tables
%dir %{_defaultconfdir}/protodown_reasons.d
%dir %{_defaultconfdir}/rt_protos.d
%dir %{_defaultconfdir}/rt_tables.d
# config overrides
%dir %{_sysconfdir}/iproute2
%dir %{_sysconfdir}/iproute2/protodown_reasons.d
%dir %{_sysconfdir}/iproute2/rt_protos.d
%dir %{_sysconfdir}/iproute2/rt_tables.d
%{_mandir}/man8/bridge.8*
%{_mandir}/man8/ctstat.8*
%{_mandir}/man8/dcb.8*
%{_mandir}/man8/dcb-app.8*
%{_mandir}/man8/dcb-apptrust.8*
%{_mandir}/man8/dcb-buffer.8*
%{_mandir}/man8/dcb-dcbx.8*
%{_mandir}/man8/dcb-ets.8*
%{_mandir}/man8/dcb-maxrate.8*
%{_mandir}/man8/dcb-pfc.8*
%{_mandir}/man8/dcb-rewr.8*
%{_mandir}/man8/devlink.8*
%{_mandir}/man8/devlink-dev.8*
%{_mandir}/man8/devlink-dpipe.8*
%{_mandir}/man8/devlink-health.8*
%{_mandir}/man8/devlink-lc.8*
%{_mandir}/man8/devlink-monitor.8*
%{_mandir}/man8/devlink-port.8*
%{_mandir}/man8/devlink-rate.8*
%{_mandir}/man8/devlink-region.8*
%{_mandir}/man8/devlink-resource.8*
%{_mandir}/man8/devlink-sb.8*
%{_mandir}/man8/devlink-trap.8*
%{_mandir}/man8/genl.8*
%{_mandir}/man8/ifstat.8*
%{_mandir}/man8/ip.8*
%{_mandir}/man8/ip-*.8*
%{_mandir}/man8/lnstat.8*
%{_mandir}/man8/nstat.8*
%{_mandir}/man8/rdma.8*
%{_mandir}/man8/rdma-dev.8*
%{_mandir}/man8/rdma-link.8*
%{_mandir}/man8/rdma-monitor.8*
%{_mandir}/man8/rdma-resource.8*
%{_mandir}/man8/rdma-statistic.8*
%{_mandir}/man8/rdma-system.8*
%{_mandir}/man8/rtacct.8*
%{_mandir}/man8/rtmon.8*
%{_mandir}/man8/rtstat.8*
%{_mandir}/man8/tipc.8*
%{_mandir}/man8/tipc-*.8*
%{_mandir}/man8/vdpa.8*
%{_mandir}/man8/vdpa-dev.8*
%{_mandir}/man8/vdpa-mgmtdev.8*
%{systemdtmpfilesdir}/%{name}.conf
%dir %attr(750,root,root) /var/run/netns

%files routel
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/routel
%{_mandir}/man8/routel.8*

%files ss
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ss
%{_mandir}/man8/ss.8*

%if %{with tc}
%files tc
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/tc
%dir %{_libdir}/tc
%{_libdir}/tc/*.dist
%{_mandir}/man7/tc-hfsc.7*
%{_mandir}/man8/tc.8*
%{_mandir}/man8/tc-*.8*
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/iproute2

%files -n libnetlink-devel
%defattr(644,root,root,755)
%{_libdir}/libnetlink.a
%{_includedir}/libnetlink.h
%{_mandir}/man3/libnetlink.3*

%files -n bash-completion-iproute2
%defattr(644,root,root,755)
%{bash_compdir}/devlink
%{bash_compdir}/tc
