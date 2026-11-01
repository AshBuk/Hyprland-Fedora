# Copyright (c) 2025 Asher Buk
# SPDX-License-Identifier: MIT
# https://copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora/

# =============================================================================
# Version definitions (single source of truth)
# =============================================================================
%global hyprland_version        0.57.0
%global hyprland_release        1
# Commit of the release tag, reported by hyprctl version
%global hyprland_commit         0aa6745f705f2c4b0a5004eb019ef76e5bbdb426
%global hyprland_protocols_ver  0.8.0
%global hyprwayland_scanner_ver 0.4.6
%global hyprutils_ver           0.14.3
%global hyprlang_ver            0.6.8
%global hyprcursor_ver          0.1.13
%global hyprgraphics_ver        0.5.1
%global aquamarine_ver          0.15.1
%global hyprwire_ver            0.3.1
%global glaze_ver               7.2.0
%global hyprtoolkit_ver         0.6.0
# Lua 5.5 (Hyprland requires >= 5.5, Fedora ships 5.4)
%global lua_ver                 5.5.1
# Subpackage versions. Their Release embeds the hyprland build they link against,
# so every hyprland rebuild also ships rebuilt hyprlock/hypridle.
%global hyprlock_version        0.9.6
%global hyprlock_release        2
%global hypridle_version        0.1.8
%global hypridle_release        2

# Release on our GitHub mirror hosting udis86, glaze and the GCC 15 patch
%global build_assets_release    v0.54-fedora

# Vendored Hyprland libraries are private (/usr/libexec/hyprland/vendor/, reached via RUNPATH):
# don't advertise their sonames to the system, and don't require them from it.
# ABI pairing is expressed with hyprland-vendor(<lib>) = <version> provides instead.
%global __provides_exclude_from ^%{_libexecdir}/%{name}/vendor/.*$
%global __requires_exclude ^lib(aquamarine|hypr[a-z]+)\\.so

Name:           hyprland
Version:        %{hyprland_version}
Release:        %{hyprland_release}%{?dist}
Summary:        Dynamic tiling Wayland compositor
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/Hyprland

# Main source
Source0:        https://github.com/hyprwm/Hyprland/archive/refs/tags/v%{hyprland_version}.tar.gz#/%{name}-%{hyprland_version}.tar.gz

# Hyprland pinned deps (vendored, fixed versions)
Source10:       https://github.com/hyprwm/hyprland-protocols/archive/refs/tags/v%{hyprland_protocols_ver}.tar.gz#/hyprland-protocols-%{hyprland_protocols_ver}.tar.gz
# udis86 submodule (not in the GitHub tarball), patched for Python 3.x, with CMakeLists.txt
Source11:       https://github.com/AshBuk/Hyprland-Fedora/releases/download/%{build_assets_release}/udis86-hyprland.tar.gz
Source20:      https://github.com/hyprwm/hyprwayland-scanner/archive/refs/tags/v%{hyprwayland_scanner_ver}.tar.gz#/hyprwayland-scanner-%{hyprwayland_scanner_ver}.tar.gz
Source21:       https://github.com/hyprwm/hyprutils/archive/refs/tags/v%{hyprutils_ver}.tar.gz#/hyprutils-%{hyprutils_ver}.tar.gz
Source22:       https://github.com/hyprwm/hyprlang/archive/refs/tags/v%{hyprlang_ver}.tar.gz#/hyprlang-%{hyprlang_ver}.tar.gz
Source23:       https://github.com/hyprwm/hyprcursor/archive/refs/tags/v%{hyprcursor_ver}.tar.gz#/hyprcursor-%{hyprcursor_ver}.tar.gz
Source24:       https://github.com/hyprwm/hyprgraphics/archive/refs/tags/v%{hyprgraphics_ver}.tar.gz#/hyprgraphics-%{hyprgraphics_ver}.tar.gz
Source25:       https://github.com/hyprwm/aquamarine/archive/refs/tags/v%{aquamarine_ver}.tar.gz#/aquamarine-%{aquamarine_ver}.tar.gz
Source26:       https://github.com/hyprwm/hyprwire/archive/refs/tags/v%{hyprwire_ver}.tar.gz#/hyprwire-%{hyprwire_ver}.tar.gz
Source27:       https://www.lua.org/ftp/lua-%{lua_ver}.tar.gz
# hyprtoolkit: not used by Hyprland itself, shipped for xdg-desktop-portal-hyprland's picker
Source28:       https://github.com/hyprwm/hyprtoolkit/archive/refs/tags/v%{hyprtoolkit_ver}.tar.gz#/hyprtoolkit-%{hyprtoolkit_ver}.tar.gz

