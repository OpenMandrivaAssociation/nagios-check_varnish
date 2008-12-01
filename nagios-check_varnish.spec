Summary:	Plugins for Nagios to monitor varnish
Name:		nagios-check_varnish
Version:	1.0
Release:	%mkrel 1
License:	BSD-like
Group:		Networking/Other
URL:		http://varnish.projects.linpro.no/
Source0:	http://dfn.dl.sourceforge.net/sourceforge/varnish/nagios-varnish-plugin-%{version}.tar.gz
Source1:	check_varnish.cfg
Requires:	nagios
Requires:	varnish
BuildRequires:	varnish-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This plugin allow you to monitor Varnish, a high-performance HTTP accelerator.

%prep

%setup -q -n nagios-varnish-plugin-%{version}

mkdir plugins.d
cp %{SOURCE1} plugins.d/check_varnish.cfg

%build
%configure2_5x

%make

perl -pi -e "s|\@libexecdir\@|%{_libdir}/nagios/plugins|g" plugins.d/*.cfg

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/nagios/plugins.d
install -d %{buildroot}%{_libdir}/nagios/plugins

install -m0755 check_varnish %{buildroot}%{_libdir}/nagios/plugins/
install -m0644 plugins.d/check_varnish.cfg %{buildroot}%{_sysconfdir}/nagios/plugins.d/check_varnish.cfg

%post
%{_initrddir}/nagios condrestart > /dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    %{_initrddir}/nagios condrestart > /dev/null 2>&1 || :
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/nagios/plugins.d/check_varnish.cfg
%{_libdir}/nagios/plugins/check_varnish

