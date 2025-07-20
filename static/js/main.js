// Global variables
let discoveryInterval = null;
let statusMonitoringInterval = null;

// Auto-format MAC address input
function setupMacAddressFormatting(inputId) {
  const input = document.getElementById(inputId);
  if (input) {
    input.addEventListener("input", function (e) {
      let value = e.target.value.replace(/[^a-fA-F0-9]/g, "");
      let formattedValue = value.match(/.{1,2}/g)?.join(":") || value;
      if (formattedValue !== e.target.value) {
        e.target.value = formattedValue.toUpperCase();
      }
    });
  }
}

// Add confirmation for wake actions
function setupWakeConfirmations() {
  document.querySelectorAll('form[action*="/wake/"]').forEach((form) => {
    form.addEventListener("submit", function (e) {
      const deviceName =
        this.closest(".device-card").querySelector(".device-name").textContent;
      if (!confirm(`Send wake signal to ${deviceName}?`)) {
        e.preventDefault();
      }
    });
  });
}

// Function to update device status
function updateDeviceStatus() {
  fetch("/status")
    .then((response) => response.json())
    .then((data) => {
      Object.keys(data).forEach((deviceId) => {
        const statusCircle = document.querySelector(
          `[data-device-id="${deviceId}"]`
        );
        if (statusCircle) {
          const status = data[deviceId];
          statusCircle.className = `status-circle status-${status}`;
          statusCircle.title = `Status: ${status}`;
        }
      });
    })
    .catch((error) => {
      console.error("Error fetching device status:", error);
    });
}

// Function to refresh the device list
function refreshDeviceList() {
  fetch("/devices")
    .then((response) => response.json())
    .then((devices) => {
      const devicesGrid = document.querySelector(".devices-grid");
      if (!devicesGrid) {
        // If no devices grid exists, create one
        const container = document.querySelector(".container");
        const newGrid = document.createElement("div");
        newGrid.className = "devices-grid";
        container.appendChild(newGrid);
      }

      const grid = document.querySelector(".devices-grid");
      if (devices.length === 0) {
        grid.innerHTML =
          '<p style="text-align: center; color: #666; font-style: italic; grid-column: 1 / -1;">No devices found. Add your first device above!</p>';
        return;
      }

      grid.innerHTML = devices
        .map(
          (device) => `
                <div class="device-card">
                    <div class="device-header">
                        <div class="device-name-container">
                            <div class="device-name">${device.name}</div>
                            <span class="status-circle status-unknown" data-device-id="${
                              device.id
                            }" title="Status: loading..."></span>
                        </div>
                    </div>
                    <div class="device-info">
                        <p><strong>MAC:</strong> ${device.mac}</p>
                        ${
                          device.ip
                            ? `<p><strong>IP:</strong> ${device.ip}</p>`
                            : ""
                        }
                        ${
                          device.description
                            ? `<p><strong>Description:</strong> ${device.description}</p>`
                            : ""
                        }
                        ${
                          device.last_wake
                            ? `<p class="last-wake">Last wake: ${device.last_wake
                                .substring(0, 19)
                                .replace("T", " ")}</p>`
                            : ""
                        }
                    </div>
                    <div class="device-actions">
                        <form method="post" action="/wake/${
                          device.id
                        }" style="display: inline-block;">
                            <button type="submit" class="btn btn-success">⚡ Wake</button>
                        </form>
                        <button type="button" class="btn btn-warning" onclick="openEditModal('${
                          device.id
                        }', '${device.name}', '${device.mac}', '${
            device.ip || ""
          }', '${device.description || ""}')">✏️ Edit</button>
                        <form method="post" action="/delete/${
                          device.id
                        }" style="display: inline-block;" 
                              onsubmit="return confirm('Delete device ${
                                device.name
                              }?')">
                            <button type="submit" class="btn btn-danger">🗑️ Delete</button>
                        </form>
                    </div>
                </div>
            `
        )
        .join("");

      // Re-attach event listeners to new forms
      setupWakeConfirmations();

      // Update device status for the new elements
      updateDeviceStatus();

      // Restart status monitoring for new devices
      startStatusMonitoring();
    })
    .catch((error) => {
      console.error("Error refreshing device list:", error);
    });
}

