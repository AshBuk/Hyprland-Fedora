Name:           hyprland
Version:        0.52.2
Release:        1%{?dist}
Summary:        Dynamic tiling Wayland compositor
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/Hyprland

# Main source
Source0:        https://github.com/hyprwm/Hyprland/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Git submodules (not included in GitHub tarball)
Source10:       https://github.com/hyprwm/hyprland-protocols/archive/refs/tags/v0.6.4.tar.gz#/hyprland-protocols-0.6.4.tar.gz
Source11:       https://github.com/canihavesomecoffee/udis86/archive/refs/tags/v1.7.2.tar.gz#/udis86-1.7.2.tar.gz

# Hyprland pinned deps (vendored, fixed versions)
Source20:       https://github.com/hyprwm/hyprwayland-scanner/archive/refs/tags/v0.4.4.tar.gz#/hyprwayland-scanner-0.4.4.tar.gz
Source21:       https://github.com/hyprwm/hyprutils/archive/refs/tags/v0.11.0.tar.gz#/hyprutils-0.11.0.tar.gz
Source22:       https://github.com/hyprwm/hyprlang/archive/refs/tags/v0.6.7.tar.gz#/hyprlang-0.6.7.tar.gz
Source23:       https://github.com/hyprwm/hyprcursor/archive/refs/tags/v0.1.13.tar.gz#/hyprcursor-0.1.13.tar.gz
Source24:       https://github.com/hyprwm/hyprgraphics/archive/refs/tags/v0.4.0.tar.gz#/hyprgraphics-0.4.0.tar.gz
Source25:       https://github.com/hyprwm/aquamarine/archive/refs/tags/v0.10.0.tar.gz#/aquamarine-0.10.0.tar.gz

# Build dependencies
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  patchelf

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

%description
Hyprland is a dynamic tiling Wayland compositor with modern Wayland features,
high customizability, IPC, plugins, and visual effects.

This is a single-package COPR build for Fedora 43.
Pinned Hyprland dependencies are built from fixed-version sources and installed
into a private vendor prefix to avoid polluting system /usr/lib64.

%prep
%autosetup -n Hyprland-%{version}

# Unpack submodules into correct locations
rm -rf subprojects/hyprland-protocols subprojects/udis86
tar -xzf %{SOURCE10} -C subprojects
mv subprojects/hyprland-protocols-0.6.4 subprojects/hyprland-protocols
tar -xzf %{SOURCE11} -C subprojects
mv subprojects/udis86-1.7.2 subprojects/udis86

# Unpack vendored deps in top build dir
tar -xzf %{SOURCE20}
tar -xzf %{SOURCE21}
tar -xzf %{SOURCE22}
tar -xzf %{SOURCE23}
tar -xzf %{SOURCE24}
tar -xzf %{SOURCE25}

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
# Use %{optflags} (RPM standard flags) + -fpermissive for protocol code
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
pushd hyprwayland-scanner-0.4.4
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
  -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# Verify hyprwayland-scanner cmake config is installed
ls -la "$VENDOR_PREFIX/lib64/cmake/hyprwayland-scanner/" || ls -la "$VENDOR_PREFIX/lib/cmake/hyprwayland-scanner/" || true

# 2) hyprutils
pushd hyprutils-0.11.0
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# 3) hyprlang
pushd hyprlang-0.6.7
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# 4) hyprcursor
pushd hyprcursor-0.1.13
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# 5) hyprgraphics
pushd hyprgraphics-0.4.0
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$VENDOR_PREFIX" \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" -DCMAKE_INSTALL_LIBDIR=lib64
cmake --build build --parallel %{_smp_build_ncpus}
cmake --install build
popd

# 6) aquamarine (needs -fpermissive for generated protocol code with zero-size arrays)
# Explicitly set hyprwayland-scanner_DIR since CMAKE_PREFIX_PATH may not work in mock chroot
# Also need explicit OpenGL/EGL paths for libglvnd on Fedora
pushd aquamarine-0.10.0
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

# 7) hyprland-protocols
pushd subprojects/hyprland-protocols
meson setup build --prefix="$VENDOR_PREFIX"
ninja -C build
ninja -C build install
popd

# 8) Hyprland (needs -fpermissive for generated protocol code with zero-size arrays)
cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_PREFIX_PATH="$VENDOR_PREFIX" \
  -Dhyprwayland-scanner_DIR="$VENDOR_PREFIX/lib64/cmake/hyprwayland-scanner" \
  -DCMAKE_CXX_FLAGS="$GCC15_CXXFLAGS" \
  -DOPENGL_opengl_LIBRARY=%{_libdir}/libOpenGL.so \
  -DOPENGL_gles3_LIBRARY=%{_libdir}/libGLESv2.so \
  -DOPENGL_GLES3_INCLUDE_DIR=/usr/include \
  -DOPENGL_egl_LIBRARY=%{_libdir}/libEGL.so \
  -DOPENGL_EGL_INCLUDE_DIR=/usr/include \
  -DOPENGL_INCLUDE_DIR=/usr/include
cmake --build build --parallel %{_smp_build_ncpus}

%install
VENDOR_PREFIX="$(pwd)/vendor"

# Install Hyprland binaries/data
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

# Set RPATH on binaries to use vendored libs
RPATH='$ORIGIN/../libexec/hyprland/vendor/lib64:$ORIGIN/../libexec/hyprland/vendor/lib'
for bin in %{buildroot}%{_bindir}/Hyprland %{buildroot}%{_bindir}/hyprctl %{buildroot}%{_bindir}/hyprpm; do
  [ -x "$bin" ] || continue
  patchelf --set-rpath "$RPATH" "$bin"
done

%files
%license LICENSE
%doc README.md
%{_bindir}/Hyprland
%{_bindir}/hyprland
%{_bindir}/hyprctl
%{_bindir}/hyprpm
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/vendor/
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/hypr/
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
%{_includedir}/hyprland/

%changelog
* Mon Dec 15 2025 Asher Buk <asherbuk@example.com> - 0.52.2-1
- Single-package COPR build for Fedora 43
- Pinned Hyprland deps built from fixed-version sources
- Vendored runtime libs in /usr/libexec to avoid system library conflicts
