Summary:     Utility to control Networking behavior in 2.2.X kernels
Name:	     iproute2
Version:     2.1.99
Release:     3d
Vendor:	     Alexey Kuznetsov <kuznet@ms2.inr.ac.ru>
Copyright:   GPL
Group:	     Networking/Admin
Group(pl):   Sieæ/Administracja
URL:	     ftp://ftp.inr.ac.ru/ip-routing
Source:      %{name}-%{version}-now-ss990203.tar.gz
Patch:	     %{name}.make.diff
Patch1:	     %{name}.readme.patch
BuildRoot:   /var/tmp/%{name}-buildroot
Summary(pl): Narzêdzie do kontrolowania Sieci w kernelach 2.2

%description
This package contains the ip and the rtmon tool that allow control of
routing and other aspects of networking.
  
%description -l pl
Ten pakiet zawiera programy pozwalaj±ce na kontrolê routingu i innych
aspektów dotycz±cych sieci.
  
%prep
%setup -q -n %{name}
%patch  -p1
%patch1 -p1

%build
make OPT="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/sbin
install -s ip/ip ip/rtmon tc/tc $RPM_BUILD_ROOT/sbin

gzip -9nf READ*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.gz README.ip-sysctl.gz
%doc README.iproute2+tc.gz README.multidomain-httpd.gz
%doc README.policy-routing.gz

%attr(755,root,root) /sbin/*

%changelog
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
