"""
Visitor Analytics Tracker
Tracks visitor information including device type, bot detection, and geolocation
"""
import json
from pathlib import Path
from datetime import datetime
import re
import requests
from functools import lru_cache


class AnalyticsTracker:
    """Track visitor analytics to JSON file."""

    def __init__(self, data_file="visitor_analytics.json"):
        self.data_file = Path(data_file)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create analytics file if it doesn't exist."""
        if not self.data_file.exists():
            self.data_file.write_text(json.dumps({
                "visits": [],
                "stats": {
                    "desktop": 0,
                    "mobile": 0,
                    "tablet": 0,
                    "bot": 0,
                    "total": 0
                }
            }, indent=2))

    def detect_device_type(self, user_agent):
        """Detect device type from user agent string."""
        if not user_agent:
            return "desktop"

        user_agent = user_agent.lower()

        # Check for bots first
        if self.is_bot(user_agent):
            return "bot"

        # Check for mobile
        if any(mobile in user_agent for mobile in ['mobile', 'android', 'iphone', 'ipod', 'blackberry', 'windows phone']):
            return "mobile"

        # Check for tablet
        if any(tablet in user_agent for tablet in ['ipad', 'tablet', 'kindle']):
            return "tablet"

        return "desktop"

    def is_bot(self, user_agent):
        """Check if user agent is a bot."""
        if not user_agent:
            return False

        bot_patterns = [
            'bot', 'crawler', 'spider', 'scraper', 'curl', 'wget',
            'python-requests', 'gptbot', 'anthropic', 'claude',
            'googlebot', 'bingbot', 'slurp', 'duckduckbot',
            'perplexitybot', 'chatgpt'
        ]

        return any(pattern in user_agent.lower() for pattern in bot_patterns)

    def detect_bot_type(self, user_agent):
        """Detect the type of bot from user agent."""
        if not user_agent:
            return "unknown"

        user_agent = user_agent.lower()

        # AI Training bots
        training_bots = ['gptbot', 'anthropic-ai', 'claude-web', 'ccbot', 'google-extended', 'facebookbot']
        if any(bot in user_agent for bot in training_bots):
            return "training"

        # AI Search bots
        search_bots = ['chatgpt-user', 'claudebot', 'perplexitybot', 'youbot']
        if any(bot in user_agent for bot in search_bots):
            return "search"

        # Traditional search bots
        traditional_bots = ['googlebot', 'bingbot', 'slurp', 'duckduckbot', 'yandex', 'baidu']
        if any(bot in user_agent for bot in traditional_bots):
            return "traditional"

        return "unknown"

    def _get_session_id(self, ip_address, user_agent):
        """Generate a consistent session ID based on IP and user agent."""
        import hashlib
        session_key = f"{ip_address}:{user_agent}"
        return hashlib.md5(session_key.encode()).hexdigest()

    @lru_cache(maxsize=1000)
    def get_geolocation(self, ip_address, session_id=None):
        """Get geolocation data from IP address using ip-api.com (free service)."""
        # For local/private IPs, return consistent sample location per session
        if not ip_address or ip_address in ['127.0.0.1', 'localhost', '::1']:
            # Use session_id to consistently assign a location to each unique visitor
            # This makes development testing more realistic
            import hashlib

            # If no session_id provided, use IP as fallback
            seed_value = session_id if session_id else ip_address
            location_index = int(hashlib.md5(seed_value.encode()).hexdigest(), 16) % 10

            sample_locations = [
                {'country': 'United States', 'country_code': 'US', 'region': 'California',
                 'city': 'San Francisco', 'latitude': 37.7749, 'longitude': -122.4194, 'timezone': 'America/Los_Angeles'},
                {'country': 'United Kingdom', 'country_code': 'GB', 'region': 'England',
                 'city': 'London', 'latitude': 51.5074, 'longitude': -0.1278, 'timezone': 'Europe/London'},
                {'country': 'Japan', 'country_code': 'JP', 'region': 'Tokyo',
                 'city': 'Tokyo', 'latitude': 35.6762, 'longitude': 139.6503, 'timezone': 'Asia/Tokyo'},
                {'country': 'Germany', 'country_code': 'DE', 'region': 'Berlin',
                 'city': 'Berlin', 'latitude': 52.5200, 'longitude': 13.4050, 'timezone': 'Europe/Berlin'},
                {'country': 'Australia', 'country_code': 'AU', 'region': 'New South Wales',
                 'city': 'Sydney', 'latitude': -33.8688, 'longitude': 151.2093, 'timezone': 'Australia/Sydney'},
                {'country': 'Canada', 'country_code': 'CA', 'region': 'Ontario',
                 'city': 'Toronto', 'latitude': 43.6532, 'longitude': -79.3832, 'timezone': 'America/Toronto'},
                {'country': 'Brazil', 'country_code': 'BR', 'region': 'São Paulo',
                 'city': 'São Paulo', 'latitude': -23.5505, 'longitude': -46.6333, 'timezone': 'America/Sao_Paulo'},
                {'country': 'India', 'country_code': 'IN', 'region': 'Maharashtra',
                 'city': 'Mumbai', 'latitude': 19.0760, 'longitude': 72.8777, 'timezone': 'Asia/Kolkata'},
                {'country': 'France', 'country_code': 'FR', 'region': 'Île-de-France',
                 'city': 'Paris', 'latitude': 48.8566, 'longitude': 2.3522, 'timezone': 'Europe/Paris'},
                {'country': 'Singapore', 'country_code': 'SG', 'region': 'Singapore',
                 'city': 'Singapore', 'latitude': 1.3521, 'longitude': 103.8198, 'timezone': 'Asia/Singapore'},
            ]

            return sample_locations[location_index]

        # Skip private IP ranges
        if ip_address.startswith(('10.', '172.', '192.168.', 'fe80:', 'fc00:', 'fd00:')):
            return None

        try:
            # Use ip-api.com free API (no key required, 45 requests/minute limit)
            response = requests.get(
                f'http://ip-api.com/json/{ip_address}',
                timeout=2  # Short timeout to avoid slowing down requests
            )

            if response.status_code == 200:
                data = response.json()

                # Check if request was successful
                if data.get('status') == 'success':
                    return {
                        'country': data.get('country'),
                        'country_code': data.get('countryCode'),
                        'region': data.get('regionName'),
                        'city': data.get('city'),
                        'latitude': data.get('lat'),
                        'longitude': data.get('lon'),
                        'timezone': data.get('timezone')
                    }
        except Exception as e:
            # Silently fail - geolocation is optional
            print(f"Geolocation failed for {ip_address}: {e}")
            pass

        return None

    def track_visit(self, path, user_agent, ip_address=None):
        """Track a visitor."""
        # Skip internal Dash paths and static assets
        skip_paths = [
            '.css', '.js', '.png', '.jpg', '.ico', '.svg', '.woff', '.woff2', '.ttf', '.eot',
            '_dash', '_reload-hash', 'favicon', '/_dash-update-component',
            '/_dash-layout', '/_dash-dependencies', '/_dash-component-suites',
            '/assets/', '[]'  # Also skip malformed paths
        ]
        if any(skip in path for skip in skip_paths):
            return

        # Only track valid paths that start with /
        if not path or not path.startswith('/') or path.startswith('//'):
            return

        device_type = self.detect_device_type(user_agent)

        # Generate session ID based on IP and user agent
        session_id = self._get_session_id(ip_address or "unknown", user_agent or "unknown")

        visit_data = {
            "timestamp": datetime.now().isoformat(),
            "path": path,
            "device_type": device_type,
            "user_agent": user_agent or "Unknown",
            "session_id": session_id,
        }

        # Add bot type if it's a bot
        if device_type == "bot":
            visit_data["bot_type"] = self.detect_bot_type(user_agent)

        # Load existing data
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
        except:
            data = {"visits": [], "stats": {"desktop": 0, "mobile": 0, "tablet": 0, "bot": 0, "total": 0}}

        # Check if this session already has a visit with location data
        session_has_location = any(
            v.get('session_id') == session_id and 'location' in v
            for v in data.get('visits', [])
        )

        # Only add location data on first visit for this session
        if ip_address and not session_has_location:
            visit_data["ip_address"] = ip_address

            # Try to get geolocation with session_id for consistent localhost mapping
            geo_data = self.get_geolocation(ip_address, session_id)
            if geo_data:
                visit_data["location"] = geo_data

        # Add visit
        data["visits"].append(visit_data)

        # Update stats
        data["stats"][device_type] = data["stats"].get(device_type, 0) + 1
        data["stats"]["total"] = data["stats"].get("total", 0) + 1

        # Save data
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)


# Global tracker instance
tracker = AnalyticsTracker()
