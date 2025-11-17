"""
Advertising Click Tracking Callbacks
Handles client-side click tracking for advertisement campaigns
"""
from dash import callback, Input, Output, clientside_callback, MATCH

from lib.advertising import track_click


# Track ad clicks with clientside callback for immediate navigation
clientside_callback(
    """
    function(n_clicks, campaign_data) {
        if (n_clicks && campaign_data) {
            console.log('[Advertising] Ad clicked:', campaign_data);

            // Send click tracking to server via fetch
            fetch('/api/track-ad-click', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    campaign_id: campaign_data.campaign_id,
                    page: campaign_data.page,
                    timestamp: new Date().toISOString()
                })
            }).catch(error => console.error('[Advertising] Error tracking click:', error));
        }

        return null;
    }
    """,
    Output({"type": "ad-click-tracker", "page": MATCH, "viewport": MATCH}, "children"),
    Input({"type": "ad-link", "page": MATCH, "viewport": MATCH}, "n_clicks"),
    Input({"type": "ad-campaign-data", "page": MATCH, "viewport": MATCH}, "data"),
    prevent_initial_call=True
)