import pytest


# Simple test without any parameterization

def test_basic_addition():
    assert 1 + 1 == 2, "Basic addition failed"


# Test with parameterization
# The parameter string should be a single string with comma-separated values in the pytest decorator
# Following with the corresponding list of tuples for the test cases
@pytest.mark.parametrize("num1, num2, expected", [
    (1, 2, 3),
    (4, 5, 9),
    (10, 15, 25),
])
# The mentioned parameters should be used in the test function
def test_summation(num1, num2, expected):
    assert sum([num1, num2]) == expected, f"Should be {expected}"



# Testing with some fixture functions similar to depends behavior
@pytest.fixture
def setup_data():
    return {1: {"name": "Alice"}, 2: {"name": "Bob"}, 3: {"name": "Charlie"}}

# Simple test with fixtures
def test_user_existence(setup_data): 
    assert 1 in setup_data, "User with ID 1 should exist"
    assert 2 in setup_data, "User with ID 2 should exist"
    assert 3 in setup_data, "User with ID 3 should exist"


# Testing with both fixture and parameterization
@pytest.mark.parametrize("user_id, expected_name", [
    (1, "Alice"),
    (2, "Bob"),
    (3, "Charlie"),
])
def test_user_names(setup_data, user_id, expected_name):
    # All parameters should be used in the test function
    # setup_data is the fixture, user_id and expected_name are from parameterization
    assert setup_data[user_id]["name"] == expected_name, f"User with ID {user_id} should be {expected_name}"


def test_exception():
    # Sometimes we need to test for exceptions
    # like scenario where a user tries to register with an existing email
    with pytest.raises(Exception):
        # Since we are raising an exception in this line, and we have defined a
        # generic Exception in the pytest.raises, the test will pass
        raise Exception("This is a test exception")
    
    with pytest.raises(ZeroDivisionError):
        # This will raise a ZeroDivisionError, so the test will pass
        result = 1 / 0
    
    with pytest.raises(KeyError):
        # This will raise a KeyError, so the test will pass
        my_dict = {"a": 1, "b": 2}
        value = my_dict["c"]  # Key 'c' does not exist
    
    with pytest.raises(ValueError):
        # This will raise a ValueError, so the test will pass
        int("invalid")  # Cannot convert string to int

    # with pytest.raises(ValueError):
    #     # This will raise a ZeroDivisionError, so the test will fail
    #     # because it was expecting a ValueError. This means the scenario is not handled properly.
    #     result = 1/0