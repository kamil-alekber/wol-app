# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of our software seriously. If you discover a security vulnerability, please follow these steps:

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by email to: [your-email@example.com]

Include the following information in your report:

- **Description of the vulnerability**: Provide a clear description of the issue
- **Steps to reproduce**: Include detailed steps to reproduce the vulnerability
- **Potential impact**: Describe what an attacker might be able to achieve
- **Suggested fix**: If you have ideas for how to fix the issue, please include them
- **Your contact information**: So we can follow up with questions if needed

### What to Expect

After you submit a vulnerability report, here's what you can expect:

- **Acknowledgment**: We'll acknowledge receipt of your report within 48 hours
- **Assessment**: We'll assess the vulnerability and determine its severity
- **Timeline**: We'll provide an estimated timeline for addressing the issue
- **Updates**: We'll keep you informed of our progress
- **Credit**: We'll credit you in our security advisory (unless you prefer to remain anonymous)

### Security Response Timeline

- **Initial Response**: Within 48 hours
- **Vulnerability Assessment**: Within 1 week
- **Fix Development**: Timeline depends on severity and complexity
- **Release**: Security fixes are prioritized and released as soon as possible

## Security Best Practices

When using this application, please follow these security best practices:

### Network Security
- Run the application behind a firewall or reverse proxy
- Use HTTPS in production environments
- Restrict access to trusted networks when possible
- Monitor network traffic for suspicious activity

### Configuration Security
- Change default passwords and secret keys
- Regularly update configuration files
- Limit user permissions appropriately
- Enable logging and monitoring

### System Security
- Keep Python and dependencies up to date
- Run the application with minimal required privileges
- Regularly update the operating system
- Monitor system logs for unusual activity

### Device Security
- Ensure target devices have appropriate security measures
- Use strong passwords on target devices
- Keep target device firmware updated
- Consider network segmentation for WOL targets

## Known Security Considerations

This application has the following security considerations by design:

1. **Network Access**: The application requires network access to send WOL packets
2. **Device Control**: The application can wake up devices on the network
3. **Configuration Storage**: Device information is stored in local files
4. **Web Interface**: The application exposes a web interface that should be secured

## Dependency Security

I regularly monitor our dependencies for security vulnerabilities:

- Dependencies are listed in `requirements.txt`
- I use automated security scanning in my CI/CD pipeline
- Security updates are applied promptly
- I follow security advisories for all dependencies

## Disclosure Policy

When I receive a security bug report, I will:

1. Confirm the problem and determine affected versions
2. Audit code to find any similar problems
3. Prepare fixes for the most recent release and other supported versions
4. Release patched versions as quickly as possible
5. Publish a security advisory with appropriate credit

## Comments on This Policy

If you have suggestions on how this process could be improved, please submit a pull request or create an issue.