# glaze JSON library (for start-hyprland, mock chroot has no network for FetchContent)
# Using our release mirror to ensure availability
Source30:       https://github.com/AshBuk/Hyprland-Fedora/releases/download/%{build_assets_release}/glaze-%{glaze_ver}.tar.gz

# Subpackage sources
Source40:       https://github.com/hyprwm/hyprlock/archive/refs/tags/v%{hyprlock_version}.tar.gz#/hyprlock-%{hyprlock_version}.tar.gz
Source41:       https://github.com/hyprwm/hypridle/archive/refs/tags/v%{hypridle_version}.tar.gz#/hypridle-%{hypridle_version}.tar.gz

# Downstream compatibility patches (hosted in our release mirror)
# Fedora 43 (GCC 15) lacks std::ranges::starts_with and std::string::subview
# (libstdc++ ships them from GCC 16). Drop once Fedora 43 reaches EOL.
# gcc15_patch_ver: Hyprland version the patch was cut against.
%global gcc15_patch_ver 0.57.0
Patch0:         https://github.com/AshBuk/Hyprland-Fedora/releases/download/%{build_assets_release}/hyprland-%{gcc15_patch_ver}-gcc15.patch

# Build dependencies
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3

# Library dependencies (system)
BuildRequires:  cairo-devel
BuildRequires:  glslang-devel
BuildRequires:  hwdata
BuildRequires:  libdisplay-info-devel
BuildRequires:  libdrm-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  libglvnd-devel
BuildRequires:  libglvnd-gles
BuildRequires:  libinput-devel >= 1.29
# libeis for input-capture protocol
BuildRequires:  libeis-devel
# readline for hyprctl Lua REPL
BuildRequires:  readline-devel
BuildRequires:  lcms2-devel
BuildRequires:  libjxl-devel
BuildRequires:  libwebp-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  pango-devel
BuildRequires:  pixman-devel
BuildRequires:  pugixml-devel
BuildRequires:  re2-devel
BuildRequires:  scdoc
BuildRequires:  libseat-devel
BuildRequires:  systemd-devel
BuildRequires:  tomlplusplus-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel >= 1.35
BuildRequires:  libzip-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  file-devel
BuildRequires:  xcb-util-errors-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xorg-x11-server-Xwayland
BuildRequires:  glib2-devel
BuildRequires:  libuuid-devel
# libffi for hyprwire
BuildRequires:  libffi-devel
# muparser for math expressions in config
BuildRequires:  muParser-devel
# libcanberra for bell sounds
BuildRequires:  libcanberra-devel
# iniparser, abseil for hyprtoolkit
BuildRequires:  iniparser-devel
BuildRequires:  abseil-cpp-devel
# Subpackage deps (hyprlock: PAM auth); D-Bus IPC for hyprlock, hypridle and Hyprland rtkit
BuildRequires:  pam-devel
BuildRequires:  sdbus-cpp-devel >= 2.0.0

