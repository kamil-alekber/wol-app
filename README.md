# Wake-On-LAN Web Application

A simple web application for managing Wake-On-LAN devices with a clean, modern interface.

## Features

- ✨ Add and manage WOL devices
- 🚀 Wake devices with a single click
- 💾 Persistent storage in JSON format
- 🎨 Modern, responsive web interface
- 📱 Mobile-friendly design
- 🔄 Real-time feedback and notifications

## Prerequisites

1. **Python 3.7+** installed on your system
2. **wakeonlan command-line tool** installed:

   **On macOS:**
   ```bash
   brew install wakeonlan
   ```

   **On Ubuntu/Debian:**
   ```bash
   sudo apt-get install wakeonlan
   ```

   **On CentOS/RHEL/Fedora:**
   ```bash
   sudo yum install wakeonlan
   # or
   sudo dnf install wakeonlan
   ```

## Installation

### Quick Installation (Recommended)

For a completely automated installation, run this one-liner:

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/wol-app/main/quick-install.sh | bash
```

Or with wget:
```bash
wget -qO- https://raw.githubusercontent.com/yourusername/wol-app/main/quick-install.sh | bash
```

This will:
- Download the latest release
- Install all dependencies
- Set up the configuration
- Create a startup script

### Manual Installation

1. **Download the latest release:**
   ```bash
   curl -L https://github.com/yourusername/wol-app/archive/refs/tags/v1.0.0.tar.gz | tar -xz
   cd wol-app-1.0.0
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application:**
   ```bash
   # Copy the example configuration file
   cp config.example.json config.json
   
   # Edit the configuration file to suit your needs
   nano config.json  # or use your preferred editor
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the web interface:**
   Open your browser and go to: `http://localhost:5000` (or the port you configured)

## Usage

### Adding Devices

1. Fill out the "Add New Device" form:
   - **Device Name** (required): A friendly name for your device
   - **MAC Address** (required): The device's MAC address (e.g., AA:BB:CC:DD:EE:FF)
   - **IP Address** (optional): The device's IP address
   - **Description** (optional): Additional notes about the device

2. Click "Add Device" to save

### Waking Devices

1. Find your device in the list
2. Click the "⚡ Wake Up" button
3. The application will send a Wake-On-LAN packet to the device

### Managing Devices

- **Delete**: Use the "🗑️ Delete" button to remove a device
- **View History**: See when each device was last awakened

## API Endpoints

The application also provides RESTful API endpoints:

- `GET /devices` - Retrieve all devices as JSON
- `POST /devices` - Add a new device (JSON or form data)
- `POST /wake/<device_id>` - Wake a specific device

## Configuration

The application uses a `config.json` file for all configuration settings. Create this file by copying the example:

```bash
cp config.example.json config.json
```

### Configuration Options

Edit `config.json` to customize the following settings:

#### App Settings (`app` section)
- **`secret_key`**: Flask secret key for session security (change for production!)
- **`debug`**: Enable debug mode (`true`/`false`)
- **`host`**: Host interface to bind to (default: `"0.0.0.0"`)
- **`port`**: Port to run the application on (default: `5000`)

#### Monitoring Settings (`monitoring` section)
- **`interval_seconds`**: How often to ping devices for status (default: `30`)
- **`ping_count`**: Number of ping packets to send per check (default: `4`)

#### Path Settings (`paths` section)
- **`devices_file`**: File to store device data (default: `"devices.json"`)
- **`ping_command`**: Path to ping command (default: `"/usr/bin/ping"`)
- **`wakeonlan_command`**: Path to wakeonlan command (default: `"/usr/bin/wakeonlan"`)

### Example Configuration

```json
{
  "app": {
    "secret_key": "your-random-secret-key-here",
    "debug": false,
    "host": "0.0.0.0",
    "port": 8080
  },
  "monitoring": {
    "interval_seconds": 60,
    "ping_count": 3
  },
  "paths": {
    "devices_file": "my_devices.json",
    "ping_command": "/bin/ping",
    "wakeonlan_command": "/usr/local/bin/wakeonlan"
  }
}
```

### Data Storage

Devices are stored in the file specified by `paths.devices_file` (default: `devices.json`). This file is created automatically when you add your first device.

## Troubleshooting

### "wakeonlan command not found"

Make sure the `wakeonlan` utility is installed on your system. See the Prerequisites section for installation instructions.

### Device not waking up

1. **Check MAC address**: Ensure the MAC address is correct
2. **Enable WOL**: Make sure Wake-On-LAN is enabled in the device's BIOS/UEFI settings
3. **Network settings**: Ensure the device's network adapter is configured to allow wake-on-LAN
4. **Power settings**: Check that the device is in a state that allows wake-up (sleep/hibernate, not fully powered off on some systems)

### Cannot access from other devices

If you want to access the web interface from other devices on your network:
1. Make sure the application is configured with `"host": "0.0.0.0"` in `config.json`
2. Check your firewall settings to allow connections on the configured port
3. Use your computer's IP address instead of `localhost`

## Security Considerations

- This application is intended for local network use
- **Important**: Change the `secret_key` in `config.json` for production use
- Consider adding authentication if deploying on a public network
- Keep the configuration file secure as it may contain sensitive settings

## License

This project is open source and available under the MIT License.
