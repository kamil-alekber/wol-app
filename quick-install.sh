#!/bin/bash

# Quick installer for Wake-on-LAN Web Application
# Usage: curl -sSL https://raw.githubusercontent.com/yourusername/wol-app/main/quick-install.sh | bash

set -e

REPO_URL="https://raw.githubusercontent.com/yourusername/wol-app/main/install.sh"
TEMP_DIR=$(mktemp -d)

echo "🚀 Downloading Wake-on-LAN Web Application installer..."

# Download the full installer
if command -v curl >/dev/null 2>&1; then
    curl -sSL "$REPO_URL" -o "$TEMP_DIR/install.sh"
elif command -v wget >/dev/null 2>&1; then
    wget -q "$REPO_URL" -O "$TEMP_DIR/install.sh"
else
    echo "❌ Error: Neither curl nor wget found. Please install one of them."
    exit 1
fi

chmod +x "$TEMP_DIR/install.sh"

echo "✅ Running installer..."
bash "$TEMP_DIR/install.sh"

# Cleanup
rm -rf "$TEMP_DIR"
