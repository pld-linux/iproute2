%define mainver  2.2.4
%define snapshot ss001007
Summary:	Utility to control Networking behavior in 2.2.X kernels
Summary(pl):	Narzêdzie do kontrolowania Sieci w kernelach 2.2
Name:		iproute2
Version:	%{mainver}.%{snapshot}
Release:	3
Vendor:		Alexey Kuznetsov <kuznet@ms2.inr.ac.ru>
License:	GPL
Group:		Networking/Admin
Group(de):	Netzwerkwesen/Administration
Group(pl):	Sieciowe/Administracyjne
Source0:	ftp://ftp.inr.ac.ru/ip-routing/%{name}-%{mainver}-now-%{snapshot}.tar.gz
Patch0:		%{name}-make.patch
Patch1:		%{name}-ll_types.patch
%{?BOOT:Patch2:	%{name}-uClibc.patch}
Patch3:		%{name}-linux-2.4.5.patch
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex
BuildRequires:	psutils
%{?BOOT:BuildRequires:	uClibc-devel-BOOT}
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


%if %{?BOOT:1}%{!?BOOT:0}
%package BOOT
Summary:	Utility to control Networking behavior in 2.2.X kernels
Summary(pl):	Narzêdzie do kontrolowania Sieci w kernelach 2.2
Group:		Networking/Admin
Group(de):	Netzwerkwesen/Administration
Group(pl):	Sieciowe/Administracyjne

%description BOOT

%endif


%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%{?BOOT:%patch2 -p1}
%patch3 -p1

%build

%if %{?BOOT:1}%{!?BOOT:0}
%{__make} \
	OPT="-m386 -Os" GLIBCFIX="" \
	KERNEL_INCLUDE="/usr/src/linux/include -I%{_libdir}/bootdisk%{_includedir}" \
	LDFLAGS="-nostdlib -static -s" \
	LDLIBS="%{_libdir}/bootdisk%{_libdir}/crt0.o %{_libdir}/bootdisk%{_libdir}/libc.a -lgcc" \
	ADDLIB="inet_ntop.o inet_pton.o dnet_ntop.o dnet_pton.o ipx_ntop.o ipx_pton.o" \
	SUBDIRS="lib ip"

# there are some problems compiling with uClibc, falling back to simple glibc-static
%{__make} SUBDIRS="lib ip" OPT="-Os" LDFLAGS="-static -s" 
mv -f ip/ip ip-BOOT
mv -f ip/rtacct rtacct-BOOT
mv -f ip/rtmon rtmon-BOOT
%{__make} clean
%endif

%{__make} OPT="%{rpmcflags}"
%{__make} -C doc



%install
rm -rf $RPM_BUILD_ROOT
%if %{?BOOT:1}%{!?BOOT:0}
install -d $RPM_BUILD_ROOT%{_libdir}/bootdisk/sbin
# we need only 'ip' on bootdisk (don't we??)
install -s ip-BOOT $RPM_BUILD_ROOT%{_libdir}/bootdisk/sbin/ip
%endif

install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}}
install ip/{ip,rtmon,rtacct,routel} tc/tc $RPM_BUILD_ROOT%{_sbindir}
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

%if %{?BOOT:1}%{!?BOOT:0}
%files BOOT
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/bootdisk/sbin/*
%endif
