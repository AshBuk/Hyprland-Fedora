# Copyright (c) 2025 Asher Buk
# SPDX-License-Identifier: MIT
# https://copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora/

# =============================================================================
# Version definitions (single source of truth)
# =============================================================================
%global hyprland_version        0.55.0
%global hyprland_protocols_ver  0.7.0
%global hyprwayland_scanner_ver 0.4.6
%global hyprutils_ver           0.13.1
%global hyprlang_ver            0.6.8
%global hyprcursor_ver          0.1.13
%global hyprgraphics_ver        0.5.1
%global aquamarine_ver          0.11.0
%global hyprwire_ver            0.3.1
%global glaze_ver               7.0.0
# Subpackage versions
%global hyprlock_version        0.9.5
%global hypridle_version        0.1.7

# Build assets release (udis86, glaze tarballs - only changes when these deps update)
%global build_assets_release    v0.54-fedora

# Exclude auto-requires for vendored Hyprland libraries
# These are built from source and installed in /usr/libexec/hyprland/vendor/
%global __requires_exclude pkgconfig\\((aquamarine|hyprutils|hyprlang|hyprcursor|hyprgraphics|hyprwayland-scanner|hyprland-protocols|hyprwire)\\)

Name:           hyprland
Version:        %{hyprland_version}
Release:        1%{?dist}
Summary:        Dynamic tiling Wayland compositor
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/Hyprland

# Main source
Source0:        https://github.com/hyprwm/Hyprland/archive/refs/tags/v%{hyprland_version}.tar.gz#/%{name}-%{hyprland_version}.tar.gz

# Git submodules (not included in GitHub tarball)
Source10:       https://github.com/hyprwm/hyprland-protocols/archive/refs/tags/v%{hyprland_protocols_ver}.tar.gz#/hyprland-protocols-%{hyprland_protocols_ver}.tar.gz
# udis86 from Hyprland subprojects (patched for Python 3.x, with CMakeLists.txt)
Source11:       https://github.com/AshBuk/Hyprland-Fedora/releases/download/%{build_assets_release}/udis86-hyprland.tar.gz

# Hyprland pinned deps (vendored, fixed versions)
Source20:       https://github.com/hyprwm/hyprwayland-scanner/archive/refs/tags/v%{hyprwayland_scanner_ver}.tar.gz#/hyprwayland-scanner-%{hyprwayland_scanner_ver}.tar.gz
Source21:       https://github.com/hyprwm/hyprutils/archive/refs/tags/v%{hyprutils_ver}.tar.gz#/hyprutils-%{hyprutils_ver}.tar.gz
Source22:       https://github.com/hyprwm/hyprlang/archive/refs/tags/v%{hyprlang_ver}.tar.gz#/hyprlang-%{hyprlang_ver}.tar.gz
Source23:       https://github.com/hyprwm/hyprcursor/archive/refs/tags/v%{hyprcursor_ver}.tar.gz#/hyprcursor-%{hyprcursor_ver}.tar.gz
Source24:       https://github.com/hyprwm/hyprgraphics/archive/refs/tags/v%{hyprgraphics_ver}.tar.gz#/hyprgraphics-%{hyprgraphics_ver}.tar.gz
Source25:       https://github.com/hyprwm/aquamarine/archive/refs/tags/v%{aquamarine_ver}.tar.gz#/aquamarine-%{aquamarine_ver}.tar.gz
# hyprwire IPC library (includes hyprwire-scanner for hyprctl)
Source26:       https://github.com/hyprwm/hyprwire/archive/refs/tags/v%{hyprwire_ver}.tar.gz#/hyprwire-%{hyprwire_ver}.tar.gz

# glaze JSON library (for hyprpm, mock chroot has no network for FetchContent)
# Using our release mirror to ensure availability
Source30:       https://github.com/AshBuk/Hyprland-Fedora/releases/download/%{build_assets_release}/glaze-%{glaze_ver}.tar.gz

