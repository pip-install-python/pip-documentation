"""
Advertising Module
Handles random ad selection, display, and click tracking for documentation pages
"""
import json
import random
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import threading

import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify


# Thread lock for file operations
_lock = threading.Lock()

# Config file paths
CONFIG_FILE = Path("advertising_config.json")
ANALYTICS_FILE = Path("advertising_analytics.json")


def load_config() -> Dict:
    """Load advertising configuration from JSON file."""
    if not CONFIG_FILE.exists():
        return {"campaigns": []}

    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[Advertising] Error loading config: {e}")
        return {"campaigns": []}


def get_active_campaigns() -> List[Dict]:
    """
    Get list of active advertising campaigns.

    Returns:
        List of active campaign dictionaries
    """
    config = load_config()
    campaigns = config.get("campaigns", [])

    # Filter for active campaigns only
    active_campaigns = [
        campaign for campaign in campaigns
        if campaign.get("active", False)
    ]

    return active_campaigns


def get_random_campaign() -> Optional[Dict]:
    """
    Select a random active advertising campaign.

    Returns:
        Campaign dictionary or None if no campaigns available
    """
    campaigns = get_active_campaigns()

    if not campaigns:
        return None

    return random.choice(campaigns)


def track_impression(campaign_id: str, page: str):
    """
    Track an advertisement impression (view) with deduplication.

    Only tracks if there isn't a recent impression (within 10 seconds)
    for the same campaign on the same page to prevent duplicate tracking
    during layout re-renders.

    Args:
        campaign_id: ID of the campaign shown
        page: Page where ad was shown
    """
    if not ANALYTICS_FILE.exists():
        ANALYTICS_FILE.write_text(json.dumps({"clicks": [], "impressions": []}))

    try:
        with _lock:
            with open(ANALYTICS_FILE, 'r') as f:
                data = json.load(f)

            now = datetime.now()

            # Check for recent duplicate impressions (within last 10 seconds)
            recent_impressions = data.get("impressions", [])
            for imp in reversed(recent_impressions[-20:]):  # Check last 20 impressions
                if imp.get("campaign_id") == campaign_id and imp.get("page") == page:
                    try:
                        imp_time = datetime.fromisoformat(imp["timestamp"])
                        time_diff = (now - imp_time).total_seconds()

                        if time_diff < 10:  # Within 10 seconds
                            # Duplicate impression, skip tracking
                            return
                    except:
                        pass

            # No recent duplicate found, track the impression
            impression = {
                "campaign_id": campaign_id,
                "page": page,
                "timestamp": now.isoformat(),
            }

            data["impressions"].append(impression)

            with open(ANALYTICS_FILE, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"[Advertising] Impression tracked: {campaign_id} on {page}")

    except Exception as e:
        print(f"[Advertising] Error tracking impression: {e}")


def track_click(campaign_id: str, page: str, session_id: str = None):
    """
    Track an advertisement click.

    Args:
        campaign_id: ID of the campaign clicked
        page: Page where click occurred
        session_id: Optional session identifier
    """
    if not ANALYTICS_FILE.exists():
        ANALYTICS_FILE.write_text(json.dumps({"clicks": [], "impressions": []}))

    try:
        with _lock:
            with open(ANALYTICS_FILE, 'r') as f:
                data = json.load(f)

            click = {
                "campaign_id": campaign_id,
                "page": page,
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id
            }

            data["clicks"].append(click)

            with open(ANALYTICS_FILE, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"[Advertising] Click tracked: {campaign_id} on {page}")

    except Exception as e:
        print(f"[Advertising] Error tracking click: {e}")


def create_ad_component(page_name: str, viewport: str = "desktop") -> html.Div:
    """
    Create an advertisement component with random campaign selection and click tracking.

    Args:
        page_name: Page identifier for unique IDs and tracking
        viewport: "mobile" or "desktop" for unique IDs

    Returns:
        Dash component with clickable advertisement
    """
    # Get random campaign
    campaign = get_random_campaign()

    if not campaign:
        # No campaigns available, return empty div
        return html.Div(id={"type": "ad-container", "page": page_name, "viewport": viewport})

    # Track impression
    track_impression(campaign['id'], page_name)

    # Store campaign data in a hidden div for click tracking
    campaign_data_store = dcc.Store(
        id={"type": "ad-campaign-data", "page": page_name, "viewport": viewport},
        data={
            "campaign_id": campaign['id'],
            "campaign_url": campaign.get('url', '#'),
            "page": page_name
        }
    )

    return html.Div(
        id={"type": "ad-container", "page": page_name, "viewport": viewport},
        children=[
            campaign_data_store,
            # Hidden div for click tracking callback output
            html.Div(id={"type": "ad-click-tracker", "page": page_name, "viewport": viewport}, style={"display": "none"}),
            dmc.Divider(
                label="Advertisement",
                labelPosition="center",
                mb="md",
                mt="xl",
                styles={
                    "label": {
                        "fontSize": "0.75rem",
                        "fontWeight": 600,
                        "textTransform": "uppercase",
                        "letterSpacing": "0.5px",
                        "color": "var(--mantine-color-gray-6)"
                    }
                }
            ),
            html.A(
                href=campaign.get('url', '#'),
                target="_blank",
                rel="noopener noreferrer",
                id={"type": "ad-link", "page": page_name, "viewport": viewport},
                style={"textDecoration": "none"},
                children=[
                    dmc.Paper(
                        [
                            html.Img(
                                id={"type": "ad-image", "page": page_name, "viewport": viewport},
                                src=campaign.get('image', ''),
                                alt=campaign.get('name', 'Advertisement'),
                                style={
                                    "width": "100%",
                                    "height": "auto",
                                    "display": "block",
                                    "borderRadius": "8px",
                                    "transition": "transform 0.2s ease"
                                },
                                className="ad-image"
                            ),
                            dmc.Text(
                                [
                                    DashIconify(icon="tabler:info-circle", width=12, style={"marginRight": "4px"}),
                                    "Sponsored Content"
                                ],
                                size="xs",
                                c="gray",
                                ta="center",
                                mt="xs",
                                style={"display": "flex", "alignItems": "center", "justifyContent": "center"}
                            )
                        ],
                        p="md",
                        withBorder=True,
                        radius="md",
                        className="ad-paper",
                        style={
                            "cursor": "pointer",
                            "transition": "transform 0.2s ease, box-shadow 0.2s ease"
                        }
                    )
                ]
            )
        ]
    )