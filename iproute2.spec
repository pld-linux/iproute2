#
# TODO:
#	- fix build @ uClibc
#
# Conditional build
%bcond_without	doc		# don't build documentation
%bcond_without	tc		# don't build tc program (it breaks static linkage)
%bcond_with	uClibc		# do some hacks to build with uClibc
%bcond_with	iec_complaint	# fix bitrate calculations
#
Summary:	Utility to control Networking behavior in.X kernels
Summary(es):	Herramientas para encaminamiento avanzado y configuración de interfaces de red
Summary(pl):	Narzêdzie do kontrolowania Sieci w kernelach
Summary(pt_BR):	Ferramentas para roteamento avançado e configuração de interfaces de rede
Name:		iproute2
%define	sdate	040608
Version:	2.6.7
Release:	0.1
License:	GPL
Vendor:		Stephen Hemminger <shemminger@osdl.org>
Group:		Networking/Admin
Source0:	http://developer.osdl.org/dev/iproute2/download/%{name}-%{version}-ss%{sdate}.tar.gz
# Source0-md5:	28196897deb1a45295cd606bd911a33d
Patch0:         %{name}-build.patch
Patch1:		%{name}-db.patch
Patch2:		%{name}-arp.patch
Patch3:         %{name}-diffserv-config.patch
Patch4:         %{name}-ipaddress.patch
# extensions
Patch10:        %{name}-2.2.4-wrr.patch
Patch11:        %{name}-2.2.4-esfq.patch
Patch12:        %{name}-hfsc.patch
Patch13:        %{name}-rates-1024-fix.patch
URL:		http://developer.osdl.org/dev/iproute2/
BuildRequires:	bison
BuildRequires:	linux-libc-headers >= 7:2.6.6.0-2
%if %{with doc}
BuildRequires:	psutils
BuildRequires:	sgml-tools
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex
BuildRequires:	tetex-tex-babel
%endif
Obsoletes:	iproute
Conflicts:	ifstat
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_sysconfdir	/etc/iproute2

%description
Linux maintains compatibility with the basic configuration
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
%setup -q
rm -rf include-glibc
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%patch10 -p1
%patch11 -p1
%patch12 -p1
%{?with_iec_complaint:%patch13 -p1}

%build
%{__make} \
	%{?with_uClibc:CC="%{_target_cpu}-uclibc-gcc"}%{!?with_uClibc:CC="%{__cc}"} \
	OPT="%{rpmcflags}" \
	%{!?with_tc:SUBDIRS="lib ip misc" LDFLAGS="%{rpmldflags}"}

%{?with_doc:%{__make} -C doc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir},%{_mandir}/man8,%{_libdir},%{_includedir}}

install ip/{ip,rtmon,routel} %{?with_tc:tc/tc} misc/{rtacct,rtstat,ss,ifstat} $RPM_BUILD_ROOT%{_sbindir}
install etc/iproute2/rt_protos \
	etc/iproute2/rt_realms \
	etc/iproute2/rt_scopes \
	etc/iproute2/rt_tables \
	$RPM_BUILD_ROOT%{_sysconfdir}

install man/man8/*	$RPM_BUILD_ROOT%{_mandir}/man8
echo ".so tc-pbfifo.8" > $RPM_BUILD_ROOT%{_mandir}/man8/tc-bfifo.8
echo ".so tc-pbfifo.8" > $RPM_BUILD_ROOT%{_mandir}/man8/tc-pfifo.8

install lib/libnetlink.a $RPM_BUILD_ROOT%{_libdir}
install include/libnetlink.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README README.iproute2+tc RELNOTES %{?with_doc:doc/*.ps}
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/*
%{_mandir}/man8/*

%files -n libnetlink-devel
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{_includedir}/*.h
