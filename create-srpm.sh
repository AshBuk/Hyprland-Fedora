#!/bin/bash
# Create SRPM for COPR submission
set -e

VERSION="0.52.2"
RELEASE="1"

echo "=== Creating SRPM for Hyprland ${VERSION} ==="

# Download source
if [ ! -f "hyprland-${VERSION}.tar.gz" ]; then
    echo "Downloading source..."
    wget -O "hyprland-${VERSION}.tar.gz" \
         "https://github.com/hyprwm/Hyprland/archive/refs/tags/v${VERSION}.tar.gz"
fi

# Create SRPM
echo "Creating SRPM..."
rpmbuild -bs hyprland-copr.spec \
         --define "_sourcedir $(pwd)" \
         --define "_srcrpmdir $(pwd)/srpm" \
         --define "dist .fc43"

mkdir -p srpm
mv *.src.rpm srpm/ 2>/dev/null || true

echo ""
echo "=== SRPM created successfully! ==="
echo "Location: $(pwd)/srpm/"
ls -la srpm/*.src.rpm
echo ""
echo "To submit to COPR:"
echo "  copr-cli build <your-copr-repo> srpm/hyprland-${VERSION}-${RELEASE}.fc43.src.rpm"