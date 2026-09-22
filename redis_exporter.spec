%global debug_package %{nil}
%global user prometheus
%global group prometheus

Name:    redis_exporter
Version: 1.90.1
Release: 1%{?dist}
Summary: Prometheus exporter for Redis server metrics.
License: MIT
URL:     https://github.com/oliver006/redis_exporter

Source0: https://github.com/oliver006/redis_exporter/releases/download/v%{version}/%{name}-v%{version}.linux-amd64.tar.gz
Source1: %{name}.unit
Source2: %{name}.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description
Prometheus Exporter for Redis Metrics. Supports Redis 2.x, 3.x, 4.x, 5.x and 6.x

%prep
%setup -q -n %{name}-v%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/prometheus
%{_unitdir}/%{name}.service

%changelog
* Tue Sep 22 2026 Ivan Garcia
- Bump version to 1.90.1
* Sat Sep 05 2026 Ivan Garcia <igarcia@cloudox.org> - 1.90.0
- Bump to 1.90.0
* Thu Aug 06 2026 Ivan Garcia <igarcia@cloudox.org> - 1.88.0
- Add stream_entries_added_total
* Wed Jun 10 2026 Ivan Garcia <igarcia@cloudox.org> - 1.86.0
- Initial packaging for the 1.86.0 branch
