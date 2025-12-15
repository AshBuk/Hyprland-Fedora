#!/bin/bash
# Build Hyprland RPM for Fedora 43 (includes xdg-desktop-portal-hyprland)
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION="0.52.2"
RELEASE="1"
RPM_NAME="hyprland-${VERSION}-${RELEASE}.fc43.x86_64.rpm"

echo "=== Building Hyprland ${VERSION} RPM for Fedora 43 (with portal) ==="

# First build binaries if not already done
if [ ! -f "${SCRIPT_DIR}/output/Hyprland" ]; then
    echo "Building Hyprland binaries first..."
    "${SCRIPT_DIR}/build-fedora43.sh"
fi

# Extract libraries from container
echo ""
echo "=== Extracting libraries from container... ==="
mkdir -p "${SCRIPT_DIR}/output/libs"
docker run --rm -v "${SCRIPT_DIR}/output/libs:/libs" hyprland-fedora43 \
    sh -c "cp /usr/lib64/libhypr* /usr/lib64/libaquamarine* /libs/ 2>/dev/null || true"

# Create RPM build structure
echo ""
echo "=== Creating RPM structure... ==="
RPM_BUILD_DIR="${SCRIPT_DIR}/rpmbuild"
rm -rf "${RPM_BUILD_DIR}"
mkdir -p "${RPM_BUILD_DIR}"/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Create spec file for binary RPM
cat > "${RPM_BUILD_DIR}/SPECS/hyprland.spec" << EOF
Name:           hyprland
Version:        ${VERSION}
Release:        ${RELEASE}%{?dist}
Summary:        Dynamic tiling Wayland compositor with xdg-desktop-portal
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/Hyprland
AutoReqProv:    no

# Bundled libraries - we provide and replace system packages
Provides:       hyprlang = 0.6.7
Provides:       hyprutils = 0.11.0
Provides:       hyprcursor = 0.1.13
Provides:       hyprgraphics = 0.4.0
Provides:       aquamarine = 0.10.0
Provides:       xdg-desktop-portal-hyprland = ${VERSION}
Obsoletes:      hyprlang < 999
Obsoletes:      hyprutils < 999
Obsoletes:      hyprcursor < 999
Obsoletes:      hyprgraphics < 999
Obsoletes:      aquamarine < 999
Obsoletes:      xdg-desktop-portal-hyprland < 999
Conflicts:      hyprlang
Conflicts:      hyprutils
Conflicts:      hyprcursor
Conflicts:      hyprgraphics
Conflicts:      aquamarine
Conflicts:      xdg-desktop-portal-hyprland

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
Requires:       tomlplusplus
Requires:       xdg-desktop-portal
Requires:       pipewire
Requires:       sdbus-cpp
Requires:       qt6-qtbase
Requires:       qt6-qtwayland

%description
Hyprland is a dynamic tiling Wayland compositor that doesn't sacrifice
on its looks. Custom build with noscreenshare layerrule support.
Includes bundled xdg-desktop-portal-hyprland for screen sharing.

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_datadir}/wayland-sessions
mkdir -p %{buildroot}%{_datadir}/hyprland
mkdir -p %{buildroot}%{_datadir}/licenses/hyprland
mkdir -p %{buildroot}%{_datadir}/xdg-desktop-portal
mkdir -p %{buildroot}%{_datadir}/xdg-desktop-portal/portals
mkdir -p %{buildroot}%{_datadir}/dbus-1/services
mkdir -p %{buildroot}%{_userunitdir}

# Copy binaries
install -m 755 ${SCRIPT_DIR}/output/Hyprland %{buildroot}%{_bindir}/
install -m 755 ${SCRIPT_DIR}/output/hyprctl %{buildroot}%{_bindir}/
install -m 755 ${SCRIPT_DIR}/output/hyprpm %{buildroot}%{_bindir}/

# Copy portal binaries
install -m 755 ${SCRIPT_DIR}/output/xdg-desktop-portal-hyprland %{buildroot}%{_libexecdir}/
install -m 755 ${SCRIPT_DIR}/output/hyprland-share-picker %{buildroot}%{_bindir}/ 2>/dev/null || true

# Copy portal data files
install -m 644 ${SCRIPT_DIR}/output/portal-data/hyprland.portal %{buildroot}%{_datadir}/xdg-desktop-portal/portals/
install -m 644 ${SCRIPT_DIR}/output/portal-data/org.freedesktop.impl.portal.desktop.hyprland.service %{buildroot}%{_datadir}/dbus-1/services/
install -m 644 ${SCRIPT_DIR}/output/portal-data/xdg-desktop-portal-hyprland.service %{buildroot}%{_userunitdir}/

# Copy libraries if available
cp -a ${SCRIPT_DIR}/output/libs/*.so* %{buildroot}%{_libdir}/ 2>/dev/null || true

# Copy assets
cp -r ${SCRIPT_DIR}/output/assets/* %{buildroot}%{_datadir}/hyprland/ 2>/dev/null || true
cp -r ${SCRIPT_DIR}/output/example/* %{buildroot}%{_datadir}/hyprland/ 2>/dev/null || true

# Copy license
install -m 644 ${SCRIPT_DIR}/output/LICENSE %{buildroot}%{_datadir}/licenses/hyprland/

# Copy portal config
install -m 644 ${SCRIPT_DIR}/assets/hyprland-portals.conf %{buildroot}%{_datadir}/xdg-desktop-portal/ 2>/dev/null || true

# Create desktop entry
cat > %{buildroot}%{_datadir}/wayland-sessions/hyprland.desktop << 'DESKTOP'
[Desktop Entry]
Name=Hyprland
Comment=Dynamic tiling Wayland compositor
Exec=Hyprland
Type=Application
DesktopNames=Hyprland
DESKTOP

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%license %{_datadir}/licenses/hyprland/LICENSE
%{_bindir}/Hyprland
%{_bindir}/hyprctl
%{_bindir}/hyprpm
%{_bindir}/hyprland-share-picker
%{_libexecdir}/xdg-desktop-portal-hyprland
%{_libdir}/libaquamarine.so*
%{_libdir}/libhyprcursor.so*
%{_libdir}/libhyprgraphics.so*
%{_libdir}/libhyprlang.so*
%{_libdir}/libhyprutils.so*
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/hyprland/
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
%{_datadir}/xdg-desktop-portal/portals/hyprland.portal
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.hyprland.service
%{_userunitdir}/xdg-desktop-portal-hyprland.service

%changelog
* $(date "+%a %b %d %Y") Local Build <local@localhost> - ${VERSION}-${RELEASE}
- Custom build for Fedora 43 with noscreenshare support
- Includes bundled xdg-desktop-portal-hyprland
EOF

# Build RPM
echo ""
echo "=== Building RPM... ==="
rpmbuild --define "_topdir ${RPM_BUILD_DIR}" \
         --define "dist .fc43" \
         -bb "${RPM_BUILD_DIR}/SPECS/hyprland.spec"

# Copy result
cp "${RPM_BUILD_DIR}/RPMS/x86_64/${RPM_NAME}" "${SCRIPT_DIR}/output/"

echo ""
echo "=== RPM Build complete! ==="
echo "RPM location: ${SCRIPT_DIR}/output/${RPM_NAME}"
echo ""
echo "To install:"
echo "  sudo dnf install ${SCRIPT_DIR}/output/${RPM_NAME}"
echo ""
echo "To update (after rebuilding):"
echo "  sudo dnf upgrade ${SCRIPT_DIR}/output/${RPM_NAME}"
echo ""
echo "To remove:"
echo "  sudo dnf remove hyprland"
