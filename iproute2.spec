# conditional build
# --without tetex
# --without tc (don't build tc program, it break static linkage)
%define mainver		2.4.7
%define snapshot	ss010803
Summary:	Utility to control Networking behavior in 2.2.X kernels
Summary(pl):	Narzêdzie do kontrolowania Sieci w kernelach 2.2
Name:		iproute2
Version:	%{mainver}.%{snapshot}
Release:	5
License:	GPL
Vendor:		Alexey Kuznetsov <kuznet@ms2.inr.ac.ru>
Group:		Networking/Admin
Source0:	ftp://ftp.inr.ac.ru/ip-routing/%{name}-%{mainver}-now-%{snapshot}.tar.gz
Patch0:		%{name}-make.patch
Patch1:		%{name}-uClibc.patch
Patch2:		%{name}-fix-2_2.patch
Patch3:		%{name}-label.patch
Patch4:		%{name}-latest.patch
Patch5:		%{name}-htb2_tc.patch
%{!?_without_tetex:BuildRequires:	tetex-dvips}
%{!?_without_tetex:BuildRequires:	tetex-latex}
%{!?_without_tetex:BuildRequires:	psutils}
Obsoletes:	iproute
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_sysconfdir	/etc/iproute2

%description
This package contains the ip, tc and the rtmon tool that allow control
of routing and other aspects of networking.

%description -l pl
Ten pakiet zawiera programy pozwalaj±ce na kontrolê routingu i innych
aspektów dotycz±cych sieci.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build

%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	KERNEL_INCLUDE="%{_kernelsrcdir}/include" \
	%{?_without_tc:SUBDIRS="lib ip"}
%{!?_without_tetex:%{__make} -C doc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}}

install ip/{ip,rtmon,rtacct,routel} %{!?_without_tc:tc/tc} $RPM_BUILD_ROOT%{_sbindir}
install etc/iproute2/rt_protos \
	etc/iproute2/rt_realms \
	etc/iproute2/rt_scopes \
	etc/iproute2/rt_tables \
	$RPM_BUILD_ROOT%{_sysconfdir}

gzip -9nf READ* RELNOTES %{!?_without_tetex:doc/*.ps}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,README.iproute2+tc,RELNOTES}.gz
%{!?_without_tetex:d%doc doc/*.ps.gz}
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/*
