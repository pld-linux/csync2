# TODO:
# - inetd subpackage/files
Summary:	Cluster sync tool
Summary(pl.UTF-8):	Narzędzie do synchronizacji klastra
Name:		csync2
Version:	1.33
Release:	0.5
License:	GPL v2
Group:		Daemons
Source0:	http://oss.linbit.com/csync2/%{name}-%{version}.tar.gz
# Source0-md5:	e16e3c0f4285439cef09a6b63319a0b0
Patch0:		%{name}-man_fix.patch
URL:		http://oss.linbit.com/csync2/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gnutls-devel
BuildRequires:	librsync-devel
BuildRequires:	openssl-devel
BuildRequires:	sqlite-devel
Requires:	setup > 2.4.10-4
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

%prep
%setup -q
%patch0 -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_var}/lib/csync2

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO csync2.xinetd csync2_locheck.sh paper.pdf
%dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/csync2.cfg
%attr(755,root,root) %{_sbindir}/csync2
%attr(755,root,root) %{_sbindir}/csync2-compare
%dir %{_var}/lib/csync2
%{_mandir}/man1/*.1*
