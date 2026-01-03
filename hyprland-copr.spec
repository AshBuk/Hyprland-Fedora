# Copyright (c) 2025 Asher Buk
# SPDX-License-Identifier: MIT
# https://copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora/

# =============================================================================
# Version definitions (single source of truth)
# =============================================================================
%global hyprland_version        0.53.1
%global hyprland_protocols_ver  0.7.0
%global hyprwayland_scanner_ver 0.4.5
%global hyprutils_ver           0.11.0
%global hyprlang_ver            0.6.7
%global hyprcursor_ver          0.1.13
%global hyprgraphics_ver        0.5.0
%global aquamarine_ver          0.10.0
%global hyprwire_ver            0.2.1
%global glaze_ver               6.4.1

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
Source0:        https://github.com/hyprwm/Hyprland/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Git submodules (not included in GitHub tarball)
Source10:       https://github.com/hyprwm/hyprland-protocols/archive/refs/tags/v%{hyprland_protocols_ver}.tar.gz#/hyprland-protocols-%{hyprland_protocols_ver}.tar.gz
# udis86 from Hyprland subprojects (patched for Python 3.x, with CMakeLists.txt)
Source11:       https://github.com/AshBuk/Hyprland-Fedora/releases/download/v%{version}-fedora/udis86-hyprland.tar.gz

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
Source30:       https://github.com/AshBuk/Hyprland-Fedora/releases/download/v%{version}-fedora/glaze-%{glaze_ver}.tar.gz

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
BuildRequires:  wayland-protocols-devel
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

%description
Hyprland is a dynamic tiling Wayland compositor with modern Wayland features,
high customizability, IPC, plugins, and visual effects.

This is a single-package COPR build for Fedora 43.
Pinned Hyprland dependencies are built from fixed-version sources and installed
into a private vendor prefix to avoid polluting system /usr/lib64.

Note: Version 0.53.0 includes breaking changes in window rules syntax.
Please review https://hypr.land/news/update53/ before upgrading.

%prep
%autosetup -n Hyprland-%{version}

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

# 9) Hyprland (needs -fpermissive for generated protocol code with zero-size arrays)
# Use local glaze source (mock chroot has no network for FetchContent)
# Disable BUILD_TESTING to skip hyprtester (its plugin Makefile doesn't support vendored deps)
# Set RPATH at build time to avoid patchelf corruption issues
VENDOR_RPATH='$ORIGIN/../libexec/hyprland/vendor/lib64:$ORIGIN/../libexec/hyprland/vendor/lib'
cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" \
  -Dhyprwayland-scanner_DIR="$VENDOR_PREFIX/lib64/cmake/hyprwayland-scanner" \
  -DCMAKE_CXX_FLAGS="$GCC15_CXXFLAGS" \
  -DFETCHCONTENT_SOURCE_DIR_GLAZE="$(pwd)/glaze-%{glaze_ver}" \
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

# 10) start-hyprland (NEW: watchdog/crash recovery binary)
pushd start
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" \
  -DCMAKE_INSTALL_RPATH="$VENDOR_RPATH" \
  -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
cmake --build build --parallel %{_smp_build_ncpus}
popd

%check
# Tests disabled: hyprtester doesn't support vendored deps

%install
VENDOR_PREFIX="$(pwd)/vendor"

# Install Hyprland binaries/data
DESTDIR=%{buildroot} cmake --install build

# Install start-hyprland
DESTDIR=%{buildroot} cmake --install start/build

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

# Verify RPATH is set correctly (was set at build time via CMAKE_INSTALL_RPATH)
# Using patchelf post-install can corrupt ELF program headers, so we set RPATH at build time
echo "Verifying RPATH on installed binaries:"
for bin in %{buildroot}%{_bindir}/Hyprland %{buildroot}%{_bindir}/hyprctl %{buildroot}%{_bindir}/hyprpm %{buildroot}%{_bindir}/start-hyprland; do
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
# Data files
%{_datadir}/hypr/
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

%changelog
* Sat Jan 03 2026 Asher Buk <AshBuk@users.noreply.github.com> - 0.53.0-4
- Update to Hyprland 0.53.1 (patch release with bugfixes)
- Refactor: use %%global macros for all dependency versions
- Refactor: create-srpm.sh now parses versions from spec file

* Wed Dec 31 2025 Asher Buk <AshBuk@users.noreply.github.com> - 0.53.0-3
- Update to Hyprland 0.53.0
- BREAKING: Window rules syntax completely reworked (see https://hypr.land/news/update53/)
- NEW: start-hyprland watchdog binary for crash recovery and safe mode
- NEW: hyprwire IPC library (v0.2.1) for improved hyprctl communication
- Update hyprland-protocols 0.6.4 -> 0.7.0
- Update hyprgraphics 0.4.0 -> 0.5.0
- Update glaze 5.1.1 -> 6.4.1
- Add libffi dependency for hyprwire
- Add muParser dependency for math expressions in config
- Exclude auto-requires for vendored Hyprland libraries

* Thu Dec 18 2025 Asher Buk <AshBuk@users.noreply.github.com> - 0.52.2-2
- Fix ELF corruption: set RPATH at build time via CMAKE_INSTALL_RPATH
- Remove patchelf post-install which was corrupting ELF program headers
- Binaries are now properly dynamically linked

* Mon Dec 15 2025 Asher Buk <AshBuk@users.noreply.github.com> - 0.52.2-1
- Single-package COPR build for Fedora 43
- Pinned Hyprland deps built from fixed-version sources
- Vendored runtime libs in /usr/libexec to avoid system library conflicts
