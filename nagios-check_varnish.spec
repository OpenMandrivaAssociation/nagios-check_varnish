Summary:	Plugins for Nagios to monitor varnish
Name:		nagios-check_varnish
Version:	1.0
Release:	%mkrel 4
License:	BSD-like
Group:		Networking/Other
URL:		http://varnish.projects.linpro.no/
Source0:	http://dfn.dl.sourceforge.net/sourceforge/varnish/nagios-varnish-plugin-%{version}.tar.gz
Requires:	nagios-plugins
Requires:	varnish
BuildRequires:	varnish-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
This plugin allow you to monitor Varnish, a high-performance HTTP accelerator.

%prep
%setup -q -n nagios-varnish-plugin-%{version}

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_libdir}/nagios/plugins
install -m 755 check_varnish %{buildroot}%{_libdir}/nagios/plugins/

install -d -m 755 %{buildroot}%{_sysconfdir}/nagios/plugins.d
cat > %{buildroot}%{_sysconfdir}/nagios/plugins.d/check_varnish.cfg <<'EOF'
define command {
	command_name	check_varnish
	command_line	%{_libdir}/nagios/plugins/check_varnish -l -n $ARG1$ -p $ARG2$ -c $ARG3$ -w $ARG4$
}
EOF

%if %mdkversion < 200900
%post
%{_initrddir}/nagios condrestart > /dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    %{_initrddir}/nagios condrestart > /dev/null 2>&1 || :
fi
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/nagios/plugins.d/check_varnish.cfg
%{_libdir}/nagios/plugins/check_varnish
