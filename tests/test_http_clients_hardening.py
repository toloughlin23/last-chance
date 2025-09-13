#!/usr/bin/env python3
import inspect

from services.http import HttpClient


def test_http_client_defaults_are_bounded():
    client = HttpClient()
    # Ensure non-zero bounded defaults
    assert getattr(client, 'timeout', getattr(client, 'timeout_seconds', 0)) > 0
    assert getattr(client, 'max_retries', 0) >= 1


def test_http_client_timeout_signature():
    # Verify requests.get is called with timeout arg by inspecting source
    src = inspect.getsource(HttpClient.get_json)
    assert 'timeout=' in src

