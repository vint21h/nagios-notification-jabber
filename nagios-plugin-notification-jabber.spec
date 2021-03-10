# nagios-notification-jabber
# nagios-plugin-notification-jabber.spec

%global _unpackaged_files_terminate_build 0
%global original_name nagios-notification-jabber
%global debug_package %{nil}

Summary: Notifications via jabber Nagios plugin
Name: nagios-plugins-notification-jabber
Version: 1.0.3
Release: 1%{?dist}
Source0: %{original_name}-%{version}.tar.gz
License: GPLv3 or later
Group: Applications/System
BuildRequires: python-setuptools
Requires: python >= 3.7
Requires: nagios-plugins
Requires: slixmpp
Packager: Alexei Andrushievich <vint21h@vint21h.pp.ua>
Url: https://github.com/vint21h/nagios-notification-jabber/

%description
Notifications via jabber Nagios plugin.

%prep
%setup -n %{original_name}-%{version}

%install
mkdir -p %{buildroot}%{_libdir}/nagios/plugins
install -p -m 755 notification_jabber.py %{buildroot}%{_libdir}/nagios/plugins/notification_jabber

%files
%defattr(-,root,root)
%doc README.rst COPYING AUTHORS notification_jabber.ini
%{_libdir}/nagios/plugins/notification_jabber

%changelog
* Wed Mar 10 2021 Alexei Andrushievich <vint21h@vint21h.pp.ua> - 1.0.3-1
- Updated to new version

* Sun Mar 7 2021 Alexei Andrushievich <vint21h@vint21h.pp.ua> - 1.0.2-1
- Updated to new version

* Tue Feb 16 2021 Alexei Andrushievich <vint21h@vint21h.pp.ua> - 1.0.1-1
- Updated to new version

* Tue Feb 16 2021 Alexei Andrushievich <vint21h@vint21h.pp.ua> - 1.0.0-1
- Init
