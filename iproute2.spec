#
# Conditional build
# _without_tetex	- don't build documentation
# _without_tc		- don't build tc program (it breaks static linkage)
# _without_tc_esfq	- build tc without esfq support (requires patched headers)
#
%define		_kernel24	%(echo %{_kernel_ver} | grep -q '2\.[012]\.' ; echo $?)
%define mainver		2.4.7
%define snapshot	ss020116
Summary:	Utility to control Networking behavior in 2.2.X kernels
Summary(es):	Herramientas para encaminamiento avanzado y configuración de interfaces de red
Summary(pl):	Narzêdzie do kontrolowania Sieci w kernelach 2.2
Summary(pt_BR):	Ferramentas para roteamento avançado e configuração de interfaces de rede
Name:		iproute2
Version:	%{mainver}.%{snapshot}
%define _rel    11
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Vendor:		Alexey Kuznetsov <kuznet@ms2.inr.ac.ru>
Group:		Networking/Admin
Source0:	ftp://ftp.inr.ac.ru/ip-routing/%{name}-%{mainver}-now-%{snapshot}.tar.gz
# Source0-md5:	2c7e5f3a10e703745ecdc613f7a7d187
Source1:	%{name}-owl-man.tar.bz2
# Source1-md5:	cd4425df972a4ab001db31a5eb1c5da5
Patch0:		%{name}-make.patch
Patch1:		%{name}-uClibc.patch
Patch2:		%{name}-fix-2_2.patch
Patch3:		%{name}-label.patch
Patch4:		%{name}-latest.patch
Patch5:		%{name}-htb2_tc.patch
Patch6:		wrr-iproute2-2.2.4.patch
Patch7:		htb3.6_tc.patch
Patch8:		%{name}-no_libresolv.patch
Patch9:		%{name}-2.2.4-now-ss001007-esfq.diff
Patch10:	%{name}-stats.patch
Patch11:	%{name}-disable_arpd.patch
BuildRequires:	bison
%{!?_without_tetex:BuildRequires:	latex2html}
%{!?_without_tetex:BuildRequires:	psutils}
%{!?_without_tetex:BuildRequires:	sgml-tools}
%{!?_without_tetex:BuildRequires:	tetex-dvips}
%{!?_without_tetex:BuildRequires:	tetex-latex}
%{!?_without_tetex:BuildRequires:	tetex-tex-babel}
Obsoletes:	iproute
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_sysconfdir	/etc/iproute2

%description
Linux 2.2 maintains compatibility with the basic configuration
utilities of the network (ifconfig, route) but a new utility is
required to exploit the new characteristics and features of the
kernel. This package includes the new utilities.

%description -l es
Linux mantiene compatibilidad con los utilitarios estándares de
configuración de la red, pero se necesitan nuevos utilitarios para
usar los recursos y características del nuevo núcleo. Este paquete
incluye los nuevos utilitarios.

%description -l pl
Ten pakiet zawiera programy pozwalaj±ce na kontrolê routingu i innych
aspektów dotycz±cych sieci.

%description -l pt_BR
O Linux mantém compatibilidade com os utilitários padrão de
configuração da rede, mas novos utilitários são necessários para fazer
uso das características e recursos da nova kernel. This package
includes the new utilities.

%package -n libnetlink-devel
Summary:	Library for the netlink interface
Summary(pl):	Biblioteka do interfejsu netlink
Group:		Development/Libraries

%description -n libnetlink-devel
This library provides an interface for kernel-user netlink interface.

%description -n libnetlink-devel -l pl
Ta biblioteka udostêpnia interfejs do interfejsu netlink miêdzy j±drem
a przestrzeni± u¿ytkownika.

%prep
%setup -q -n %{name} -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
#%%patch3 -p1
#%%patch4 -p1
%if %{_kernel24}
%patch7 -p1
%patch10 -p1
%else
%patch5 -p1
%endif
%patch6 -p1
%patch8 -p1
%{!?_without_tc_esfq:%patch9 -p1}
%patch11 -p1

%build
WRRDEF=""
grep -q tc_wrr_class_weight %{_kernelsrcdir}/include/linux/pkt_sched.h || WRRDEF="-DNEED_WRR_DEFS"

%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcflags} ${WRRDEF}" \
	KERNEL_INCLUDE="%{_kernelsrcdir}/include" \
	LDFLAGS="%{rpmldflags}" \
	%{?_without_tc:SUBDIRS="lib ip misc"}
%{!?_without_tetex:%{__make} -C doc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir},%{_mandir}/man8,%{_libdir},%{_includedir}}

install ip/{ip,rtmon,routel} %{!?_without_tc:tc/tc} misc/{rtacct,rtstat} $RPM_BUILD_ROOT%{_sbindir}
install etc/iproute2/rt_protos \
	etc/iproute2/rt_realms \
	etc/iproute2/rt_scopes \
	etc/iproute2/rt_tables \
	$RPM_BUILD_ROOT%{_sysconfdir}
install man/*	$RPM_BUILD_ROOT%{_mandir}/man8
install lib/libnetlink.a $RPM_BUILD_ROOT%{_libdir}
install include/libnetlink.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README README.iproute2+tc RELNOTES %{!?_without_tetex:doc/*.ps}
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/*
%{_mandir}/man8/*

%files -n libnetlink-devel
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{_includedir}/*.h
