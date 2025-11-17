"""
Advertising Analytics Helper
Load and analyze advertising campaign performance data
"""
import json
from pathlib import Path
from collections import Counter
from datetime import datetime
from typing import Dict, List

from lib.advertising import CONFIG_FILE, ANALYTICS_FILE, load_config


def load_analytics_data() -> Dict:
    """Load advertising analytics data from JSON file."""
    if not ANALYTICS_FILE.exists():
        return {"clicks": [], "impressions": []}

    try:
        with open(ANALYTICS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[Ad Analytics] Error loading data: {e}")
        return {"clicks": [], "impressions": []}


def get_campaign_performance() -> List[Dict]:
    """
    Get performance metrics for each campaign.

    Returns:
        List of campaign dictionaries with performance metrics
    """
    config = load_config()
    campaigns = config.get("campaigns", [])
    analytics = load_analytics_data()

    # Count clicks and impressions per campaign
    click_counts = Counter(c['campaign_id'] for c in analytics.get('clicks', []))
    impression_counts = Counter(i['campaign_id'] for i in analytics.get('impressions', []))

    # Build performance data
    performance = []
    for campaign in campaigns:
        campaign_id = campaign['id']
        clicks = click_counts.get(campaign_id, 0)
        impressions = impression_counts.get(campaign_id, 0)

        # Calculate CTR (Click-Through Rate)
        ctr = (clicks / impressions * 100) if impressions > 0 else 0

        performance.append({
            'id': campaign_id,
            'name': campaign['name'],
            'url': campaign.get('url', '#'),
            'image': campaign.get('image', ''),
            'active': campaign.get('active', False),
            'clicks': clicks,
            'impressions': impressions,
            'ctr': round(ctr, 2),
            'start_date': campaign.get('start_date', ''),
            'end_date': campaign.get('end_date', ''),
            'description': campaign.get('description', '')
        })

    # Sort by impressions (most viewed first)
    performance.sort(key=lambda x: x['impressions'], reverse=True)

    return performance


def get_clicks_by_page() -> List[Dict]:
    """
    Get click counts grouped by page.

    Returns:
        List of dictionaries with page and click count
    """
    analytics = load_analytics_data()
    clicks = analytics.get('clicks', [])

    # Count clicks per page
    page_counts = Counter(c['page'] for c in clicks)

    # Convert to list of dicts
    result = [
        {'page': page, 'clicks': count}
        for page, count in page_counts.most_common()
    ]

    return result


def get_total_stats() -> Dict:
    """
    Get total advertising statistics.

    Returns:
        Dictionary with total clicks, impressions, and CTR
    """
    analytics = load_analytics_data()
    clicks = len(analytics.get('clicks', []))
    impressions = len(analytics.get('impressions', []))
    ctr = (clicks / impressions * 100) if impressions > 0 else 0

    active_campaigns = len([c for c in load_config().get("campaigns", []) if c.get("active", False)])

    return {
        'total_clicks': clicks,
        'total_impressions': impressions,
        'overall_ctr': round(ctr, 2),
        'active_campaigns': active_campaigns
    }