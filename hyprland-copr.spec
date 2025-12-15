Name:           hyprland
Version:        0.52.2
Release:        1%{?dist}
Summary:        Dynamic tiling Wayland compositor
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/Hyprland
Source0:        https://github.com/hyprwm/Hyprland/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

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
BuildRequires:  git

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
Hyprland is a dynamic tiling Wayland compositor that doesn't sacrifice
on its looks. It provides the latest Wayland features, is highly
customizable, has all the eyecandy, the most powerful plugins, easy IPC,
and much more.

This build includes the noscreenshare layerrule feature for excluding
layers from screenshare applications.

%prep
%autosetup -n %{name}-%{version}

# Build hyprwayland-scanner
pushd .
mkdir hyprwayland-scanner-build
cd hyprwayland-scanner-build
git clone --depth=1 https://github.com/hyprwm/hyprwayland-scanner .
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_prefix} -B build
cmake --build build -j%(nproc)
cmake --install build --prefix %{_builddir}/hyprwayland-scanner-install
popd

# Build hyprutils
pushd .
mkdir hyprutils-build
cd hyprutils-build
git clone --depth=1 https://github.com/hyprwm/hyprutils .
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_prefix} -B build
cmake --build build -j%(nproc)
cmake --install build --prefix %{_builddir}/hyprutils-install
popd

# Build hyprlang
pushd .
mkdir hyprlang-build
cd hyprlang-build
git clone --depth=1 https://github.com/hyprwm/hyprlang .
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_prefix} -B build
cmake --build build -j%(nproc)
cmake --install build --prefix %{_builddir}/hyprlang-install
popd

# Build hyprcursor
pushd .
mkdir hyprcursor-build
cd hyprcursor-build
git clone --depth=1 https://github.com/hyprwm/hyprcursor .
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_prefix} -B build
cmake --build build -j%(nproc)
cmake --install build --prefix %{_builddir}/hyprcursor-install
popd

# Build hyprgraphics
pushd .
mkdir hyprgraphics-build
cd hyprgraphics-build
git clone --depth=1 https://github.com/hyprwm/hyprgraphics .
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_prefix} -B build
cmake --build build -j%(nproc)
cmake --install build --prefix %{_builddir}/hyprgraphics-install
popd

# Build aquamarine
pushd .
mkdir aquamarine-build
cd aquamarine-build
git clone --depth=1 https://github.com/hyprwm/aquamarine .
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_prefix} -B build
cmake --build build -j%(nproc)
cmake --install build --prefix %{_builddir}/aquamarine-install
popd

%build
# Create hwdata.pc if missing
mkdir -p %{_builddir}/pkgconfig
cat > %{_builddir}/pkgconfig/hwdata.pc << 'EOF'
prefix=%{_prefix}
datarootdir=${prefix}/share
pkgdatadir=${datarootdir}/hwdata

Name: hwdata
Description: Hardware identification databases
Version: 0.385
EOF
export PKG_CONFIG_PATH="%{_builddir}/pkgconfig:$PKG_CONFIG_PATH"
export CMAKE_PREFIX_PATH="%{_builddir}/hyprwayland-scanner-install:%{_builddir}/hyprutils-install:%{_builddir}/hyprlang-install:%{_builddir}/hyprcursor-install:%{_builddir}/hyprgraphics-install:%{_builddir}/aquamarine-install:$CMAKE_PREFIX_PATH"

%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

# Install desktop entry
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
* Thu Dec 11 2025 Local Build <local@localhost> - 0.52.2-1
- Custom build for Fedora 43 with noscreenshare support