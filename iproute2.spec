# conditional build
# --with db3
# --without tex	# with tetex-2 there shuld be BR tetex-tex-babel
# --without tc (don't build tc program, it break static linkage)
# --without dist_kernel

%define		_kernel24	%(echo %{_kernel_ver} | grep -q '2\.[012]\.' ; echo $?)
%define mainver		2.4.7
%define snapshot	ss020116
Summary:	Utility to control Networking behavior in 2.2.X kernels
Summary(es):	Herramientas para encaminamiento avanzado y configuraci�n de interfaces de red
Summary(pl):	Narz�dzie do kontrolowania Sieci w kernelach 2.2
Summary(pt_BR):	Ferramentas para roteamento avan�ado e configura��o de interfaces de rede
Name:		iproute2
Version:	%{mainver}.%{snapshot}
%define _rel    2
Release:        %{_rel}@%{_kernel_ver_str}
License:	GPL
Vendor:		Alexey Kuznetsov <kuznet@ms2.inr.ac.ru>
Group:		Networking/Admin
Source0:	ftp://ftp.inr.ac.ru/ip-routing/%{name}-%{mainver}-now-%{snapshot}.tar.gz
Patch0:		%{name}-make.patch
Patch1:		%{name}-uClibc.patch
Patch6:		wrr-iproute2-2.2.4.patch
Patch7:		htb3.6_tc.patch
Patch8:		%{name}-no_libresolv.patch
BuildRequires:	kernel-headers
%{?_with_db3:BuildRequires: db3-devel}
%{!?_with_db3:BuildRequires: db-devel}
%{!?_without_tex:BuildRequires:	tetex-dvips}
%{!?_without_tex:BuildRequires:	tetex-latex}
%{!?_without_tex:BuildRequires: latex2html}
%{!?_without_tex:BuildRequires:	psutils}
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
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch7 -p1
%patch6 -p1
%patch8 -p1

%build
WRRDEF=""
grep -q tc_wrr_class_weight /usr/include/linux/pkt_sched.h || WRRDEF="-DNEED_WRR_DEFS"

%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcflags} ${WRRDEF}" \
	KERNEL_INCLUDE="%{_kernelsrcdir}/include" \
	%{?_without_tc:SUBDIRS="lib ip" LDFLAGS="%{rpmldflags}"}
%{!?_without_tex:%{__make} -C doc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir},%{_mandir}/man8,%{_libdir},%{_includedir}}

install ip/{ip,rtmon,routel} %{!?_without_tc:tc/tc} $RPM_BUILD_ROOT%{_sbindir}
install etc/iproute2/rt_protos \
	etc/iproute2/rt_realms \
	etc/iproute2/rt_scopes \
	etc/iproute2/rt_tables \
	$RPM_BUILD_ROOT%{_sysconfdir}
install lib/libnetlink.a $RPM_BUILD_ROOT%{_libdir}
install include/libnetlink.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README README.iproute2+tc RELNOTES
%{!?_without_tex:%doc doc/*.ps}
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/*

%files -n libnetlink-devel
%defattr(644,root,root,755)
%{_libdir}/*
%{_includedir}/*
