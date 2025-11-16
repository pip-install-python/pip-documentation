"""
API Cost Logger for tracking Claude API usage and costs.

Provides centralized logging of API requests with cost calculations
and session-based tracking.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import threading


class APICostLogger:
    """Singleton logger for tracking API costs across sessions."""

    _instance = None
    _lock = threading.Lock()

    # Pricing per million tokens (as of January 2025)
    PRICING = {
        'claude-sonnet-4-20250514': {
            'input': 3.00,   # $ per 1M tokens
            'output': 15.00  # $ per 1M tokens
        },
        'claude-3-5-sonnet-20241022': {
            'input': 3.00,
            'output': 15.00
        },
        'claude-haiku-4-5-20251001': {
            'input': 0.40,
            'output': 2.00
        },
        'claude-3-haiku-20240307': {
            'input': 0.25,
            'output': 1.25
        }
    }

    def __new__(cls):
        """Ensure singleton pattern."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the logger (only once)."""
        if self._initialized:
            return

        self.log_file = Path('api-cost-breakdown.json')
        self.sessions = {}
        self._load_existing_logs()
        self._initialized = True

    def _load_existing_logs(self):
        """Load existing logs from file."""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                    self.sessions = data.get('sessions', {})
            except Exception as e:
                print(f"Error loading cost logs: {e}")
                self.sessions = {}

    def _save_logs(self):
        """Save logs to file (thread-safe)."""
        with self._lock:
            try:
                data = {
                    'last_updated': datetime.now().isoformat(),
                    'sessions': self.sessions
                }
                with open(self.log_file, 'w') as f:
                    json.dump(data, f, indent=2)
            except Exception as e:
                print(f"Error saving cost logs: {e}")

    def calculate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> Dict[str, float]:
        """
        Calculate cost for an API call.

        Args:
            model: Model name (e.g., 'claude-sonnet-4-20250514')
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Dictionary with cost breakdown
        """
        pricing = self.PRICING.get(model, self.PRICING['claude-sonnet-4-20250514'])

        input_cost = (input_tokens / 1_000_000) * pricing['input']
        output_cost = (output_tokens / 1_000_000) * pricing['output']
        total_cost = input_cost + output_cost

        return {
            'input_cost': round(input_cost, 6),
            'output_cost': round(output_cost, 6),
            'total_cost': round(total_cost, 6),
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': input_tokens + output_tokens
        }

    def log_api_request(
        self,
        session_id: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        call_type: str = 'generate',
        page_path: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """
        Log an API request with cost calculation.

        Args:
            session_id: Unique session identifier
            model: Model name
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            call_type: Type of call (e.g., 'generate', 'format', 'suggest')
            page_path: Current page path
            metadata: Additional metadata to log
        """
        cost_data = self.calculate_cost(model, input_tokens, output_tokens)

        # Initialize session if it doesn't exist
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'created_at': datetime.now().isoformat(),
                'calls': [],
                'total_cost': 0,
                'total_tokens': 0
            }

        # Create log entry
        entry = {
            'timestamp': datetime.now().isoformat(),
            'model': model,
            'call_type': call_type,
            'page_path': page_path,
            **cost_data
        }

        if metadata:
            entry['metadata'] = metadata

        # Add to session
        self.sessions[session_id]['calls'].append(entry)
        self.sessions[session_id]['total_cost'] += cost_data['total_cost']
        self.sessions[session_id]['total_tokens'] += cost_data['total_tokens']

        # Save to file
        self._save_logs()

        return entry

    def get_session_costs(self, session_id: str) -> Optional[Dict]:
        """
        Get cost summary for a session.

        Args:
            session_id: Session identifier

        Returns:
            Dictionary with session cost summary or None
        """
        return self.sessions.get(session_id)

    def get_total_costs(self) -> Dict[str, float]:
        """
        Get total costs across all sessions.

        Returns:
            Dictionary with total cost and token counts
        """
        total_cost = sum(
            session.get('total_cost', 0)
            for session in self.sessions.values()
        )
        total_tokens = sum(
            session.get('total_tokens', 0)
            for session in self.sessions.values()
        )

        return {
            'total_cost': round(total_cost, 6),
            'total_tokens': total_tokens,
            'total_sessions': len(self.sessions)
        }


# Singleton instance
_logger_instance = None


def get_logger() -> APICostLogger:
    """
    Get the singleton logger instance.

    Returns:
        APICostLogger instance
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = APICostLogger()
    return _logger_instance