// Device Discovery Functions
function toggleDiscoverySection() {
  const discoverySection = document.getElementById("discoverySection");
  const locateBtn = document.getElementById("locateDevicesBtn");
  const isCurrentlyVisible = discoverySection.style.display === "block";

  if (isCurrentlyVisible) {
    // Hide the discovery section
    discoverySection.style.display = "none";
    if (locateBtn) {
      locateBtn.innerHTML = "Locate Devices";
    }
  } else {
    // Show the discovery section and check for previous results
    discoverySection.style.display = "block";
    if (locateBtn) {
      locateBtn.innerHTML = "Hide Discovery";
    }
    // Check if there are any previous discovery results
    fetch("/discover/status")
      .then((response) => response.json())
      .then((data) => {
        updateDiscoveryStatusModal(data);
      })
      .catch((error) => {
        console.error("Error checking discovery status:", error);
        // Show modal with no previous results
        updateDiscoveryStatusModal({ active: false, count: 0, devices: [] });
      });
  }
}

function showDiscoveryModal() {
  // First show the modal and check for previous results
  document.getElementById("discoverySection").style.display = "block";
  // Check if there are any previous discovery results
  fetch("/discover/status")
    .then((response) => response.json())
    .then((data) => {
      updateDiscoveryStatusModal(data);
    })
    .catch((error) => {
      console.error("Error checking discovery status:", error);
      // Show modal with no previous results
      updateDiscoveryStatusModal({ active: false, count: 0, devices: [] });
    });
}

function startDiscovery() {
  fetch("/discover/start", { method: "POST" })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
        return;
      }

      // Clear previous devices display when starting new search
      document.getElementById("discoveredDevices").innerHTML = "";

      // Start polling for discovery status
      discoveryInterval = setInterval(checkDiscoveryStatus, 2000);
    })
    .catch((error) => {
      console.error("Error starting discovery:", error);
      alert("Failed to start device discovery");
    });
}

function stopDiscovery() {
  fetch("/discover/stop", { method: "POST" })
    .then((response) => response.json())
    .then((data) => {
      clearInterval(discoveryInterval);

      // Get current discovery status to preserve found devices
      fetch("/discover/status")
        .then((response) => response.json())
        .then((currentData) => {
          // Update status but mark as inactive while keeping existing devices
          updateDiscoveryStatusModal({
            active: false,
            count: currentData.count || 0,
            devices: currentData.devices || [],
          });
        })
        .catch((error) => {
          console.error("Error getting current discovery status:", error);
          // Fallback: just update the UI to show as stopped
          updateDiscoveryStatusModal({ active: false, count: 0, devices: [] });
        });
    })
    .catch((error) => {
      console.error("Error stopping discovery:", error);
    });
}

function checkDiscoveryStatus() {
  fetch("/discover/status")
    .then((response) => response.json())
    .then((data) => {
      updateDiscoveryStatusModal(data);

      if (!data.active) {
        clearInterval(discoveryInterval);
      }
    })
    .catch((error) => {
      console.error("Error checking discovery status:", error);
    });
}

