#!/bin/bash

# Wake-on-LAN Web Application Installation Script
# This script downloads and sets up the WOL app for easy use

set -e

echo "🚀 Wake-on-LAN Web Application Installer"
echo "========================================"

# Configuration
REPO_URL="https://github.com/yourusername/wol-app"  # Update this with your actual repo URL
APP_DIR="$HOME/wol-app"
PYTHON_MIN_VERSION="3.7"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python version
check_python_version() {
    if command_exists python3; then
        local python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        local required_version=$PYTHON_MIN_VERSION
        
        if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
            log_success "Python $python_version found (>= $PYTHON_MIN_VERSION required)"
            return 0
        else
            log_error "Python $python_version found, but Python $PYTHON_MIN_VERSION or higher is required"
            return 1
        fi
    else
        log_error "Python 3 is not installed"
        return 1
    fi
}

# Install wakeonlan tool
install_wakeonlan() {
    log_info "Checking for wakeonlan tool..."
    
    if command_exists wakeonlan; then
        log_success "wakeonlan is already installed"
        return 0
    fi
    
    log_warning "wakeonlan not found. Installing..."
    
    # Detect OS and install wakeonlan
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command_exists brew; then
            brew install wakeonlan
            log_success "wakeonlan installed via Homebrew"
        else
            log_error "Homebrew not found. Please install Homebrew first or install wakeonlan manually"
            return 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command_exists apt-get; then
            sudo apt-get update && sudo apt-get install -y wakeonlan
            log_success "wakeonlan installed via apt"
        elif command_exists yum; then
            sudo yum install -y wakeonlan
            log_success "wakeonlan installed via yum"
        elif command_exists dnf; then
            sudo dnf install -y wakeonlan
            log_success "wakeonlan installed via dnf"
        elif command_exists pacman; then
            sudo pacman -S --noconfirm wakeonlan
            log_success "wakeonlan installed via pacman"
        else
            log_error "Unable to detect package manager. Please install wakeonlan manually"
            return 1
        fi
    else
        log_error "Unsupported operating system. Please install wakeonlan manually"
        return 1
    fi
}

# Download and extract application
download_app() {
    log_info "Downloading Wake-on-LAN Web Application..."
    
    # Remove existing directory if it exists
    if [ -d "$APP_DIR" ]; then
        log_warning "Existing installation found at $APP_DIR. Removing..."
        rm -rf "$APP_DIR"
    fi
    
    # Create application directory
    mkdir -p "$APP_DIR"
    cd "$APP_DIR"
    
    # Download latest release
    if command_exists curl; then
        curl -L "$REPO_URL/archive/refs/tags/v1.0.0.tar.gz" | tar -xz --strip-components=1
    elif command_exists wget; then
        wget -O - "$REPO_URL/archive/refs/tags/v1.0.0.tar.gz" | tar -xz --strip-components=1
    else
        log_error "Neither curl nor wget found. Please install one of them"
        return 1
    fi
    
    log_success "Application downloaded to $APP_DIR"
}

# Install Python dependencies
install_dependencies() {
    log_info "Installing Python dependencies..."
    
    cd "$APP_DIR"
    
    # Create virtual environment if possible
    if command_exists python3 && python3 -m venv --help >/dev/null 2>&1; then
        log_info "Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        log_success "Virtual environment created and activated"
    fi
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt
        log_success "Python dependencies installed"
    else
        log_error "requirements.txt not found"
        return 1
    fi
}

# Setup configuration
setup_config() {
    log_info "Setting up configuration..."
    
    cd "$APP_DIR"
    
    if [ -f "config.example.json" ]; then
        cp config.example.json config.json
        log_success "Configuration file created from example"
        log_info "You can edit config.json to customize settings"
    else
        log_warning "config.example.json not found. You may need to create config.json manually"
    fi
}

# Create startup script
create_startup_script() {
    log_info "Creating startup script..."
    
    cat > "$APP_DIR/start.sh" << 'EOF'
#!/bin/bash

# Navigate to application directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Start the application
echo "🚀 Starting Wake-on-LAN Web Application..."
echo "📱 Access the web interface at: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the application"
echo ""

python3 app.py
EOF

    chmod +x "$APP_DIR/start.sh"
    log_success "Startup script created at $APP_DIR/start.sh"
}

# Main installation process
main() {
    echo ""
    log_info "Starting installation process..."
    echo ""
    
    # Check prerequisites
    log_info "Checking prerequisites..."
    if ! check_python_version; then
        log_error "Python version check failed. Please install Python $PYTHON_MIN_VERSION or higher"
        exit 1
    fi
    
    # Install wakeonlan
    if ! install_wakeonlan; then
        log_error "Failed to install wakeonlan. Please install it manually and try again"
        exit 1
    fi
    
    # Download application
    if ! download_app; then
        log_error "Failed to download application"
        exit 1
    fi
    
    # Install dependencies
    if ! install_dependencies; then
        log_error "Failed to install Python dependencies"
        exit 1
    fi
    
    # Setup configuration
    setup_config
    
    # Create startup script
    create_startup_script
    
    echo ""
    log_success "🎉 Installation completed successfully!"
    echo ""
    echo "📁 Application installed at: $APP_DIR"
    echo "🚀 To start the application, run:"
    echo "   cd $APP_DIR && ./start.sh"
    echo ""
    echo "📱 Once started, access the web interface at: http://localhost:5000"
    echo ""
    echo "📖 For more information, see the README.md file in the application directory"
    echo ""
}

# Run main function
main "$@"