# Runtime deps invisible to automatic soname Requires (linked libraries are added by RPM)
# hwdata: PNP/PCI ID databases read by aquamarine; Xwayland: spawned for X11 clients
Requires:       hwdata
Requires:       xorg-x11-server-Xwayland
# rtkit grants Hyprland realtime scheduling over D-Bus
Recommends:     rtkit
# Vendored library versions, for packages linked against them via RUNPATH
Provides:       hyprland-vendor(aquamarine) = %{aquamarine_ver}
Provides:       hyprland-vendor(hyprcursor) = %{hyprcursor_ver}
Provides:       hyprland-vendor(hyprgraphics) = %{hyprgraphics_ver}
Provides:       hyprland-vendor(hyprlang) = %{hyprlang_ver}
Provides:       hyprland-vendor(hyprtoolkit) = %{hyprtoolkit_ver}
Provides:       hyprland-vendor(hyprutils) = %{hyprutils_ver}
Provides:       hyprland-vendor(hyprwire) = %{hyprwire_ver}
# Subpackages (installed by default via weak deps, removable individually)
Recommends:     hyprlock
Recommends:     hypridle
# Session manager for the hyprland-uwsm.desktop session
Suggests:       uwsm

%description
Hyprland is a dynamic tiling Wayland compositor with modern Wayland features,
high customizability, IPC and visual effects.

This is a COPR build for Fedora, with hyprlock and hypridle as subpackages.
Pinned Hyprland dependencies are built from fixed-version sources and installed
into a private vendor prefix to avoid polluting system /usr/lib64.

# -----------------------------------------------------------------------------
# Subpackage: hyprlock
# -----------------------------------------------------------------------------
%package -n hyprlock
Version:        %{hyprlock_version}
Release:        %{hyprlock_release}.%{hyprland_version}.%{hyprland_release}%{?dist}
Summary:        Hyprland screen lock utility
License:        BSD-3-Clause
Requires:       hyprland%{?_isa} = %{hyprland_version}-%{hyprland_release}%{?dist}
Requires:       pam

%description -n hyprlock
hyprlock is a screen lock utility for Hyprland. It uses the ext-session-lock
Wayland protocol for secure screen locking, supports PAM authentication,
and provides a customizable lock screen with widgets and effects.

# -----------------------------------------------------------------------------
# Subpackage: hypridle
# -----------------------------------------------------------------------------
%package -n hypridle
Version:        %{hypridle_version}
Release:        %{hypridle_release}.%{hyprland_version}.%{hyprland_release}%{?dist}
Summary:        Hyprland idle daemon
License:        BSD-3-Clause
Requires:       hyprland%{?_isa} = %{hyprland_version}-%{hyprland_release}%{?dist}

%description -n hypridle
hypridle is Hyprland's idle daemon. It monitors user activity and triggers
actions on inactivity timeouts, such as locking the screen, turning off
the display, or suspending the system.

%prep
# -N: Patch0 is applied only on Fedora <= 43 (GCC 15)
%autosetup -N -n Hyprland-%{hyprland_version}
%if 0%{?fedora} <= 43
%patch -P 0 -p1
%endif

# udis86 submodule (not in the GitHub tarball)
rm -rf subprojects/udis86
tar -xzf %{SOURCE11} -C subprojects

# Unpack vendored deps in top build dir
tar -xzf %{SOURCE10}
tar -xzf %{SOURCE20}
tar -xzf %{SOURCE21}
tar -xzf %{SOURCE22}
tar -xzf %{SOURCE23}
tar -xzf %{SOURCE24}
tar -xzf %{SOURCE25}
tar -xzf %{SOURCE26}
tar -xzf %{SOURCE27}
tar -xzf %{SOURCE28}

# Unpack glaze (for start-hyprland, mock chroot has no network for FetchContent)
tar -xzf %{SOURCE30}

# Unpack subpackage sources
tar -xzf %{SOURCE40}
tar -xzf %{SOURCE41}

%build
# hwdata.pc for pkg-config consumers
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

