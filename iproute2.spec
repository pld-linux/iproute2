# _without_embed - don't build uClibc version
%define mainver  2.4.7
%define snapshot ss010803
Summary:	Utility to control Networking behavior in 2.2.X kernels
Summary(pl):	Narzêdzie do kontrolowania Sieci w kernelach 2.2
Name:		iproute2
Version:	%{mainver}.%{snapshot}
Release:	4
Vendor:		Alexey Kuznetsov <kuznet@ms2.inr.ac.ru>
License:	GPL
Group:		Networking/Admin
Group(de):	Netzwerkwesen/Administration
Group(pl):	Sieciowe/Administracyjne
Source0:	ftp://ftp.inr.ac.ru/ip-routing/%{name}-%{mainver}-now-%{snapshot}.tar.gz
Patch0:		%{name}-make.patch
Patch1:		%{name}-uClibc.patch
Patch2:		%{name}-fix-2_2.patch
Patch3:		%{name}-label.patch
Patch4:		%{name}-latest.patch
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex
BuildRequires:	psutils
%if %{!?_without_embed:1}%{?_without_embed:0}
BuildRequires:	uClibc-devel
BuildRequires:	uClibc-static
%endif
Obsoletes:	iproute
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_sysconfdir	/etc/iproute2

%define embed_path	/usr/lib/embed
%define embed_cc	%{_arch}-uclibc-cc
%define embed_cflags	%{rpmcflags} -Os
%define uclibc_prefix	/usr/%{_arch}-linux-uclibc

%description
This package contains the ip, tc and the rtmon tool that allow control
of routing and other aspects of networking.

%description -l pl
Ten pakiet zawiera programy pozwalaj±ce na kontrolê routingu i innych
aspektów dotycz±cych sieci.

%package embed
Summary:	Utility to control Networking behavior in 2.2.X kernels
Summary(pl):	Narzêdzie do kontrolowania Sieci w kernelach 2.2
Group:		Networking/Admin
Group(de):	Netzwerkwesen/Administration
Group(pl):	Sieciowe/Administracyjne

%description embed
Embedded iproute2.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build

%if %{!?_without_embed:1}%{?_without_embed:0}
%{__make} \
	OPT="%{embed_cflags}" GLIBCFIX="" \
	KERNEL_INCLUDE="%{_kernelsrcdir}/include" \
	CC=%{embed_cc} \
	ADDLIB="inet_ntop.o inet_pton.o dnet_ntop.o dnet_pton.o ipx_ntop.o ipx_pton.o" \
	SUBDIRS="lib ip"
# someday we might also need rtmon and rtacct, but not today ;)
mv -f ip/ip ip-embed-shared

%{__make} \
	OPT="%{embed_cflags}" GLIBCFIX="" \
	KERNEL_INCLUDE="%{_kernelsrcdir}/include" \
	LDFLAGS="-static" \
	CC=%{embed_cc} \
	ADDLIB="inet_ntop.o inet_pton.o dnet_ntop.o dnet_pton.o ipx_ntop.o ipx_pton.o" \
	SUBDIRS="lib ip"

mv -f ip/ip ip-embed-static
%{__make} clean
%endif

%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcflags}" \
	KERNEL_INCLUDE="%{_kernelsrcdir}/include"
%{__make} -C doc

%install
rm -rf $RPM_BUILD_ROOT
%if %{!?_without_embed:1}%{?_without_embed:0}
install -d $RPM_BUILD_ROOT%{embed_path}/{shared,static}
install ip-embed-shared $RPM_BUILD_ROOT%{embed_path}/shared/ip
install ip-embed-static $RPM_BUILD_ROOT%{embed_path}/static/ip
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
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/*

%if %{!?_without_embed:1}%{?_without_embed:0}
%files embed
%defattr(644,root,root,755)
%attr(755,root,root) %{embed_path}/*/*
%endif
