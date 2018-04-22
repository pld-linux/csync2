Summary:	Cluster sync tool
Summary(pl.UTF-8):	Narzędzie do synchronizacji klastra
Name:		csync2
Version:	2.0
Release:	3
License:	GPL v2+
Group:		Daemons
Source0:	http://oss.linbit.com/csync2/%{name}-%{version}.tar.gz
# Source0-md5:	4e189ff02af441e588ceaa7791732162
Source1:	%{name}.init
Source2:	%{name}.inet
Source3:	%{name}.sysconfig
Patch0:		%{name}-fix-sonames.patch
Patch1:		%{name}-docdata.patch
Patch2:		librsync.patch
URL:		http://oss.linbit.com/csync2/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gnutls-devel
BuildRequires:	librsync-devel
BuildRequires:	mysql-devel
BuildRequires:	openssl-devel
BuildRequires:	postgresql-devel
BuildRequires:	sqlite3-devel
BuildRequires:	texlive-format-pdflatex
Requires:	setup > 2.4.10-4
Suggests:	mysql-libs
Suggests:	postgresql-libs
Suggests:	sqlite3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

%description
Csync2 is a cluster synchronization tool. It can be used to keep files
on multiple hosts in a cluster in sync. Csync2 can handle complex
setups with much more than just 2 hosts, handle file deletions and can
detect conflicts. It is expedient for HA-clusters, HPC-clusters, COWs
and server farms.

%description -l pl.UTF-8
Csync2 to narzędzie do synchronizacji klastra. Może być używane do
utrzymywania zgodności plików na wielu hostach w klastrze. Csync2 jest
w stanie obsłużyć złożone konfiguracje z więcej niż 2 hostami,
obsługiwać usuwanie plików i wykrywać konflikty. Jest praktyczne dla
klastrów HA, HPC, COW oraz farm serwerów.

%package -n csync2-inetd
Summary:	Files necessary to run csync2 in inetd service mode
Summary(pl.UTF-8):	Pliki niezbędne do uruchomienia csync2 w trybie usługi inetd
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	rc-inetd
Provides:	csyncd
Provides:	csyncd-inetd
Obsoletes:	csyncd
Obsoletes:	csync2-standalone
Obsoletes:	csyncd-standalone

%description -n csync2-inetd
Csync2 is a cluster synchronization tool. It can be used to keep files
on multiple hosts in a cluster in sync. Csync2 can handle complex
setups with much more than just 2 hosts, handle file deletions and can
detect conflicts. It is expedient for HA-clusters, HPC-clusters, COWs
and server farms.

%description -n csync2-inetd -l pl.UTF-8
Csync2 to narzędzie do synchronizacji klastra. Może być używane do
utrzymywania zgodności plików na wielu hostach w klastrze. Csync2 jest
w stanie obsłużyć złożone konfiguracje z więcej niż 2 hostami,
obsługiwać usuwanie plików i wykrywać konflikty. Jest praktyczne dla
klastrów HA, HPC, COW oraz farm serwerów.

%package -n csync2-standalone
Summary:	Files necessary to run csync2 in standalone daemon mode
Summary(pl.UTF-8):	Pliki niezbędne do uruchomienia csync2 w trybie samodzielnego serwera
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Provides:	csyncd
Provides:	csyncd-standalone
Obsoletes:      csyncd
Obsoletes:      csync2-inetd
Obsoletes:      csyncd-inetd

%description -n csync2-standalone
Csync2 is a cluster synchronization tool. It can be used to keep files
on multiple hosts in a cluster in sync. Csync2 can handle complex
setups with much more than just 2 hosts, handle file deletions and can
detect conflicts. It is expedient for HA-clusters, HPC-clusters, COWs
and server farms.

%description -n csync2-standalone -l pl.UTF-8
Csync2 to narzędzie do synchronizacji klastra. Może być używane do
utrzymywania zgodności plików na wielu hostach w klastrze. Csync2 jest
w stanie obsłużyć złożone konfiguracje z więcej niż 2 hostami,
obsługiwać usuwanie plików i wykrywać konflikty. Jest praktyczne dla
klastrów HA, HPC, COW oraz farm serwerów.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1

%build
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	--enable-gnutls \
	--enable-mysql \
	--enable-postgres \
	--enable-sqlite3
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_var}/lib/csync2,/etc/{sysconfig/rc-inetd,rc.d/init.d}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n csync2-inetd
%service -q rc-inetd reload

%postun -n csync2-inetd
if [ "$1" = "0" ]; then
        %service -q rc-inetd reload
fi

%post -n csync2-standalone
/sbin/chkconfig --add csync2
%service csync2 restart "csync2 server"

%preun -n csync2-standalone
if [ "$1" = "0" ]; then
        %service csync2 stop
        /sbin/chkconfig --del csync2
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README csync2.xinetd doc/csync2_paper.pdf
%dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/csync2.cfg
%attr(755,root,root) %{_sbindir}/csync2
%attr(755,root,root) %{_sbindir}/csync2-compare
%dir %{_var}/lib/csync2
%{_mandir}/man1/*.1*

%files -n csync2-inetd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/%{name}

%files -n csync2-standalone
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
