"""The dataset consent question is only asked when data could actually be sent."""

import MCP_Server.dataset.consent as consent


def test_never_asks_without_credentials(monkeypatch):
    monkeypatch.setattr(consent, "needs_prompt", lambda: True)
    monkeypatch.setattr(consent, "collection_possible", lambda: False)
    assert consent.may_ask_now() is False
    assert consent.maybe_consent_notice() == ""


def test_asks_when_collection_is_configured(monkeypatch):
    monkeypatch.setattr(consent, "needs_prompt", lambda: True)
    monkeypatch.setattr(consent, "collection_possible", lambda: True)
    monkeypatch.setattr(consent, "_read_state", lambda: {})
    assert consent.may_ask_now() is True


def test_this_repository_ships_no_credentials():
    # config.py is gitignored: a clean install can't collect anything.
    assert consent.collection_possible() is False
