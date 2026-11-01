# Copyright (c) 2025 Asher Buk
# SPDX-License-Identifier: MIT
# https://copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora/

# =============================================================================
# Version definitions
# =============================================================================
%global portal_version          1.5.0
%global hyprland_min_ver        0.57.0
%global hyprwayland_scanner_ver 0.4.6
%global hyprutils_ver           0.14.3
%global hyprlang_ver            0.6.8
%global hyprland_protocols_ver  0.8.0
%global aquamarine_ver          0.15.1
%global hyprgraphics_ver        0.5.1
%global hyprtoolkit_ver         0.6.0

# Vendored libs live in hyprland's private prefix and aren't advertised as sonames;
# the ABI pairing is required through hyprland-vendor() provides below.
%global __requires_exclude ^lib(aquamarine|hypr[a-z]+)\\.so

Name:           xdg-desktop-portal-hyprland
Version:        %{portal_version}
Release:        1%{?dist}
Summary:        XDG Desktop Portal backend for Hyprland
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/xdg-desktop-portal-hyprland

# Main source
Source0:        https://github.com/hyprwm/xdg-desktop-portal-hyprland/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Vendored Hyprland libs (same versions as hyprland package)
# These are needed at build time and will be linked via RUNPATH
Source10:       https://github.com/hyprwm/hyprwayland-scanner/archive/refs/tags/v%{hyprwayland_scanner_ver}.tar.gz#/hyprwayland-scanner-%{hyprwayland_scanner_ver}.tar.gz
Source11:       https://github.com/hyprwm/hyprutils/archive/refs/tags/v%{hyprutils_ver}.tar.gz#/hyprutils-%{hyprutils_ver}.tar.gz
Source12:       https://github.com/hyprwm/hyprlang/archive/refs/tags/v%{hyprlang_ver}.tar.gz#/hyprlang-%{hyprlang_ver}.tar.gz
Source13:       https://github.com/hyprwm/hyprland-protocols/archive/refs/tags/v%{hyprland_protocols_ver}.tar.gz#/hyprland-protocols-%{hyprland_protocols_ver}.tar.gz
# hyprtoolkit and its hypr* deps (for the share picker)
Source14:       https://github.com/hyprwm/aquamarine/archive/refs/tags/v%{aquamarine_ver}.tar.gz#/aquamarine-%{aquamarine_ver}.tar.gz
Source15:       https://github.com/hyprwm/hyprgraphics/archive/refs/tags/v%{hyprgraphics_ver}.tar.gz#/hyprgraphics-%{hyprgraphics_ver}.tar.gz
Source16:       https://github.com/hyprwm/hyprtoolkit/archive/refs/tags/v%{hyprtoolkit_ver}.tar.gz#/hyprtoolkit-%{hyprtoolkit_ver}.tar.gz

# Build dependencies
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconf-pkg-config
BuildRequires:  pugixml-devel
BuildRequires:  pixman-devel

# Portal dependencies
BuildRequires:  pipewire-devel >= 1.1.82
BuildRequires:  sdbus-cpp-devel >= 2.0.0
BuildRequires:  libdrm-devel
BuildRequires:  libuuid-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel >= 1.39

# hyprtoolkit chain for hyprland-share-picker (build-time only, runtime libs come from hyprland)
BuildRequires:  abseil-cpp-devel
BuildRequires:  cairo-devel
BuildRequires:  file-devel
BuildRequires:  hwdata
BuildRequires:  iniparser-devel
BuildRequires:  libdisplay-info-devel
BuildRequires:  libglvnd-devel
BuildRequires:  libinput-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libseat-devel
BuildRequires:  libwebp-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  pango-devel
BuildRequires:  systemd-devel

# Runtime deps
Requires:       hyprland >= %{hyprland_min_ver}
Requires:       hyprland-vendor(hyprlang) = %{hyprlang_ver}
Requires:       hyprland-vendor(hyprtoolkit) = %{hyprtoolkit_ver}
Requires:       hyprland-vendor(hyprutils) = %{hyprutils_ver}
Requires:       xdg-desktop-portal
Requires:       pipewire >= 1.1.82

%description
xdg-desktop-portal-hyprland is a portal backend for Hyprland that provides
screen sharing, file dialogs, and other desktop integration features.

This package uses the same vendored Hyprland libraries as the main hyprland
package, located in /usr/libexec/hyprland/vendor/.

%prep
%autosetup -n %{name}-%{version}

# Unpack vendored deps
tar -xzf %{SOURCE10}
tar -xzf %{SOURCE11}
tar -xzf %{SOURCE12}
tar -xzf %{SOURCE13}
tar -xzf %{SOURCE14}
tar -xzf %{SOURCE15}
tar -xzf %{SOURCE16}

%build
# hwdata.pc for aquamarine (Fedora's hwdata ships no pkg-config file)
mkdir -p pkgconfig
cat > pkgconfig/hwdata.pc << 'EOF'
prefix=/usr
datarootdir=${prefix}/share
pkgdatadir=${datarootdir}/hwdata

Name: hwdata
Description: Hardware identification databases
Version: 0.385
EOF

VENDOR_PREFIX="$(pwd)/vendor"
export PATH="$VENDOR_PREFIX/bin:$PATH"
export PKG_CONFIG_PATH="$VENDOR_PREFIX/lib64/pkgconfig:$VENDOR_PREFIX/share/pkgconfig:$(pwd)/pkgconfig:%{_libdir}/pkgconfig:%{_datadir}/pkgconfig"
export CMAKE_PREFIX_PATH="$VENDOR_PREFIX"

