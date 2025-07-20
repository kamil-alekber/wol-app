# Template Structure Documentation

## Overview
The Wake-on-LAN application has been refactored to use a modular template structure for better maintainability and organization.

## Directory Structure

```
templates/
├── base.html                     # Base template with common layout
├── index.html                    # Main page template (extends base)
├── index_backup.html            # Backup of original monolithic template
└── partials/                    # Reusable template components
    ├── add_device_form.html     # Form for adding new devices
    ├── device_card.html         # Individual device card component
    ├── devices_list.html        # Grid of device cards or empty state
    ├── discovery_section.html   # Network discovery interface
    ├── edit_modal.html          # Modal for editing device details
    └── flash_messages.html      # Alert/notification messages

static/
├── css/
│   └── style.css               # All application styles
└── js/
    └── main.js                 # All JavaScript functionality
```

## Template Hierarchy

1. **base.html** - Provides the basic HTML structure, includes CSS/JS files
2. **index.html** - Extends base template and includes all partials
3. **partials/** - Modular components that can be reused

## Benefits of This Structure

1. **Modularity**: Each component is in its own file, making it easier to maintain
2. **Reusability**: Partials can be included in multiple templates
3. **Separation of Concerns**: CSS and JS are in separate files
4. **Maintainability**: Easier to locate and modify specific functionality
5. **Scalability**: Easy to add new pages or components

## Adding New Components

1. Create new partial in `templates/partials/`
2. Include it in the appropriate template using `{% include 'partials/filename.html' %}`
3. Add any specific styles to `static/css/style.css`
4. Add any specific JavaScript to `static/js/main.js`

## Customization

- **Styling**: Modify `static/css/style.css`
- **Behavior**: Modify `static/js/main.js`
- **Layout**: Modify `templates/base.html`
- **Components**: Modify files in `templates/partials/`