# OpenGL/GLES3/EGL detection: CMake FindOpenGL needs explicit hints for libglvnd on Fedora
# libglvnd provides libGLESv2.so (GLES2/3), libEGL.so, and libOpenGL.so
GL_FLAGS="-DOpenGL_GL_PREFERENCE=GLVND \
  -DOPENGL_opengl_LIBRARY=%{_libdir}/libOpenGL.so \
  -DOPENGL_gles3_LIBRARY=%{_libdir}/libGLESv2.so \
  -DOPENGL_GLES3_INCLUDE_DIR=/usr/include \
  -DOPENGL_egl_LIBRARY=%{_libdir}/libEGL.so \
  -DOPENGL_EGL_INCLUDE_DIR=/usr/include \
  -DOPENGL_INCLUDE_DIR=/usr/include"

# 1) hyprwayland-scanner (build tool) and hypr* libraries, in dependency order
# (hyprwire: IPC library + scanner for hyprctl)
for dep in hyprwayland-scanner-%{hyprwayland_scanner_ver} hyprutils-%{hyprutils_ver} hyprlang-%{hyprlang_ver} \
           hyprcursor-%{hyprcursor_ver} hyprgraphics-%{hyprgraphics_ver} hyprwire-%{hyprwire_ver}; do
  pushd $dep
  cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
    -DCMAKE_INSTALL_LIBDIR=lib64
  cmake --build build --parallel %{_smp_build_ncpus}
  cmake --install build
  popd
done

# 2) aquamarine, hyprtoolkit (for the portal's share picker)
for dep in aquamarine-%{aquamarine_ver} hyprtoolkit-%{hyprtoolkit_ver}; do
  pushd $dep
  cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
    -DCMAKE_INSTALL_LIBDIR=lib64 \
    $GL_FLAGS
  cmake --build build --parallel %{_smp_build_ncpus}
  cmake --install build
  popd
done

# 3) hyprland-protocols
pushd hyprland-protocols-%{hyprland_protocols_ver}
cmake -B build -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX"
cmake --install build
popd

