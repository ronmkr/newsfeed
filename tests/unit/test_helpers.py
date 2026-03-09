import pytest
from src.utils.helpers import clean_text, get_registered_domain

def test_clean_text_normalization():
    raw = "BREAKING: New Policy Announced!   "
    expected = "breaking new policy announced"
    assert clean_text(raw) == expected

def test_clean_text_empty():
    assert clean_text("") == ""
    assert clean_text(None) == ""

def test_get_registered_domain_valid():
    url = "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms"
    assert get_registered_domain(url) == "indiatimes.com"

def test_get_registered_domain_subdomain():
    url = "news.google.co.in"
    assert get_registered_domain(url) == "google.co.in"

def test_get_registered_domain_invalid():
    assert get_registered_domain("not-a-url") is None
    assert get_registered_domain("") is None
