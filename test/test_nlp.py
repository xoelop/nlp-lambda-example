from src.nlp import find_locations


def test_find_locations():
    text = 'Spain is a sunnier country than the UK'
    locations = find_locations(text=text)
    assert 'Spain' in locations
    assert 'UK' in locations
