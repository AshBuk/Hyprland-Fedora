#!/bin/bash
# Copyright (c) 2025 Asher Buk
# SPDX-License-Identifier: MIT
# https://copr.fedorainfracloud.org/coprs/ashbuk/Hyprland-Fedora/
#
# Run rpmlint on spec files using Fedora container
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Running rpmlint on hyprland-copr.spec ==="
docker run --rm -e LANG=C.UTF-8 -v "${SCRIPT_DIR}:/work:ro" fedora:43 \
  sh -c "dnf install -y -q rpmlint 2>/dev/null && rpmlint /work/hyprland-copr.spec"
