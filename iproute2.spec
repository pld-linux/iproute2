Summary:	Utility to control Networking behavior in 2.2.X kernels
Summary(pl):	Narzêdzie do kontrolowania Sieci w kernelach 2.2
Name:		iproute2
Version:	2.2.4
Release:	1
Vendor:		Alexey Kuznetsov <kuznet@ms2.inr.ac.ru>
License:	GPL
Group:		Networking/Admin
Group(pl):	Sieciowe/Administracyjne
Source0:	ftp://ftp.inr.ac.ru/ip-routing/%{name}-%{version}-now-ss001007.tar.gz
Patch0:		iproute2-make.patch
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex
BuildRequires:	psutils
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
%patch -p1

%build
%{__make} OPT="$RPM_OPT_FLAGS"
%{__make} -C doc

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}}

install -s ip/ip ip/rtmon ip/rtacct tc/tc $RPM_BUILD_ROOT%{_sbindir}
install    ip/routel $RPM_BUILD_ROOT%{_sbindir}

install etc/iproute2/rt_protos \
	etc/iproute2/rt_realms \
	etc/iproute2/rt_scopes \
	etc/iproute2/rt_tables \
	$RPM_BUILD_ROOT%{_sysconfdir}

gzip -9nf READ* RELNOTES doc/*.ps

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,README.iproute2+tc,RELNOTES}.gz
%doc doc/*.ps.gz

%attr(755,root,root) %{_sbindir}/*
%{_sysconfdir}
