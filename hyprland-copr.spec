Name:           hyprland
Version:        0.52.2
Release:        1%{?dist}
Summary:        Dynamic tiling Wayland compositor
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/Hyprland

Source0:  https://github.com/hyprwm/Hyprland/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:  https://github.com/hyprwm/hyprwayland-scanner/archive/refs/tags/v0.4.4.tar.gz
Source2:  https://github.com/hyprwm/hyprutils/archive/refs/tags/v0.11.0.tar.gz
Source3:  https://github.com/hyprwm/hyprlang/archive/refs/tags/v0.6.7.tar.gz
Source4:  https://github.com/hyprwm/hyprcursor/archive/refs/tags/v0.1.13.tar.gz
Source5:  https://github.com/hyprwm/hyprgraphics/archive/refs/tags/v0.4.0.tar.gz
Source6:  https://github.com/hyprwm/aquamarine/archive/refs/tags/v0.10.0.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  cairo-devel
BuildRequires:  glm-devel
BuildRequires:  glslang-devel
BuildRequires:  hwdata
BuildRequires:  libdisplay-info-devel
BuildRequires:  libdrm-devel
BuildRequires:  libepoxy-devel
BuildRequires:  mesa-libgbm-devel
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

Requires: cairo
Requires: hwdata
Requires: libdisplay-info
Requires: libdrm
Requires: libepoxy
Requires: mesa-libgbm
Requires: libinput
Requires: libjxl
Requires: libliftoff
Requires: libspng
Requires: libwebp
Requires: libxcb
Requires: libXcursor
Requires: libxcvt
Requires: libxkbcommon
Requires: pango
Requires: pixman
Requires: pugixml
Requires: re2
Requires: libseat
Requires: libwayland-client
Requires: libwayland-server
Requires: libzip
Requires: librsvg2
Requires: xcb-util
Requires: xcb-util-errors
Requires: xcb-util-image
Requires: xcb-util-renderutil
Requires: xcb-util-wm
Requires: xorg-x11-server-Xwayland

%description
Hyprland is a dynamic tiling Wayland compositor with modern features,
high customizability, IPC, plugins, and visual effects.

This build pins internal Hyprland dependencies to fixed upstream versions
for reproducible Fedora 43 builds.

%prep
%autosetup -n Hyprland-%{version} -a1 -a2 -a3 -a4 -a5 -a6

%build
export CMAKE_PREFIX_PATH=%{_builddir}/hyprwayland-scanner-0.4.4:%{_builddir}/hyprutils-0.11.0:%{_builddir}/hyprlang-0.6.7:%{_builddir}/hyprcursor-0.1.13:%{_builddir}/hyprgraphics-0.4.0:%{_builddir}/aquamarine-0.10.0

%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

mkdir -p %{buildroot}%{_datadir}/wayland-sessions
cat > %{buildroot}%{_datadir}/wayland-sessions/hyprland.desktop << 'EOF'
[Desktop Entry]
Name=Hyprland
Comment=Dynamic tiling Wayland compositor
Exec=Hyprland
Type=Application
DesktopNames=Hyprland
EOF

%files
%license LICENSE
%doc README.md
%{_bindir}/Hyprland
%{_bindir}/hyprctl
%{_bindir}/hyprpm
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/hyprland/
%{_datadir}/xdg-desktop-portal/

%changelog
* Mon Dec 15 2025 Asher Buk <asherbuk@example.com> - 0.52.2-1
- Update to Hyprland 0.52.2
- Fixed internal dependency versions for reproducible COPR builds
- Fedora 43 custom build
