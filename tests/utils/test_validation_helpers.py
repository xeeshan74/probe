from utils.validation_helpers import is_valid_domain

def test_is_valid_domain():
    assert is_valid_domain("example.com") == True
    assert is_valid_domain("sub.example.com") == True
    assert is_valid_domain("invalid_domain") == False