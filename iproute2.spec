Summary:	Utility to control Networking behavior in 2.2.X kernels
Summary(pl):	Narzêdzie do kontrolowania Sieci w kernelach 2.2
Name:		iproute2
Version:	2.2.4
Release:	1
Vendor:		Alexey Kuznetsov <kuznet@ms2.inr.ac.ru>
Copyright:	GPL
Group:		Networking/Admin
Group(pl):	Sieciowe/Administracyjne
Source:		ftp://ftp.inr.ac.ru/ip-routing/%{name}-%{version}-now-ss990417.tar.gz
Patch0:		iproute2-make.patch
Patch1:		iproute2-readme.patch
BuildRoot:	/tmp/%{name}-%{version}-root

%description
This package contains the ip, tc and the rtmon tool that allow control of
routing and other aspects of networking.
  
%description -l pl
Ten pakiet zawiera programy pozwalaj±ce na kontrolê routingu i innych 
aspektów dotycz±cych sieci.
  
%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
make OPT="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{sbin,etc/iproute2}

install -s ip/ip ip/rtmon ip/rtacct tc/tc $RPM_BUILD_ROOT/sbin

install etc/iproute2/rt_protos \
	etc/iproute2/rt_realms \
	etc/iproute2/rt_scopes \
	etc/iproute2/rt_tables \
	$RPM_BUILD_ROOT/etc/iproute2

gzip -9nf READ* RELNOTES

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,README.ip-sysctl,README.iproute2+tc}.gz
%doc {README.multidomain-httpd,README.policy-routing,RELNOTES}.gz
%doc flowlabels.tex ip-tunnels.tex

%attr(755,root,root) /sbin/*
/etc/iproute2

%changelog
* Sat May  1 1999 Piotr Czerwiñski <pius@pld.org.pl>
  [2.2.4-1]
- new upstream release (990417),
- patches corrected,
- added /etc/iproute2/*,
- added more documentation,
- recompiled on rpm 3,
- cosmetic changes for common l&f.

* Fri Feb 19 1999 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
- new upstream release
- gzipping instead bzipping

* Fri Jan 01 1999 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
- new upstream release (981220).
- docs are now compressed

* Sat Nov 07 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
- new upstream release (981101),
- corrected patch.

* Wed Oct 14 1998 Arkadiusz Mi¶kiewicz <misiek@zsz2.starachowice.pl>
- initial rpm release.
