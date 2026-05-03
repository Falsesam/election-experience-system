from assistant.engine import process_query

def test_voting():
    assert "vote" in process_query("How do people vote?").lower()

def test_registration():
    assert "register" in process_query("How to register?").lower()

def test_counting():
    assert "count" in process_query("How are votes counted?").lower()

def test_invalid():
    assert "couldn't find" in process_query("Tell me about football").lower()