function updateDiscoveryStatusModal(data) {
  const statusDiv = document.getElementById("discoveryStatus");
  const devicesDiv = document.getElementById("discoveredDevices");

  if (data.active) {
    statusDiv.innerHTML = `
            <p>Scanning network... Found ${data.count} devices</p>
            <div style="margin: 10px 0;">
                <div style="background: #e0e0e0; border-radius: 10px; height: 8px; overflow: hidden;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 100%; width: 100%; animation: pulse-progress 1.5s ease-in-out infinite; border-radius: 10px;"></div>
                </div>
            </div>
            <div style="display: flex; gap: 10px; margin-top: 15px;">
                <button type="button" id="stopDiscoveryBtn" class="btn btn-danger" onclick="stopDiscovery()">Stop Discovery</button>
            </div>
        `;
  } else {
    const newDevicesCount = data.devices.filter(
      (device) => !device.already_imported
    ).length;

    // Check if we have any previous results
    const hasPreviousResults = data.devices && data.devices.length > 0;

    if (hasPreviousResults) {
      statusDiv.innerHTML = `
              <p>Discovery completed. Found ${data.count} devices</p>
              <div style="display: flex; gap: 10px; margin-top: 15px; flex-wrap: wrap;">
                  ${
                    newDevicesCount > 0
                      ? `<button type="button" onclick="importAllDevices()" class="btn btn-success">Import All New (${newDevicesCount})</button>`
                      : '<span style="color: #666; font-style: italic;">All devices already imported</span>'
                  }
                  <button type="button" onclick="startDiscovery()" class="btn btn-warning">Start New Search</button>
              </div>
          `;
    } else {
      // No previous results - show initial state
      statusDiv.innerHTML = `
              <p>Ready to search for devices on your network</p>
              <div style="display: flex; gap: 10px; margin-top: 15px;">
                  <button type="button" onclick="startDiscovery()" class="btn btn-success">Start Device Search</button>
              </div>
          `;
    }
  }

  // Display discovered devices
  if (data.devices && data.devices.length > 0) {
    devicesDiv.innerHTML = `
            <h3>Discovered Devices (${data.devices.length})</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; margin-top: 15px;">
                ${data.devices
                  .map(
                    (device, idx) => `
                    <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px; background: ${
                      device.already_imported ? "#f0f0f0" : "#f8f9fa"
                    }; opacity: ${device.already_imported ? "0.6" : "1"};">
                        <div style="font-weight: bold; margin-bottom: 8px; color: ${
                          device.already_imported ? "#888" : "#333"
                        };">
                            Device-${idx + 1}
                            ${
                              device.already_imported
                                ? '<span style="font-size: 0.8em; color: #666; font-weight: normal;"> (Already imported)</span>'
                                : ""
                            }
                        </div>
                        <div style="font-size: 0.9em; color: ${
                          device.already_imported ? "#888" : "#666"
                        }; margin-bottom: 5px;">IP: ${device.ip}</div>
                        <div style="font-size: 0.9em; color: ${
                          device.already_imported ? "#888" : "#666"
                        }; margin-bottom: 10px;">MAC: ${device.mac}</div>
                        ${
                          device.already_imported
                            ? '<button type="button" class="btn" style="font-size: 0.9em; padding: 8px 15px; background: #ccc; color: #666; cursor: not-allowed;" disabled>Already Imported</button>'
                            : `<button type="button" onclick="openImportModal('${device.mac}', '${device.ip}')" class="btn btn-primary" style="font-size: 0.9em; padding: 8px 15px;">Import Device</button>`
                        }
                    </div>
                `
                  )
                  .join("")}
            </div>
        `;
  } else if (!data.active) {
    devicesDiv.innerHTML =
      '<p style="color: #666; font-style: italic;">No devices found yet. Click "Start Device Search" to scan your network.</p>';
  }
}

function updateDiscoveryStatus(data) {
  // Keep original function for backward compatibility if needed elsewhere
  updateDiscoveryStatusModal(data);
}

function importAllDevices() {
  // Get current discovery status to find new devices
  fetch("/discover/status")
    .then((response) => response.json())
    .then((data) => {
      const newDevices = data.devices.filter(
        (device) => !device.already_imported
      );

      if (newDevices.length === 0) {
        alert("No new devices to import");
        return;
      }

      if (
        confirm(
          `Import all ${newDevices.length} new devices? You can modify device details individually after import.`
        )
      ) {
        // Import all devices with default names
        const importPromises = newDevices.map((device) => {
          const deviceName = `Device-${device.ip.split(".").pop()}`;

          const formData = new FormData();
          formData.append("name", deviceName);
          formData.append("mac", device.mac);
          formData.append("ip", device.ip);
          formData.append("description", "");

          return fetch("/add", {
            method: "POST",
            body: formData,
          });
        });

        Promise.all(importPromises)
          .then(() => {
            alert(`Successfully imported ${newDevices.length} devices!`);
            refreshDeviceList();
            checkDiscoveryStatus();
          })
          .catch((error) => {
            console.error("Error importing devices:", error);
            alert(
              "Some devices failed to import. Please try importing them individually."
            );
            refreshDeviceList();
            checkDiscoveryStatus();
          });
      }
    })
    .catch((error) => {
      console.error("Error getting discovery status:", error);
      alert("Failed to get device list");
    });
}