# Subpackage sources
Source40:       https://github.com/hyprwm/hyprlock/archive/refs/tags/v%{hyprlock_version}.tar.gz#/hyprlock-%{hyprlock_version}.tar.gz
Source41:       https://github.com/hyprwm/hypridle/archive/refs/tags/v%{hypridle_version}.tar.gz#/hypridle-%{hypridle_version}.tar.gz

# Build dependencies
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3

# Library dependencies (system)
BuildRequires:  cairo-devel
BuildRequires:  glm-devel
BuildRequires:  glslang-devel
BuildRequires:  hwdata
BuildRequires:  libdisplay-info-devel
BuildRequires:  libdrm-devel
BuildRequires:  libepoxy-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  libglvnd-devel
BuildRequires:  libglvnd-gles
BuildRequires:  libinput-devel
BuildRequires:  libjxl-devel
BuildRequires:  libliftoff-devel
BuildRequires:  libspng-devel
BuildRequires:  libwebp-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libxcvt-devel
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
BuildRequires:  xcb-util-devel
BuildRequires:  xcb-util-errors-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-renderutil-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xorg-x11-server-Xwayland
BuildRequires:  libXfont2-devel
BuildRequires:  xkeyboard-config
BuildRequires:  glib2-devel
BuildRequires:  libuuid-devel
# NEW: libffi for hyprwire
BuildRequires:  libffi-devel
# NEW: muparser for math expressions in config (0.53.0)
BuildRequires:  muParser-devel
# Subpackage deps (hyprlock: PAM auth, hyprlock+hypridle: D-Bus IPC)
BuildRequires:  pam-devel
BuildRequires:  sdbus-cpp-devel >= 2.0.0

# Runtime deps (system)
Requires:       cairo
Requires:       hwdata
Requires:       libdisplay-info
Requires:       libdrm
Requires:       libepoxy
Requires:       mesa-libgbm
Requires:       libinput
Requires:       libjxl
Requires:       libliftoff
Requires:       libspng
Requires:       libwebp
Requires:       libxcb
Requires:       libXcursor
Requires:       libxcvt
Requires:       libxkbcommon
Requires:       pango
Requires:       pixman
Requires:       pugixml
Requires:       re2
Requires:       libseat
Requires:       libwayland-client
Requires:       libwayland-server
Requires:       libzip
Requires:       librsvg2
Requires:       xcb-util
Requires:       xcb-util-errors
Requires:       xcb-util-image
Requires:       xcb-util-renderutil
Requires:       xcb-util-wm
Requires:       xorg-x11-server-Xwayland
# NEW: libffi for hyprwire runtime
Requires:       libffi
# NEW: muparser for math expressions in config (0.53.0)
Requires:       muParser
# Subpackages (installed by default via weak deps, removable individually)
Recommends:     hyprlock
Recommends:     hypridle

%description
Hyprland is a dynamic tiling Wayland compositor with modern Wayland features,
high customizability, IPC, plugins, and visual effects.

This is a single-package COPR build for Fedora.
Pinned Hyprland dependencies are built from fixed-version sources and installed
into a private vendor prefix to avoid polluting system /usr/lib64.

# -----------------------------------------------------------------------------
# Subpackage: hyprlock
# -----------------------------------------------------------------------------
%package -n hyprlock
Version:        %{hyprlock_version}
Summary:        Hyprland screen lock utility
License:        BSD-3-Clause
Requires:       hyprland >= %{hyprland_version}
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
Summary:        Hyprland idle daemon
License:        BSD-3-Clause
Requires:       hyprland >= %{hyprland_version}

%description -n hypridle
hypridle is Hyprland's idle daemon. It monitors user activity and triggers
actions on inactivity timeouts, such as locking the screen, turning off
the display, or suspending the system.

%prep
%autosetup -n Hyprland-%{hyprland_version}

# Unpack submodules into correct locations
rm -rf subprojects/hyprland-protocols subprojects/udis86
tar -xzf %{SOURCE10} -C subprojects
mv subprojects/hyprland-protocols-%{hyprland_protocols_ver} subprojects/hyprland-protocols
# udis86 from Hyprland subprojects (patched for Python 3.x, includes CMakeLists.txt)
tar -xzf %{SOURCE11} -C subprojects

