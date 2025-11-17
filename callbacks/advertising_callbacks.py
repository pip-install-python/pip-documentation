"""
Advertising Click Tracking Callbacks
Handles client-side click tracking for advertisement campaigns
"""
from dash import callback, Input, Output, clientside_callback, MATCH, no_update, ctx
from flask import request, jsonify

from lib.advertising import track_click


# Server-side API endpoint for tracking ad clicks (Dash 3.3.0)
@callback(
    Output('ad-click-api-response', 'data'),  # Dummy output
    Input('ad-click-api-trigger', 'data'),      # Dummy input
    api_endpoint='/api/track-ad-click',
    hidden=True
)
def track_ad_click_api(trigger_data):
    """
    API endpoint to track advertisement clicks.

    This callback serves as an API endpoint that can be called directly
    via POST requests from the clientside callback below.

    Expected JSON body:
        - campaign_id: ID of the campaign clicked
        - page: Page where click occurred
        - timestamp: ISO timestamp of click
    """
    # If called from within Dash (not as API), return no_update
    if ctx.triggered_id == 'ad-click-api-trigger':
        return no_update

    # API call behavior - get JSON data from request
    try:
        data = request.get_json()
        campaign_id = data.get('campaign_id')
        page = data.get('page')
        session_id = request.headers.get('X-Session-ID')

        if campaign_id and page:
            track_click(campaign_id, page, session_id)
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"error": "Missing required fields"}), 400

    except Exception as e:
        print(f"[Advertising API] Error tracking click: {e}")
        return jsonify({"error": str(e)}), 500


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
    prevent_initial_call=True,
    hidden=True  # Dash 3.3.0: Hide infrastructure callback from dev tools
)