Summary:	Utility to control Networking behavior in 2.2.X kernels
Summary(pl):	Narzędzie do kontrolowania Sieci w kernelach 2.2
Name:		iproute2
Version:	2.2.4
Release:	2
Vendor:		Alexey Kuznetsov <kuznet@ms2.inr.ac.ru>
Copyright:	GPL
Group:		Networking/Admin
Group(pl):	Sieciowe/Administracja
Source:		ftp://ftp.inr.ac.ru/ip-routing/%{name}-%{version}-now-ss990630.tar.gz
Patch:		iproute2-make.patch
BuildRequire:	tetex-dvips
BuildRoot:	/tmp/%{name}-%{version}-root

%description
This package contains the ip, tc and the rtmon tool that allow control of
routing and other aspects of networking.
  
%description -l pl
Ten pakiet zawiera programy pozwalające na kontrolę routingu i innych 
aspektów dotyczących sieci.
  
%prep
%setup -q -n %{name}
%patch -p1

%build
make OPT="$RPM_OPT_FLAGS"
make -C doc

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT/etc/iproute2

install -s ip/ip ip/rtmon ip/rtacct tc/tc $RPM_BUILD_ROOT%{_sbindir}
install    ip/routel $RPM_BUILD_ROOT%{_sbindir}

install etc/iproute2/rt_protos \
	etc/iproute2/rt_realms \
	etc/iproute2/rt_scopes \
	etc/iproute2/rt_tables \
	$RPM_BUILD_ROOT/etc/iproute2


gzip -9nf READ* RELNOTES doc/*.ps

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,README.iproute2+tc,RELNOTES}.gz
%doc doc/*.ps.gz

%attr(755,root,root) %{_sbindir}/*
/etc/iproute2