# Unpack vendored deps in top build dir
tar -xzf %{SOURCE20}
tar -xzf %{SOURCE21}
tar -xzf %{SOURCE22}
tar -xzf %{SOURCE23}
tar -xzf %{SOURCE24}
tar -xzf %{SOURCE25}
tar -xzf %{SOURCE26}

# Unpack glaze (for hyprpm, mock chroot has no network for FetchContent)
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
export PKG_CONFIG_PATH="$VENDOR_PREFIX/lib64/pkgconfig:$VENDOR_PREFIX/lib/pkgconfig:$(pwd)/pkgconfig:%{_libdir}/pkgconfig:%{_datadir}/pkgconfig"
export CMAKE_PREFIX_PATH="$VENDOR_PREFIX"

# GCC 15 in Fedora 43 errors on zero-length arrays (generated by hyprwayland-scanner)
# Must pass flags explicitly to cmake - env vars don't work reliably in mock chroot
# Use RPM standard optflags + -fpermissive for protocol code
GCC15_CXXFLAGS="%{optflags} -fpermissive"

# OpenGL/GLES3/EGL detection: CMake FindOpenGL needs explicit hints for libglvnd on Fedora
# libglvnd provides libGLESv2.so (GLES2/3), libEGL.so, and libOpenGL.so
export OPENGL_opengl_LIBRARY=%{_libdir}/libOpenGL.so
export OPENGL_gles3_LIBRARY=%{_libdir}/libGLESv2.so
export OPENGL_GLES3_INCLUDE_DIR=/usr/include
export OPENGL_egl_LIBRARY=%{_libdir}/libEGL.so
export OPENGL_EGL_INCLUDE_DIR=/usr/include
export OPENGL_INCLUDE_DIR=/usr/include