// Legacy function - kept for backward compatibility but no longer used
// Individual device import is now handled through the import modal
function importSingleDevice(mac) {
  console.warn(
    "importSingleDevice is deprecated. Use openImportModal instead."
  );
}

// Status monitoring management
function startStatusMonitoring() {
  if (statusMonitoringInterval) {
    clearInterval(statusMonitoringInterval);
  }

  if (document.querySelectorAll(".status-circle").length > 0) {
    statusMonitoringInterval = setInterval(updateDeviceStatus, 30000);
    // Initial update after 5 seconds
    setTimeout(updateDeviceStatus, 5000);
  }
}

// Edit Device Modal Functions
function openEditModal(deviceId, name, mac, ip, description) {
  document.getElementById("editName").value = name;
  document.getElementById("editMac").value = mac;
  document.getElementById("editIp").value = ip;
  document.getElementById("editDescription").value = description;

  // Set the form action
  document.getElementById("editForm").action = `/update/${deviceId}`;

  // Show the modal
  document.getElementById("editModal").style.display = "block";
}

function closeEditModal() {
  document.getElementById("editModal").style.display = "none";
}

// Import Device Modal Functions
function openImportModal(mac, ip) {
  // Generate a default device name based on IP
  const deviceName = `Device-${ip.split(".").pop()}`;

  document.getElementById("importName").value = deviceName;
  document.getElementById("importMac").value = mac;
  document.getElementById("importIp").value = ip;
  document.getElementById("importDescription").value = "";

  // Set the form action to add device endpoint
  document.getElementById("importForm").action = "/add";

  // Show the modal
  document.getElementById("importModal").style.display = "block";
}

function closeImportModal() {
  document.getElementById("importModal").style.display = "none";
}

function handleImportFormSubmission() {
  const form = document.getElementById("importForm");
  const formData = new FormData(form);

  fetch("/devices", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.redirected) {
        // Success - the server redirected us
        closeImportModal();
        refreshDeviceList();
        checkDiscoveryStatus();
        alert("Device imported successfully!");
      } else {
        return response.text().then((text) => {
          // Parse any error messages from the response
          throw new Error("Failed to import device");
        });
      }
    })
    .catch((error) => {
      console.error("Error importing device:", error);
      alert(
        "Failed to import device. Please check if the device already exists."
      );
    });
}

// Initialize the application
function initializeApp() {
  // Setup MAC address formatting
  setupMacAddressFormatting("mac");
  setupMacAddressFormatting("editMac");
  setupMacAddressFormatting("importMac");

  // Setup wake confirmations
  setupWakeConfirmations();

  // Setup event listeners
  const locateBtn = document.getElementById("locateDevicesBtn");
  if (locateBtn) {
    locateBtn.addEventListener("click", toggleDiscoverySection);
  }

  // Setup import form submission handler
  const importForm = document.getElementById("importForm");
  if (importForm) {
    importForm.addEventListener("submit", function (e) {
      e.preventDefault();
      handleImportFormSubmission();
    });
  }

  // Start initial monitoring
  startStatusMonitoring();

  // Close modal when clicking outside of it
  window.onclick = function (event) {
    const editModal = document.getElementById("editModal");
    const importModal = document.getElementById("importModal");

    if (event.target === editModal) {
      closeEditModal();
    }
    if (event.target === importModal) {
      closeImportModal();
    }
  };
}

// Initialize when DOM is loaded
document.addEventListener("DOMContentLoaded", initializeApp);
