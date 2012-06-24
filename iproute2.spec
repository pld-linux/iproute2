# conditional build
# --without tetex
# --without tc (don't build tc program, it break static linkage)
# --without dist_kernel
%define mainver		2.4.7
%define snapshot	ss010803
Summary:	Utility to control Networking behavior in 2.2.X kernels
Summary(es):	Herramientas para encaminamiento avanzado y configuraci�n de interfaces de red
Summary(pl):	Narz�dzie do kontrolowania Sieci w kernelach 2.2
Summary(pt_BR):	Ferramentas para roteamento avan�ado e configura��o de interfaces de rede
Name:		iproute2
Version:	%{mainver}.%{snapshot}
Release:	10
License:	GPL
Vendor:		Alexey Kuznetsov <kuznet@ms2.inr.ac.ru>
Group:		Networking/Admin
Source0:	ftp://ftp.inr.ac.ru/ip-routing/%{name}-%{mainver}-now-%{snapshot}.tar.gz
Source1:	%{name}-owl-man.tar.bz2
Patch0:		%{name}-make.patch
Patch1:		%{name}-uClibc.patch
Patch2:		%{name}-fix-2_2.patch
Patch3:		%{name}-label.patch
Patch4:		%{name}-latest.patch
Patch5:		%{name}-htb3_tc.patch
Patch6:		wrr-iproute2-2.2.4.patch
%{!?_without_tetex:BuildRequires:	tetex-dvips}
%{!?_without_tetex:BuildRequires:	tetex-latex}
%{!?_without_tetex:BuildRequires:	psutils}
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

%prep
%setup -q -n %{name} -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
WRRDEF=""
grep -q tc_wrr_class_weight /usr/include/linux/pkt_sched.h || WRRDEF="-DNEED_WRR_DEFS"

%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcflags} ${WRRDEF}" \
	KERNEL_INCLUDE="%{_kernelsrcdir}/include" \
	%{?_without_tc:SUBDIRS="lib ip" LDFLAGS="%{rpmldflags}"}
%{!?_without_tetex:%{__make} -C doc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir},%{_mandir}/man8}

install ip/{ip,rtmon,rtacct,routel} %{!?_without_tc:tc/tc} $RPM_BUILD_ROOT%{_sbindir}
install etc/iproute2/rt_protos \
	etc/iproute2/rt_realms \
	etc/iproute2/rt_scopes \
	etc/iproute2/rt_tables \
	$RPM_BUILD_ROOT%{_sysconfdir}
install man/*	$RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README README.iproute2+tc RELNOTES
%{!?_without_tetex:%doc doc/*.ps}
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/*
%{_mandir}/man8/*
