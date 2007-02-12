Summary:	Cluster sync tool
Summary(pl.UTF-8):	Narzędzie do synchronizacji klastra
Name:		csync2
Version:	1.22
Release:	0.1
License:	GPL
Group:		Daemons
Source0:	http://oss.linbit.com/csync2/%{name}-%{version}.tar.gz
# Source0-md5:	6504aba35683d1663fb530b50f4c1dfd
URL:		http://oss.linbit.com/csync2/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	librsync-devel
BuildRequires:	openssl-devel
BuildRequires:	sqlite-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%build
%configure
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install csync2 $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_var}/lib/csync2

%clean
rm -rf $RPM_BUILD_ROOT

%post
if ! grep -q "^csync2" /etc/services ; then
     echo -e "csync2\t\t30865/tcp\t\t# Cluster sync" >> /etc/services
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_sbindir}/csync2
%dir %{_var}/lib/csync2