# 1) hyprwayland-scanner (build tool), hyprutils, hyprlang
for dep in hyprwayland-scanner-%{hyprwayland_scanner_ver} hyprutils-%{hyprutils_ver} hyprlang-%{hyprlang_ver}; do
  pushd $dep
  cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
    -DCMAKE_INSTALL_LIBDIR=lib64 -DBUILD_TESTING=OFF
  cmake --build build --parallel %{_smp_build_ncpus}
  cmake --install build
  popd
done

# 2) hyprland-protocols
pushd hyprland-protocols-%{hyprland_protocols_ver}
cmake -B build -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX"
cmake --install build
popd

# 3) aquamarine, hyprgraphics, hyprtoolkit (to build the share picker against)
for dep in aquamarine-%{aquamarine_ver} hyprgraphics-%{hyprgraphics_ver} hyprtoolkit-%{hyprtoolkit_ver}; do
  pushd $dep
  cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
    -DCMAKE_INSTALL_LIBDIR=lib64 -DBUILD_TESTING=OFF \
    -DOpenGL_GL_PREFERENCE=GLVND \
    -DOPENGL_opengl_LIBRARY=%{_libdir}/libOpenGL.so \
    -DOPENGL_gles3_LIBRARY=%{_libdir}/libGLESv2.so \
    -DOPENGL_GLES3_INCLUDE_DIR=/usr/include \
    -DOPENGL_egl_LIBRARY=%{_libdir}/libEGL.so \
    -DOPENGL_EGL_INCLUDE_DIR=/usr/include \
    -DOPENGL_INCLUDE_DIR=/usr/include
  cmake --build build --parallel %{_smp_build_ncpus}
  cmake --install build
  popd
done

# 4) xdg-desktop-portal-hyprland
# BUILD_TESTING off: skip the share picker data unit test
# RUNPATH points to hyprland's vendor libs (installed by hyprland package)
# rpath-link: resolves libhyprtoolkit's own deps (hyprlang) at link time only;
# $LDFLAGS repeated because -DCMAKE_EXE_LINKER_FLAGS replaces the env default
VENDOR_RPATH='%{_libexecdir}/hyprland/vendor/lib64'
cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_EXE_LINKER_FLAGS="$LDFLAGS -Wl,-rpath-link,$VENDOR_PREFIX/lib64" \
  -DBUILD_TESTING=OFF \
  -DCMAKE_INSTALL_RPATH="$VENDOR_RPATH" \
  -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
cmake --build build --parallel %{_smp_build_ncpus}

%install
DESTDIR=%{buildroot} cmake --install build

# Without RUNPATH the binaries can't find the vendored libs
for bin in %{buildroot}%{_libexecdir}/xdg-desktop-portal-hyprland %{buildroot}%{_bindir}/hyprland-share-picker; do
  readelf -d "$bin" | grep -q 'RUNPATH.*/vendor/lib64' || { echo "$bin: no vendor RUNPATH"; exit 1; }
done

%files
%license LICENSE
%doc README.md
# Portal daemon
%{_libexecdir}/xdg-desktop-portal-hyprland
# Share picker
%{_bindir}/hyprland-share-picker
# Portal config
%{_datadir}/xdg-desktop-portal/portals/hyprland.portal
# D-Bus service
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.hyprland.service
# Systemd user service
%{_userunitdir}/xdg-desktop-portal-hyprland.service

%changelog
* Sun Nov 01 2026 Asher Buk <AshBuk@users.noreply.github.com> - 1.5.0-1
- Update to xdg-desktop-portal-hyprland 1.5.0
- Bump hyprutils 0.14.2 -> 0.14.3, hyprland-protocols 0.7.0 -> 0.8.0

* Thu Sep 17 2026 Asher Buk <AshBuk@users.noreply.github.com> - 1.4.1-2
- Bump hyprutils 0.14.0 -> 0.14.2

* Thu Aug 06 2026 Asher Buk <AshBuk@users.noreply.github.com> - 1.4.1-1
- Update to xdg-desktop-portal-hyprland 1.4.1

* Thu Jul 23 2026 Asher Buk <AshBuk@users.noreply.github.com> - 1.4.0-1
- Update to xdg-desktop-portal-hyprland 1.4.0 (hyprutils 0.14.0 compat)

* Sun Jun 07 2026 Asher Buk <AshBuk@users.noreply.github.com> - 1.3.12-1
- Update to xdg-desktop-portal-hyprland 1.3.12

* Sun May 10 2026 Asher Buk <AshBuk@users.noreply.github.com> - 1.3.11-6
- Rebuild for Hyprland 0.55.0
- Bump hyprutils 0.11.0 -> 0.13.1, hyprwayland-scanner 0.4.5 -> 0.4.6

* Sat Feb 28 2026 Asher Buk <AshBuk@users.noreply.github.com> - 1.3.11-5
- Rebuild for Hyprland 0.54.0 compatibility
- Update hyprlang 0.6.7 -> 0.6.8
- Require hyprland >= 0.54.0

* Sat Jan 03 2026 Asher Buk <AshBuk@users.noreply.github.com> - 1.3.11-4
- Require hyprland >= 0.53.1 (patch release with bugfixes)

* Sat Jan 03 2026 Asher Buk <AshBuk@users.noreply.github.com> - 1.3.11-3
- Refactor: use %%global macros for all dependency versions

* Wed Dec 31 2025 Asher Buk <AshBuk@users.noreply.github.com> - 1.3.11-2
- Rebuild for Hyprland 0.53.0 compatibility
- Update hyprland-protocols 0.6.4 -> 0.7.0
- Require hyprland >= 0.53.0

* Thu Dec 25 2025 Asher Buk <AshBuk@users.noreply.github.com> - 1.3.11-1
- Initial package for Fedora 43 COPR
- Built with RUNPATH pointing to hyprland vendor libs
- Clean build without LD_LIBRARY_PATH hacks
