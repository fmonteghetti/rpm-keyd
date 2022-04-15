Name:           keyd
Version:        2.3.1.rc
Release:        1%{?dist}
Summary:        A key remapping daemon for linux

License:        MIT
URL:            https://github.com/rvaiya/%{name}
Source0:        https://github.com/rvaiya/%{name}/archive/refs/tags/v2.3.1-rc.tar.gz

Patch0:        Makefile-fPIE.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros

Requires: systemd

%description
Linux lacks a good key remapping solution. In order to achieve satisfactory 
results a medley of tools need to be employed (e.g xcape, xmodmap) with the end
result often being tethered to a specified environment (X11). keyd attempts to
solve this problem by providing a flexible system wide daemon which remaps keys
using kernel level input primitives (evdev, uinput).

Note: this package only provides the keyd daemon.

%prep
%setup -q -n %{name}-2.3.1-rc
# Patch Makefile to use -fPIE
%patch0

%build
# Compile with debug symbols to generate debug packages
make debug

%install
%make_install
# Manual installation for files that can be bypassed by Makefile
install -Dm644 %{name}.service %{buildroot}/%{_unitdir}/%{name}.service
install -Dm644 %{name}.quirks %{buildroot}/usr/share/libinput/30-%{name}.quirks
# Remove keyd-application-manager
rm %{buildroot}/%{_datadir}/man/man1/%{name}-application-mapper.1.gz
rm %{buildroot}/%{_bindir}/%{name}-application-mapper

%files
%license LICENSE
%{_bindir}/%{name}
/usr/share/libinput/30-%{name}.quirks
%{_unitdir}/%{name}.service
%{_datadir}/doc/%{name}/CHANGELOG.md
%{_datadir}/doc/%{name}/DESIGN.md
%{_datadir}/doc/%{name}/examples/capslock-esc-basic.conf
%{_datadir}/doc/%{name}/examples/capslock-escape-with-vim-mode.conf
%{_datadir}/doc/%{name}/examples/international-glyphs.conf
%{_datadir}/doc/%{name}/examples/macos.conf
%{_datadir}/doc/%{name}/examples/meta-esc.conf
%{_datadir}/doc/%{name}/examples/nav-layer.conf
%{_datadir}/man/man1/%{name}.1.gz
# Specific to keyd-application-mapper
#%%{_bindir}/%%{name}-application-mapper
#%%{_datadir}/man/man1/%%{name}-application-mapper.1.gz

%pre
# Create group 'keyd'
getent group %{name} || groupadd %{name}

# Scriptlets for packages containing systemd unit files
# Source: Fedora Packaging guidelines

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
* Thu Apr 14 2022 Florian Monteghetti <f.monteghetti@gmail.com> - 2.3.1.rc-1
- First Fedora package for keyd.
