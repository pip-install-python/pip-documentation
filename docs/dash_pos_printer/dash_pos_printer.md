---
name: POS Printer
description: Cloud-based receipt printing for Dash applications using Star Micronics printers and CloudPRNT
endpoint: /components/dash-pos-printer
package: star-micronics-cloudprnt
icon: tabler:printer
---

.. toc::

.. llms_copy::POS Printer

# Star Micronics POS Printer Integration

A comprehensive cloud-based receipt printing system for Dash applications, enabling remote printer management, real-time status monitoring, and automated order printing through the Star Micronics CloudPRNT platform.

---
.. exec::docs.dash_pos_printer.banner
    :code: false

## Overview

The Star Micronics POS Printer integration connects your Dash application to physical receipt printers via the **StarIO.Online** cloud service. This enables:

- **Remote Cloud Printing** - Send print jobs from anywhere via REST API
- **Real-Time Status Monitoring** - Track printer health, paper levels, and queue status
- **Automatic Order Printing** - Print receipts on successful checkout/payment
- **Web-Based Management** - Full-featured admin dashboard for printer control
- **Multiple Print Formats** - Text markup, images, QR codes, and barcodes
- **Queue Management** - Monitor and clear pending print jobs

### Key Features

- ✅ **Zero Infrastructure** - No local print server required, fully cloud-based
- ✅ **Production Ready** - Used in live POS systems with Stripe integration
- ✅ **Multi-Printer Support** - Manage multiple printers from single dashboard
- ✅ **Mobile Responsive** - Admin dashboard works on all devices
- ✅ **Error Handling** - Comprehensive diagnostics and retry logic
- ✅ **Secure** - Admin-only access with Clerk authentication
- ✅ **Theme Aware** - Automatic dark/light mode support

---

## Supported Hardware

### Compatible Printers

**mC-Print Series:**
- mC-Print2 (firmware 1.2+)
- mC-Print3 (firmware 1.2+, MQTT support 5.1+)

**TSP Series:**
- TSP100IV (firmware 1.0+, MQTT support 2.2+)

All printers must support the **CloudPRNT** protocol for cloud connectivity.

### Connection Modes

- **HTTP Polling** - Compatible with all firmware versions (3-5 second intervals)
- **MQTT** - Real-time push notifications (requires newer firmware)

---

## Installation

### Prerequisites

```bash
pip install requests python-dotenv Pillow qrcode[pil]
```

### Required Dependencies

```python
dash==3.3.0
dash-mantine-components==2.4.0
requests==2.32.4
python-dotenv==1.1.0
Pillow>=10.0.0
qrcode[pil]>=7.4.2
```

### GitHub Repository

The complete integration includes two core files:

- `printer_service.py` - Star Micronics API wrapper
- `pages/printer.py` - Admin management dashboard

---

## Quick Start

### 1. StarIO.Online Account Setup

**Register for Account:**
```bash
# Visit registration page
https://www.starmicronicscloud.com

# Select your region:
US: https://api.stario.online
EU: https://eu-api.stario.online
```

**Create Device Group:**
1. Navigate to "Device Groups" in dashboard
2. Create new group (e.g., "your-restaurant")
3. Note the **Group Path** (e.g., `yourcompany`)
4. Enable settings:
   - ✅ AutoCreateDeviceQueue
   - ✅ WelcomePrint
   - ❌ RequireDeviceKey

**Generate API Key:**
1. Navigate to "API Keys"
2. Create new key with permissions:
   - ✅ PrintToDevice
   - ✅ ViewDeviceGroups
   - ✅ ViewDevice
   - ✅ FlushQueue
   - ✅ ModifyDevice
3. Save API key securely (shown only once)

### 2. Printer Configuration

**Get CloudPRNT URL:**
```
Format: https://api.stario.online/v1/a/{GROUP_PATH}/cloudprnt
Example: https://api.stario.online/v1/a/yourcompany/cloudprnt
```