# 1) hyprwayland-scanner (build tool)
pushd hyprwayland-scanner-%{hyprwayland_scanner_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
  -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# Verify hyprwayland-scanner cmake config is installed
ls -la "$VENDOR_PREFIX/lib64/cmake/hyprwayland-scanner/" || ls -la "$VENDOR_PREFIX/lib/cmake/hyprwayland-scanner/" || true

# 2) hyprutils
pushd hyprutils-%{hyprutils_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# 3) hyprlang
pushd hyprlang-%{hyprlang_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# 4) hyprcursor
pushd hyprcursor-%{hyprcursor_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# 5) hyprgraphics
pushd hyprgraphics-%{hyprgraphics_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# 6) aquamarine (needs -fpermissive for generated protocol code with zero-size arrays)
# Explicitly set hyprwayland-scanner_DIR since CMAKE_PREFIX_PATH may not work in mock chroot
# Also need explicit OpenGL/EGL paths for libglvnd on Fedora
pushd aquamarine-%{aquamarine_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" -DCMAKE_INSTALL_LIBDIR=lib64 \
  -Dhyprwayland-scanner_DIR="$VENDOR_PREFIX/lib64/cmake/hyprwayland-scanner" \
  -DCMAKE_CXX_FLAGS="$GCC15_CXXFLAGS" \
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

# 7) hyprwire (IPC library + scanner for hyprctl)
pushd hyprwire-%{hyprwire_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# 8) hyprland-protocols
pushd subprojects/hyprland-protocols
meson setup build --prefix="$VENDOR_PREFIX"
ninja -C build
ninja -C build install
popd

# 9) glaze (header-only JSON library, install to vendor prefix for find_package)
pushd glaze-%{glaze_ver}
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
  -Dglaze_DEVELOPER_MODE=OFF -DBUILD_TESTING=OFF
cmake --install build
popd

# 10) Hyprland (needs -fpermissive for generated protocol code with zero-size arrays)
# Disable BUILD_TESTING to skip hyprtester (its plugin Makefile doesn't support vendored deps)
# Set RPATH at build time to avoid patchelf corruption issues
# Add vendor include path for glaze headers (start-hyprland uses direct #include, not find_package)
# Hyprland CMakeLists reads these env vars and falls back to "unknown" otherwise (tarball has no .git)
export GIT_TAG="v%{hyprland_version}"
export GIT_BRANCH="main"
export GIT_COMMIT_HASH="release-v%{hyprland_version}"
export GIT_COMMIT_MESSAGE="Release v%{hyprland_version}"
export GIT_COMMIT_DATE="$(date -u -d "@${SOURCE_DATE_EPOCH:-$(date +%s)}" +%Y-%m-%d)"
export GIT_DIRTY=""
export GIT_COMMITS="0"
VENDOR_RPATH='$ORIGIN/../libexec/hyprland/vendor/lib64:$ORIGIN/../libexec/hyprland/vendor/lib'
cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" \
  -Dhyprwayland-scanner_DIR="$VENDOR_PREFIX/lib64/cmake/hyprwayland-scanner" \
  -DCMAKE_CXX_FLAGS="$GCC15_CXXFLAGS -I$VENDOR_PREFIX/include" \
  -DBUILD_TESTING=OFF \
  -DCMAKE_INSTALL_RPATH="$VENDOR_RPATH" \
  -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON \
  -DOPENGL_opengl_LIBRARY=%{_libdir}/libOpenGL.so \
  -DOPENGL_gles3_LIBRARY=%{_libdir}/libGLESv2.so \
  -DOPENGL_GLES3_INCLUDE_DIR=/usr/include \
  -DOPENGL_egl_LIBRARY=%{_libdir}/libEGL.so \
  -DOPENGL_EGL_INCLUDE_DIR=/usr/include \
  -DOPENGL_INCLUDE_DIR=/usr/include
cmake --build build --parallel %{_smp_build_ncpus}

# Note: start-hyprland is built via add_subdirectory(start) in main CMakeLists.txt
# No separate build step needed - it inherits glaze and other settings from parent

# 11) hyprlock (screen lock utility, needs OpenGL/EGL)
SUBPKG_RPATH='%{_libexecdir}/hyprland/vendor/lib64:%{_libexecdir}/hyprland/vendor/lib'
pushd hyprlock-%{hyprlock_version}
cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" \
  -Dhyprwayland-scanner_DIR="$VENDOR_PREFIX/lib64/cmake/hyprwayland-scanner" \
  -DCMAKE_CXX_FLAGS="$GCC15_CXXFLAGS" \
  -DCMAKE_INSTALL_RPATH="$SUBPKG_RPATH" \
  -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON \
  -DOpenGL_GL_PREFERENCE=GLVND \
  -DOPENGL_opengl_LIBRARY=%{_libdir}/libOpenGL.so \
  -DOPENGL_gles3_LIBRARY=%{_libdir}/libGLESv2.so \
  -DOPENGL_GLES3_INCLUDE_DIR=/usr/include \
  -DOPENGL_egl_LIBRARY=%{_libdir}/libEGL.so \
  -DOPENGL_EGL_INCLUDE_DIR=/usr/include \
  -DOPENGL_INCLUDE_DIR=/usr/include
cmake --build build --parallel %{_smp_build_ncpus}
popd

# 12) hypridle (idle daemon, no OpenGL needed)
pushd hypridle-%{hypridle_version}
cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" \
  -Dhyprwayland-scanner_DIR="$VENDOR_PREFIX/lib64/cmake/hyprwayland-scanner" \
  -DCMAKE_CXX_FLAGS="$GCC15_CXXFLAGS" \
  -DCMAKE_INSTALL_RPATH="$SUBPKG_RPATH" \
  -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
cmake --build build --parallel %{_smp_build_ncpus}
popd

%check
# Tests disabled: hyprtester doesn't support vendored deps

%install
VENDOR_PREFIX="$(pwd)/vendor"

# Install Hyprland binaries/data (includes start-hyprland via add_subdirectory)
DESTDIR=%{buildroot} cmake --install build

# Ensure "hyprland" alias exists (some setups expect it)
ln -sf Hyprland %{buildroot}%{_bindir}/hyprland

# Ensure session desktop entry exists
install -d %{buildroot}%{_datadir}/wayland-sessions
if [ ! -f %{buildroot}%{_datadir}/wayland-sessions/hyprland.desktop ]; then
cat > %{buildroot}%{_datadir}/wayland-sessions/hyprland.desktop << 'EOF'
[Desktop Entry]
Name=Hyprland
Comment=Dynamic tiling Wayland compositor
Exec=Hyprland
Type=Application
DesktopNames=Hyprland
EOF
fi

# Install vendored runtime libs into private prefix
VENDOR_DST=%{buildroot}%{_libexecdir}/%{name}/vendor
install -d "$VENDOR_DST/lib64" "$VENDOR_DST/lib"
cp -a "$VENDOR_PREFIX"/lib64/lib*.so* "$VENDOR_DST/lib64/" 2>/dev/null || true
cp -a "$VENDOR_PREFIX"/lib/lib*.so*   "$VENDOR_DST/lib/"   2>/dev/null || true

# Install hyprlock and hypridle
DESTDIR=%{buildroot} cmake --install hyprlock-%{hyprlock_version}/build
DESTDIR=%{buildroot} cmake --install hypridle-%{hypridle_version}/build

# Verify RPATH is set correctly (was set at build time via CMAKE_INSTALL_RPATH)
# Using patchelf post-install can corrupt ELF program headers, so we set RPATH at build time
echo "Verifying RPATH on installed binaries:"
for bin in %{buildroot}%{_bindir}/Hyprland %{buildroot}%{_bindir}/hyprctl %{buildroot}%{_bindir}/hyprpm %{buildroot}%{_bindir}/start-hyprland %{buildroot}%{_bindir}/hyprlock %{buildroot}%{_bindir}/hypridle; do
  [ -x "$bin" ] || continue
  echo "  $(basename $bin): $(readelf -d "$bin" 2>/dev/null | grep -E 'RPATH|RUNPATH' || echo 'no RPATH set')"
done

# Remove glaze files (header-only library, not needed at runtime)
rm -rf %{buildroot}%{_includedir}/glaze
rm -rf %{buildroot}%{_datadir}/glaze

%files
%license LICENSE
%doc README.md
# Binaries
%{_bindir}/Hyprland
%{_bindir}/hyprland
%{_bindir}/hyprctl
%{_bindir}/hyprpm
# NEW: start-hyprland watchdog binary
%{_bindir}/start-hyprland
# Vendored libraries
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/vendor/
# Desktop entries
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/wayland-sessions/hyprland-uwsm.desktop
# Data files (exclude subpackage configs to avoid ownership conflicts)
%{_datadir}/hypr/
%exclude %{_datadir}/hypr/hyprlock.conf
%exclude %{_datadir}/hypr/hypridle.conf
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
# Development headers
%{_includedir}/hyprland/
# pkg-config
%{_datadir}/pkgconfig/hyprland.pc
# Man pages
%{_mandir}/man1/Hyprland.1*
%{_mandir}/man1/hyprctl.1*
# Shell completions
%{_datadir}/bash-completion/completions/hyprctl
%{_datadir}/bash-completion/completions/hyprpm
%{_datadir}/fish/vendor_completions.d/hyprctl.fish
%{_datadir}/fish/vendor_completions.d/hyprpm.fish
%{_datadir}/zsh/site-functions/_hyprctl
%{_datadir}/zsh/site-functions/_hyprpm

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
* Sun May 10 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.55.0-1
- Update to Hyprland 0.55.0
- Bump hyprutils 0.11.0 -> 0.13.1, hyprgraphics 0.5.0 -> 0.5.1
- Bump hyprwire 0.3.0 -> 0.3.1, hyprwayland-scanner 0.4.5 -> 0.4.6, hyprlock 0.9.3 -> 0.9.5

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
