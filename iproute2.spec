#
# TODO:
#	- build @ uClibc
#
# Conditional build
%bcond_without	doc		# don't build documentation
%bcond_without	tc		# don't build tc program (it breaks static linkage)
%bcond_with	uClibc		# do some hacks to build with uClibc
%bcond_with	iec_complaint	# fix bitrate calculations
#
Summary:	Utility to control Networking behavior in.X kernels
Summary(es):	Herramientas para encaminamiento avanzado y configuraci�n de interfaces de red
Summary(pl):	Narz�dzie do kontrolowania Sieci w kernelach
Summary(pt_BR):	Ferramentas para roteamento avan�ado e configura��o de interfaces de rede
Name:		iproute2
Version:	2.6.6
Release:	0.1
License:	GPL
Vendor:		Stephen Hemminger <shemminger@osdl.org>
Group:		Networking/Admin
Source0:	http://developer.osdl.org/dev/iproute2/download/%{name}-%{version}.tar.bz2
# Source0-md5:	b70b6b9de4b1a901ee20fea2ae7bd3b1
Patch0:		%{name}-llh.patch
URL:		http://developer.osdl.org/dev/iproute2/
BuildRequires:	bison
BuildRequires:	linux-libc-headers >= 7:2.6.5.1-4
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
Linux mantiene compatibilidad con los utilitarios est�ndares de
configuraci�n de la red, pero se necesitan nuevos utilitarios para
usar los recursos y caracter�sticas del nuevo n�cleo. Este paquete
incluye los nuevos utilitarios.

%description -l pl
Ten pakiet zawiera programy pozwalaj�ce na kontrol� routingu i innych
aspekt�w dotycz�cych sieci.

%description -l pt_BR
O Linux mant�m compatibilidade com os utilit�rios padr�o de
configura��o da rede, mas novos utilit�rios s�o necess�rios para fazer
uso das caracter�sticas e recursos da nova kernel. This package
includes the new utilities.

%package -n libnetlink-devel
Summary:	Library for the netlink interface
Summary(pl):	Biblioteka do interfejsu netlink
Group:		Development/Libraries

%description -n libnetlink-devel
This library provides an interface for kernel-user netlink interface.

%description -n libnetlink-devel -l pl
Ta biblioteka udost�pnia interfejs do interfejsu netlink mi�dzy j�drem
a przestrzeni� u�ytkownika.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
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
install man/*	$RPM_BUILD_ROOT%{_mandir}/man8
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