**Configure Printer:**
1. Access printer web interface (http://[PRINTER_IP])
2. Navigate to Settings → CloudPRNT
3. Enable CloudPRNT
4. Enter CloudPRNT URL
5. Set polling interval: 3-5 seconds
6. Save and restart printer

### 3. Environment Variables

Create `.env` file in project root:

```bash
# Star Micronics Configuration
STAR_MICRONICS=your_api_key_here
STAR_GROUP_PATH=yourcompany
STAR_DEVICE_ID=ABC123DEF456  # Optional: default device
```

---

## Device Status Example

Monitor printer health with real-time status cards:

.. exec::docs.dash_pos_printer.device_status_example
    :code: false

.. sourcetabs::docs/dash_pos_printer/device_status_example.py
    :defaultExpanded: false
    :withExpandedButton: true

This example demonstrates:
- Real-time device status monitoring
- Health diagnostics with color-coded indicators
- Connection mode detection (HTTP vs MQTT)
- Paper level warnings
- Queue status tracking

---

## Print Receipt Example

Send formatted receipts to your printer:

.. exec::docs.dash_pos_printer.print_receipt_example
    :code: false

.. sourcetabs::docs/dash_pos_printer/print_receipt_example.py
    :defaultExpanded: false
    :withExpandedButton: true

Features:
- Star Document Markup formatting
- Text alignment (left, center, right)
- Bold and sized text
- Automatic paper cutting
- Buzzer alerts

---

## Live Printer Test

Send custom messages directly to your actual Star Micronics printer:

.. exec::docs.dash_pos_printer.live_print_example
    :code: false

.. sourcetabs::docs/dash_pos_printer/live_print_example.py
    :defaultExpanded: false
    :withExpandedButton: true

This example connects to your real printer using the Star Micronics CloudPRNT API. Features:
- **Real API Connection** - Uses environment variables to connect to actual printer
- **Custom Message Composer** - Write any message with live preview
- **Template Library** - Pre-built templates for quick printing
- **Live Formatting** - Automatic date/time injection
- **Error Handling** - Comprehensive error messages and diagnostics
- **Connection Status** - Shows printer availability and configuration

**Environment Variables Required:**
- `STAR_MICRONICS` - Your Star Micronics API key
- `STAR_GROUP_PATH` - Your device group path
- `STAR_DEVICE_ID` - Target printer device ID
- `STAR_REGION` - API region (US or EU)

---

## Star Document Markup

The system uses Star Document Markup for formatting receipts:

### Text Formatting

```python
# Alignment
"[align: left]Left aligned text"
"[align: center]Centered text"
"[align: right]Right aligned text"

# Bold text
"[bold]Bold text[normal]"

# Text sizing
"[mag: w 2; h 1]Double width"
"[mag: w 1; h 2]Double height"
"[mag: w 2; h 2]Double both"

# Paper cut (required at end)
"[cut]"
```

### Example Receipt

```python
receipt = """[align: center]
[bold][mag: w 2; h 2]YOUR STORE[normal][mag: w 1; h 1]
================================

[align: left]
Order #: ORD-12345
Customer: John Doe
Date: 11/17/2025

================================
[bold]ITEMS:[normal]
2x Lobster Roll         $35.98
1x Clam Chowder         $12.99
--------------------------------
Subtotal:               $48.97
Tax (8.25%):            $4.04
================================
[bold]TOTAL:                  $52.01[normal]

Payment: Credit Card

[align: center]
Thank you for your order!
Visit us again soon!

[cut]"""
```

---

## Printer Management Dashboard

Full-featured admin dashboard for printer control:

.. exec::docs.dash_pos_printer.printer_dashboard_example
    :code: false

.. sourcetabs::docs/dash_pos_printer/printer_dashboard_example.py
    :defaultExpanded: false
    :withExpandedButton: true

Dashboard Features:
- **Device Overview** - Real-time status for all printers
- **Print Queue** - View and manage pending jobs
- **Quick Print** - Template prints and custom jobs
- **Diagnostics** - System health analysis
- **Print History** - Last 20 print jobs with status

---

## StarPrinterService API

### Initialization

```python
from printer_service import StarPrinterService

# Initialize (reads from .env)
printer = StarPrinterService()
```

### Device Management

```python
# List all devices
devices = printer.get_device_list()

for device in devices:
    print(f"Device: {device['Id']}")
    print(f"Online: {device['Status']['Online']}")
    print(f"Queue: {device['QueuedJobs']} jobs")

# Get specific device status
status = printer.get_device_status('ABC123DEF456')
```

### Print Operations

```python
# Basic print
result = printer.print_receipt(
    content="[align: center]Hello World\n[cut]",
    job_name="Test_Print",
    device_id="ABC123DEF456"
)

# Print with buzzer
result = printer.print_receipt(
    content=receipt_content,
    job_name="Order_12345",
    device_id="ABC123DEF456",
    startbuzzer=2,  # Buzz twice before
    endbuzzer=1     # Buzz once after
)

# Print multiple copies
result = printer.print_receipt(
    content=receipt_content,
    copies=3,
    device_id="ABC123DEF456"
)

# Check result
if 'JobId' in result:
    print(f"✅ Success! Job ID: {result['JobId']}")
else:
    print(f"❌ Error: {result.get('error')}")
```

### Queue Management

```python
# Clear all pending jobs
success = printer.clear_queue('ABC123DEF456')

if success:
    print("✅ Queue cleared successfully")
```

### Generate Receipt from Order

```python
order_data = {
    'order_number': 'ORD-12345',
    'customer_name': 'John Doe',
    'customer_phone': '(555) 123-4567',
    'items': [
        {'name': 'Lobster Roll', 'quantity': 2, 'amount': 35.98},
        {'name': 'Clam Chowder', 'quantity': 1, 'amount': 12.99}
    ],
    'amount': 48.97,
    'payment_method': 'Credit Card'
}

# Generate formatted receipt
receipt_markup = printer.generate_receipt_markup(order_data)

# Print it
printer.print_receipt(receipt_markup, job_name=f"Order_{order_data['order_number']}")
```

---

## Configuration Example

Step-by-step setup guide with visual feedback:

.. exec::docs.dash_pos_printer.setup_guide_example
    :code: false

.. sourcetabs::docs/dash_pos_printer/setup_guide_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

## Automatic Order Printing

Integrate with your checkout process to automatically print receipts:

```python
from printer_service import StarPrinterService
import stripe

def on_checkout_success(session_id):
    """Print receipt when customer completes checkout"""

    # Retrieve order from Stripe
    session = stripe.checkout.Session.retrieve(
        session_id,
        expand=['line_items', 'line_items.data.price.product']
    )

    # Format order data
    order_data = {
        'order_number': session.id[:12].upper(),
        'customer_name': session.customer_details.name,
        'customer_phone': session.customer_details.phone,
        'items': format_line_items(session.line_items),
        'amount': session.amount_total / 100,
        'payment_method': 'Credit Card'
    }

    # Print receipt
    printer = StarPrinterService()
    receipt = printer.generate_receipt_markup(order_data)

    result = printer.print_receipt(
        receipt,
        job_name=f"Order_{order_data['order_number']}",
        startbuzzer=2  # Alert staff with 2 beeps
    )

    if 'JobId' in result:
        print(f"✅ Receipt printed! Job ID: {result['JobId']}")
    else:
        print(f"⚠️ Print failed: {result.get('error')}")
        # Queue for retry or alert admin
```

---

## Troubleshooting

### Printer Shows Offline

**Symptoms:**
- Device appears offline in dashboard
- Status shows "Printer is offline"

**Solutions:**
```bash
# Check network connection
ping [PRINTER_IP]

# Verify CloudPRNT URL
# Should be: https://api.stario.online/v1/a/[GROUP_PATH]/cloudprnt

# Check StarIO.Online dashboard
# Device should appear under Device Groups

# Restart printer
# Power cycle and wait 30 seconds
```

### Jobs Stuck in Queue

**Symptoms:**
- QueuedJobs count > 0
- Jobs not printing
- LastConnection timestamp increasing

**Solutions:**
```python
# Check connection mode
status = printer.get_device_status(device_id)
last_conn = status['LastConnection']

if last_conn == 0:
    print("MQTT mode - check firmware version")
    print("Required: mC-Print3 5.1+ or TSP100IV 2.2+")
else:
    print(f"HTTP polling - last seen {last_conn}s ago")
    if last_conn > 60:
        print("Printer not polling - verify CloudPRNT URL")

# Clear stuck queue
printer.clear_queue(device_id)
```

### Authentication Errors

**Symptoms:**
- "API key not found" error
- 401 Unauthorized responses

**Solutions:**
```bash
# Verify .env file exists and is correct
cat .env | grep STAR_MICRONICS

# Ensure no spaces in values
STAR_MICRONICS=your_key_here  # Correct
STAR_MICRONICS= your_key_here  # Wrong (has space)

# Check API key permissions in StarIO.Online dashboard
# Required: PrintToDevice, ViewDeviceGroups, ViewDevice, FlushQueue

# Test connection
python printer_service.py
```

---

## Component Properties

### StarPrinterService Class

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `api_key` | string | env: STAR_MICRONICS | Star Micronics API key for authentication |
| `group_path` | string | env: STAR_GROUP_PATH | Device group path from StarIO.Online |
| `device_id` | string | env: STAR_DEVICE_ID | Optional default device identifier |
| `base_url` | string | https://api.stario.online/v1 | API base URL (US region) |

### Method: print_receipt()

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `content` | string | Required | Star Markup formatted receipt content |
| `job_name` | string | None | Name for job tracking in dashboard |
| `device_id` | string | None | Target device (uses default if not set) |
| `copies` | integer | 1 | Number of copies to print (1-10) |
| `startbuzzer` | integer | 0 | Number of beeps before printing (0-3) |
| `endbuzzer` | integer | 0 | Number of beeps after printing (0-3) |

### Device Status Object

| Property | Type | Description |
|:---------|:-----|:------------|
| `Id` | string | Device name/identifier |
| `AccessIdentifier` | string | Unique device ID for API calls |
| `Mac` | string | MAC address of printer |
| `ClientType` | string | Printer model (e.g., mC-Print3) |
| `Status.Online` | boolean | Whether printer is connected |
| `Status.PaperEmpty` | boolean | Paper roll is empty |
| `Status.PaperLow` | boolean | Paper roll is running low |
| `Status.CoverOpen` | boolean | Printer cover is open |
| `QueuedJobs` | integer | Number of pending print jobs |
| `LastConnection` | integer | Seconds since last poll (0 for MQTT) |
| `PaperWidthMM` | integer | Paper width in millimeters (72 or 80) |
| `PollingInterval` | integer | Polling interval in seconds |

---

## Best Practices

### 1. Error Handling

Always wrap printer calls in try-except blocks:

```python
def safe_print(content, device_id):
    try:
        printer = StarPrinterService()
        result = printer.print_receipt(content, device_id=device_id)

        if 'error' in result:
            # Log error but don't fail checkout
            logger.error(f"Print error: {result['error']}")
            # Maybe queue for retry
            return False

        return True

    except Exception as e:
        logger.exception(f"Printer exception: {e}")
        # Alert admin but continue
        return False
```

### 2. Queue Monitoring

Monitor print queues and alert on issues:

```python
def check_queue_health():
    """Run periodically to monitor queue health"""
    printer = StarPrinterService()
    devices = printer.get_device_list()

    for device in devices:
        queue_count = device.get('QueuedJobs', 0)

        if queue_count > 10:
            # Alert admin
            send_alert(f"Printer {device['Id']} has {queue_count} pending jobs")

        if queue_count > 50:
            # Auto-clear very old jobs
            printer.clear_queue(device['AccessIdentifier'])
```

### 3. Receipt Design

Design for thermal printer constraints:

```python
# GOOD: Clear, readable, proper width
receipt = """[align: center]
[bold][mag: w 2; h 2]RESTAURANT NAME[normal][mag: w 1; h 1]

[align: left]
Order: 12345
2x Item Name      $35.98
1x Another Item   $12.99
--------------------------
TOTAL:            $48.97

[align: center]
Thank you!
[cut]"""

# BAD: Too wide, will wrap or cut off
# Lines should not exceed 32 chars for 72mm paper
# or 48 chars for 80mm paper
```

### 4. Performance Optimization

Cache device status to reduce API calls:

```python
import time

class CachedPrinterService:
    def __init__(self):
        self.printer = StarPrinterService()
        self._devices_cache = None
        self._cache_time = 0
        self._cache_ttl = 30  # 30 seconds

    def get_device_list(self):
        now = time.time()
        if self._devices_cache is None or (now - self._cache_time) > self._cache_ttl:
            self._devices_cache = self.printer.get_device_list()
            self._cache_time = now
        return self._devices_cache
```

---

## Resources

### Official Documentation
- [Star Micronics Docs](https://docs.star-m.com)
- [StarIO.Online Dashboard](https://api.stario.online) (US) / [EU](https://eu-api.stario.online)
- [CloudPRNT Specification](https://docs.star-m.com) - Available in dashboard Help section

### Printer Manuals
- [mC-Print3 Manual](https://star-m.jp/products/s_print/mcprint31_oml/manual_en.html)
- [TSP100IV Manual](https://star-m.jp/products/s_print/tsp100iv_oml/manual_en.html)

### Support
- [Plotly Community Forum](https://community.plotly.com)
- [GitHub Issues](https://github.com/pip-install-python)

---

*Last Updated: November 2025*