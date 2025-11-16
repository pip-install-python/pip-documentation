import requests
import dash_mantine_components as dmc
from dash import html
import json

# List of all packages
PACKAGES = [
    # Currently Maintained
    'dash-summernote',
    'dash-insta-stories',
    'dash-image-gallery',
    'dash-fullcalendar',
    'dash-gauge',
    'dash-emoji-mart',
    'dash-dock',
    'dash-pannellum',
    'dash-planet',
    'dash-model-viewer',
    'dash-excalidraw',
    # Archived
    'dash-credit-cards',
    'dash-charty',
    'dash-nivo',
    'dash-discord',
    'dash-dynamic-grid-layout',
    'dash-swiper',
]

def get_total_downloads():
    """Fetch total downloads for all packages using pypistats.org API"""
    total = 0
    failed_packages = []
    successful = 0

    for package in PACKAGES:
        try:
            # Use pypistats.org overall endpoint
            url = f"https://pypistats.org/api/packages/{package}/overall"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                # Sum all downloads from the data
                if 'data' in data:
                    for entry in data['data']:
                        if 'downloads' in entry:
                            total += entry['downloads']
                    successful += 1
                    print(f"Successfully fetched {package}")
                else:
                    failed_packages.append(package)
                    print(f"No data for {package}")
            else:
                failed_packages.append(package)
                print(f"Failed to fetch {package}: status {response.status_code}")
        except Exception as e:
            failed_packages.append(package)
            print(f"Exception for {package}: {e}")

    print(f"Total: {total}, Successful: {successful}, Failed: {len(failed_packages)}")
    return total, failed_packages

def layout():
    """Create the download counter component"""
    total_downloads, failed = get_total_downloads()

    # Format the number with commas
    formatted_total = f"{total_downloads:,}"

    return dmc.Center(
        dmc.Paper(
            dmc.Stack(
                [
                    dmc.Text(
                        "Total Downloads Across All Packages",
                        size="lg",
                        fw=600,
                        ta="center",
                    ),
                    dmc.Text(
                        formatted_total,
                        size="32px",
                        fw=700,
                        ta="center",
                        c="blue",
                        style={"lineHeight": "1.2"}
                    ),
                    dmc.Text(
                        f"Across {len(PACKAGES)} packages",
                        size="sm",
                        c="dimmed",
                        ta="center",
                    ) if not failed else dmc.Text(
                        f"Across {len(PACKAGES) - len(failed)} packages ({len(failed)} failed to load)",
                        size="sm",
                        c="orange",
                        ta="center",
                    ),
                ],
                gap="xs",
                align="center",
            ),
            p="xl",
            radius="md",
            withBorder=True,
            shadow="sm",
            style={"maxWidth": "500px"}
        ),
        my="lg"
    )