# 4) glaze (header-only JSON library, install to vendor prefix for find_package)
pushd glaze-%{glaze_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
  -Dglaze_DEVELOPER_MODE=OFF -DBUILD_TESTING=OFF
cmake --install build
popd

# 5) Lua 5.5 (static, -fPIC; linked into Hyprland binary, no runtime dep)
pushd lua-%{lua_ver}
make MYCFLAGS="-fPIC -fvisibility=hidden" linux %{?_smp_mflags}
make install INSTALL_TOP="$VENDOR_PREFIX" INSTALL_LIB="$VENDOR_PREFIX/lib64"
mkdir -p "$VENDOR_PREFIX/lib64/pkgconfig"
cat > "$VENDOR_PREFIX/lib64/pkgconfig/lua5.5.pc" << EOF
Name: Lua
Description: An Extensible Extension Language
Version: %{lua_ver}
Libs: -L$VENDOR_PREFIX/lib64 -llua -lm -ldl
Cflags: -I$VENDOR_PREFIX/include
EOF
popd

# 6) Hyprland, including start-hyprland (add_subdirectory)
# BUILD_TESTING off: hyprtester's plugin Makefile doesn't support vendored deps
# NO_HYPRPM: plugin builds need the vendored headers and .pc files, which aren't shipped
# RPATH set at build time: patchelf corrupts the ELF program headers
# Add vendor include path for glaze headers (start-hyprland uses direct #include, not find_package)
# Hyprland CMakeLists reads these env vars and falls back to "unknown" otherwise (tarball has no .git)
export GIT_TAG="v%{hyprland_version}"
export GIT_BRANCH="main"
export GIT_COMMIT_HASH="%{hyprland_commit}"
export GIT_COMMIT_DATE="$(date -u -d "@${SOURCE_DATE_EPOCH:-$(date +%s)}" +%Y-%m-%d)"
export GIT_DIRTY=""
export GIT_COMMITS="0"
VENDOR_RPATH='%{_libexecdir}/hyprland/vendor/lib64'
cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_CXX_FLAGS="$CXXFLAGS -I$VENDOR_PREFIX/include" \
  -DBUILD_TESTING=OFF \
  -DNO_HYPRPM=ON \
  -DCMAKE_INSTALL_RPATH="$VENDOR_RPATH" \
  -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON \
  $GL_FLAGS
cmake --build build --parallel %{_smp_build_ncpus}

# 7) hyprlock (screen lock utility, needs OpenGL/EGL)
pushd hyprlock-%{hyprlock_version}
cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_RPATH="$VENDOR_RPATH" \
  -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON \
  $GL_FLAGS
cmake --build build --parallel %{_smp_build_ncpus}
popd

# 8) hypridle (idle daemon, no OpenGL needed)
pushd hypridle-%{hypridle_version}
cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_RPATH="$VENDOR_RPATH" \
  -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
cmake --build build --parallel %{_smp_build_ncpus}
popd

%check
# Tests disabled: hyprtester doesn't support vendored deps

%install
VENDOR_PREFIX="$(pwd)/vendor"

# Install Hyprland binaries/data (includes start-hyprland via add_subdirectory)
DESTDIR=%{buildroot} cmake --install build

# Upstream installs the session target to ${CMAKE_INSTALL_LIBDIR} (lib64), where systemd doesn't look
install -d %{buildroot}%{_userunitdir}
mv %{buildroot}%{_libdir}/systemd/user/hyprland-session.target %{buildroot}%{_userunitdir}/
rmdir %{buildroot}%{_libdir}/systemd/user %{buildroot}%{_libdir}/systemd

# Relative alias (upstream installs an absolute symlink)
ln -sf Hyprland %{buildroot}%{_bindir}/hyprland

# Install vendored runtime libs into private prefix
VENDOR_DST=%{buildroot}%{_libexecdir}/%{name}/vendor
install -d "$VENDOR_DST/lib64"
cp -a "$VENDOR_PREFIX"/lib64/lib*.so* "$VENDOR_DST/lib64/"

# Install hyprlock and hypridle
DESTDIR=%{buildroot} cmake --install hyprlock-%{hyprlock_version}/build
DESTDIR=%{buildroot} cmake --install hypridle-%{hypridle_version}/build

# Without RUNPATH the binaries can't find the vendored libs
for bin in Hyprland hyprctl start-hyprland hyprlock hypridle; do
  readelf -d %{buildroot}%{_bindir}/$bin | grep -q 'RUNPATH.*/vendor/lib64' || { echo "$bin: no vendor RUNPATH"; exit 1; }
done

# Plugin development files, unusable without the vendored headers
rm -rf %{buildroot}%{_includedir}/hyprland %{buildroot}%{_datadir}/pkgconfig/hyprland.pc

%files
%license LICENSE
%doc README.md
# Binaries
%{_bindir}/Hyprland
%{_bindir}/hyprland
%{_bindir}/hyprctl
# start-hyprland watchdog binary
%{_bindir}/start-hyprland
# Vendored libraries
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/vendor/
# Desktop entries
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/wayland-sessions/hyprland-uwsm.desktop
# Systemd user session target
%{_userunitdir}/hyprland-session.target
# Data files (exclude subpackage configs to avoid ownership conflicts)
%{_datadir}/hypr/
%exclude %{_datadir}/hypr/hyprlock.conf
%exclude %{_datadir}/hypr/hypridle.conf
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
# Man pages
%{_mandir}/man1/Hyprland.1*
%{_mandir}/man1/hyprctl.1*

%files -n hyprlock
%license hyprlock-%{hyprlock_version}/LICENSE
%{_bindir}/hyprlock
%config(noreplace) %{_sysconfdir}/pam.d/hyprlock
%{_datadir}/hypr/hyprlock.conf

%files -n hypridle
%license hypridle-%{hypridle_version}/LICENSE
%{_bindir}/hypridle
%{_userunitdir}/hypridle.service
%{_datadir}/hypr/hypridle.conf

%changelog
* Sun Nov 01 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.57.0-1
- Update to Hyprland 0.57.0
- Bump hyprutils 0.14.2 -> 0.14.3, hyprland-protocols 0.7.0 -> 0.8.0, Lua 5.5.0 -> 5.5.1
- Add hyprtoolkit 0.6.0

* Thu Sep 17 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.56.2-2
- Bump aquamarine 0.14.0 -> 0.15.1 (ABI break, SOVERSION 13 -> 14)
- Bump hyprutils 0.14.0 -> 0.14.2

* Thu Aug 06 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.56.2-1
- Update to Hyprland 0.56.2
- Bump aquamarine 0.13.0 -> 0.14.0 (ABI break, SOVERSION 12 -> 13)
- Bump hypridle 0.1.7 -> 0.1.8

* Thu Jul 23 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.56.0-1
- Update to Hyprland 0.56.0, Aquamarine 0.12.0 -> 0.13.0
- Bump glaze 7.0.0 -> 7.2.0 to match upstream's tested build
- Bump hyprutils 0.13.1 -> 0.14.0 (fixes virtual-inheritance cast crash on layer surfaces)
- Bump hyprlock 0.9.5 -> 0.9.6 (hyprutils 0.14.0 compat)

* Sun Jun 14 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.55.4-1
- Update to Hyprland 0.55.4 (patch release)

* Sun Jun 07 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.55.3-1
- Update to Hyprland 0.55.3 (patch release)
- Bump aquamarine 0.11.0 -> 0.12.0 (ABI changes; rebuilt against vendored lib)

* Mon May 18 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.55.2-1
- Update to Hyprland 0.55.2 (patch release)

* Thu May 14 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.55.1-1
- Update to Hyprland 0.55.1 (patch release)

* Sun May 10 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.55.0-2
- Hide vendored Lua symbols to prevent clash with system liblua-5.4

* Sun May 10 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.55.0-1
- Update to Hyprland 0.55.0
- Bump hyprutils 0.11.0 -> 0.13.1, hyprgraphics 0.5.0 -> 0.5.1
- Bump hyprwire 0.3.0 -> 0.3.1, hyprwayland-scanner 0.4.5 -> 0.4.6, hyprlock 0.9.3 -> 0.9.5
- Vendor Lua 5.5.0 (Hyprland 0.55.0 requires it; Fedora 43/44 ship 5.4)

* Mon Apr 27 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.54.3-3
- Bump aquamarine to 0.11.0

* Sun Apr 06 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.54.3-2
- Add hyprlock 0.9.3 and hypridle 0.1.7 as subpackages
- Vendored libs shared with main Hyprland build

* Sun Mar 29 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.54.3-1
- Update to Hyprland 0.54.3 (patch release)

* Thu Mar 13 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.54.2-1
- Update to Hyprland 0.54.2 (patch release)

* Mon Mar 03 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.54.1-1
- Update to Hyprland 0.54.1 (patch release)

* Sat Jan 31 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.53.3-1
- Update to Hyprland 0.53.3 (patch release)

* Sat Jan 03 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.53.0-4
- Update to Hyprland 0.53.1 (patch release with bugfixes)
- Refactor: use %%global macros for all dependency versions
- Refactor: create-srpm.sh now parses versions from spec file

* Wed Dec 31 2025 Asher Buk <AshBuk@users.noreply.github.com> - 0.53.0-3
- Update to Hyprland 0.53.0

* Thu Dec 18 2025 Asher Buk <AshBuk@users.noreply.github.com> - 0.52.2-2
- Fix ELF corruption: set RPATH at build time via CMAKE_INSTALL_RPATH
- Remove patchelf post-install which was corrupting ELF program headers
- Binaries are now properly dynamically linked

* Mon Dec 15 2025 Asher Buk <AshBuk@users.noreply.github.com> - 0.52.2-1
- Single-package COPR build for Fedora 43
- Pinned Hyprland deps built from fixed-version sources
- Vendored runtime libs in /usr/libexec to avoid system library conflicts
