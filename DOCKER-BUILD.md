# Docker Build

## Build Image

```bash
docker build -f Dockerfile.fedora43 -t hyprland-fedora43 .
```

## Extract Binaries

```bash
mkdir -p output
docker run --rm -v $(pwd)/output:/output hyprland-fedora43
```

## Extract Libraries

```bash
mkdir -p output/libs
docker run --rm -v $(pwd)/output/libs:/libs hyprland-fedora43 \
    sh -c "cp /usr/lib64/libhypr* /usr/lib64/libaquamarine* /libs/"
```

## Manual Install (without RPM)

```bash
# Libraries
sudo cp output/libs/*.so* /usr/lib64/
sudo ldconfig

# Binaries
sudo cp output/Hyprland output/hyprctl output/hyprpm /usr/bin/

# Desktop entry
sudo tee /usr/share/wayland-sessions/hyprland.desktop << 'EOF'
[Desktop Entry]
Name=Hyprland
Comment=Dynamic tiling Wayland compositor
Exec=Hyprland
Type=Application
DesktopNames=Hyprland
EOF
```

## Output Structure

```
output/
├── Hyprland          # main compositor
├── hyprctl           # control utility
├── hyprpm            # plugin manager
├── LICENSE
├── assets/           # icons, wallpapers
├── example/          # config examples
└── libs/             # shared libraries (after extraction)
    ├── libaquamarine.so*
    ├── libhyprcursor.so*
    ├── libhyprgraphics.so*
    ├── libhyprlang.so*
    └── libhyprutils.so*
```
