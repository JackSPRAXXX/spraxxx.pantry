#!/bin/bash
#
# SPRAXXX Messiah Lock Installation Script
# Purpose: Deploy Museum Pipeline to system
# Doctrine: Museum is RO by default. Always.
#

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_PREFIX="${INSTALL_PREFIX:-/usr/local}"
MUSEUM_ROOT="${MUSEUM_ROOT:-/messiah}"

echo "========================================"
echo "SPRAXXX Messiah Lock Installation"
echo "========================================"
echo "Repo:         $REPO_DIR"
echo "Install to:   $INSTALL_PREFIX"
echo "Museum root:  $MUSEUM_ROOT"
echo "========================================"
echo

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "ERROR: This script must be run as root (sudo)"
   exit 1
fi

echo "[1/6] Creating Museum directory structure..."
mkdir -p "$MUSEUM_ROOT"/{museum,workshop/dropit/inbox,workshop/staging}
echo "  ✓ Created $MUSEUM_ROOT structure"

echo
echo "[2/6] Installing binaries..."
install -m 755 "$REPO_DIR/bin/dropit" "$INSTALL_PREFIX/bin/dropit"
install -m 755 "$REPO_DIR/bin/messiah-commit" "$INSTALL_PREFIX/bin/messiah-commit"
echo "  ✓ Installed dropit → $INSTALL_PREFIX/bin/dropit"
echo "  ✓ Installed messiah-commit → $INSTALL_PREFIX/bin/messiah-commit"

echo
echo "[3/6] Installing library modules..."
mkdir -p "$INSTALL_PREFIX/lib/spraxxx"
install -m 644 "$REPO_DIR/lib/messiah_lock.py" "$INSTALL_PREFIX/lib/spraxxx/messiah_lock.py"
echo "  ✓ Installed messiah_lock.py → $INSTALL_PREFIX/lib/spraxxx/"

echo
echo "[4/6] Updating Python path in binaries..."
sed -i "s|sys.path.insert.*|sys.path.insert(0, '$INSTALL_PREFIX/lib/spraxxx')|" "$INSTALL_PREFIX/bin/messiah-commit"
echo "  ✓ Updated Python path"

echo
echo "[5/6] Setting Museum to read-only..."
chmod -R 555 "$MUSEUM_ROOT/museum"
chmod -R 755 "$MUSEUM_ROOT/workshop"
echo "  ✓ Museum locked (RO)"
echo "  ✓ Workshop writable (RW)"

echo
echo "[6/6] Installing systemd service (optional)..."
if [ -d /etc/systemd/system ]; then
    # Update service file with actual museum path
    sed "s|Environment=MUSEUM_PATH=.*|Environment=MUSEUM_PATH=$MUSEUM_ROOT/museum|" \
        "$REPO_DIR/museum-lock.service" > /etc/systemd/system/museum-lock.service

    systemctl daemon-reload
    echo "  ✓ Service installed: /etc/systemd/system/museum-lock.service"
    echo
    echo "  To enable on boot:"
    echo "    systemctl enable museum-lock.service"
    echo "    systemctl start museum-lock.service"
else
    echo "  ⚠ systemd not found. Skipping service installation."
fi

echo
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo
echo "Commands available:"
echo "  dropit              - Capture content safely"
echo "  messiah-commit      - Stage and commit to Museum"
echo
echo "Directory structure:"
echo "  $MUSEUM_ROOT/museum/            (RO - immutable archive)"
echo "  $MUSEUM_ROOT/workshop/          (RW - staging area)"
echo "  $MUSEUM_ROOT/workshop/dropit/inbox/"
echo "  $MUSEUM_ROOT/workshop/staging/"
echo
echo "Quick start:"
echo "  1. echo 'test content' | dropit"
echo "  2. messiah-commit <drop_id>"
echo
echo "Doctrine: Truth leaves a trace."
echo "========================================"
