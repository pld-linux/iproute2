#
# TODO:
#	- fix build @ uClibc
#       - fix iface_descr patch
#
# Conditional build
%bcond_without	doc		# don't build documentation
%bcond_without	tc		# don't build tc program (it breaks static linkage)
%bcond_without	atm		# don't required ATM.
%bcond_with	uClibc		# do some hacks to build with uClibc
#%bcond_with	iface_descr	# build with interface description support
#
Summary:	Utility to control Networking behavior in.X kernels
Summary(es.UTF-8):	Herramientas para encaminamiento avanzado y configuración de interfaces de red
Summary(pl.UTF-8):	Narzędzie do kontrolowania Sieci w kernelach
Summary(pt_BR.UTF-8):	Ferramentas para roteamento avançado e configuração de interfaces de rede
Name:		iproute2
%define	sdate	070710
# do not use ,,2.6.X'' as version here, put whole number like 2.6.8
Version:	2.6.22
Release:	1
License:	GPL
Group:		Networking/Admin
Source0:	http://developer.osdl.org/dev/iproute2/download/%{name}-%{version}-%{sdate}.tar.gz
# Source0-md5:	20ef2767896a0f156b6fbabd47936f79
Patch0:		%{name}-build.patch
Patch1:		%{name}-arp.patch
Patch2:		%{name}-lex.patch
Patch3:		%{name}-iptables.patch
Patch4:		%{name}-iptables64.patch
Patch5:		%{name}-LDFLAGS.patch
# extensions
Patch10:	%{name}-2.2.4-wrr.patch
Patch11:	esfq-%{name}.patch
Patch12:	001-net-dev-iface-descr-0.1.diff
Patch13:	%{name}-q_atm_c.patch
URL:		http://linux-net.osdl.org/index.php/Iproute2
BuildRequires:	bison
BuildRequires:	db-devel
BuildRequires:	flex
%if %{with atm}
BuildRequires:	linux-atm-devel
%endif
BuildRequires:	linux-libc-headers >= 7:2.6.12.0-15
%if %{with doc}
BuildRequires:	psutils
BuildRequires:	sgml-tools
BuildRequires:	tetex-dvips
BuildRequires:	tetex-fonts-jknappen
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-metafont
BuildRequires:	tetex-tex-babel
%endif
Obsoletes:	iproute
Obsoletes:	ifstat
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_sysconfdir	/etc/iproute2

%description
Linux maintains compatibility with the basic configuration utilities
of the network (ifconfig, route) but a new utility is required to
exploit the new characteristics and features of the kernel. This
package includes the new utilities.

%description -l es.UTF-8
Linux mantiene compatibilidad con los utilitarios estándares de
configuración de la red, pero se necesitan nuevos utilitarios para
usar los recursos y características del nuevo núcleo. Este paquete
incluye los nuevos utilitarios.

%description -l pl.UTF-8
Ten pakiet zawiera programy pozwalające na kontrolę routingu i innych
aspektów dotyczących sieci.

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

%prep
%setup -q -c -n iproute-%{version}-%{sdate}
#rm -rf include/linux
%patch0 -p1
%patch1 -p1
#%patch2 -p1
%if "%{_lib}" == "lib64"
%patch4 -p1
%else
%patch3 -p1
%endif
%patch5 -p1

# extensions:
%patch10 -p1
%patch11 -p1
#%{?with_iface_descr:%patch12 -p1}
%patch13 -p0

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
	OPT="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	%{!?with_tc:SUBDIRS="lib ip misc"}

%{?with_doc:%{__make} -C doc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir},%{_mandir}/man8,%{_libdir},%{_includedir},%{?with_tc:%{_libdir}/tc}}

install ip/{ip,rtmon,routel} %{?with_tc:tc/tc} misc/{ifstat,lnstat,nstat,rtacct,ss} $RPM_BUILD_ROOT%{_sbindir}
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
%{?with_tc:install tc/*.so $RPM_BUILD_ROOT%{_libdir}/tc}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README README.decnet README.iproute2+tc README.lnstat RELNOTES
%doc ChangeLog %{?with_doc:doc/*.ps}
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%{_mandir}/man8/*
%{?with_tc:%dir %{_libdir}/tc}
%{?with_tc:%attr(755,root,root) %{_libdir}/tc/*.so}

%files -n libnetlink-devel
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{_includedir}/*.h
