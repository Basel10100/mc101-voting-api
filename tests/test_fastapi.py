# import testclient from pytest
from fastapi.testclient import TestClient
import pytest
from main import voting_app  # Import the correct app instance
from utils.constants import Endpoints

client = TestClient(voting_app)



def test_read_main():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

# email, name, password, token
test_users = [
    ("test1@example.com", "test user 1", "testpassword123", None),
    ("test2@example.com", "test user 2", "testpassword456", None),
    ("test3@example.com", "test user 3", "testpassword789", None),
    ("test4@example.com", "test user 4", "testpassword012", None),
    ("test5@example.com", "test user 5", "testpassword345", None),
    ("test6@example.com", "test user 6", "testpassword678", None),
    ("test7@example.com", "test user 7", "testpassword901", None),
    ("test8@example.com", "test user 8", "testpassword234", None),
    ("test9@example.com", "test user 9", "testpassword567", None),
    ("test10@example.com", "test user 10", "testpassword890", None)
]

@pytest.mark.parametrize("email, name, password, token", test_users)
def test_user_registration(email, name, password, token):
    """Test user registration endpoint"""
    user_data = {
        "email": email,
        "password": password,
        "name": name
    } 

    response = client.post(f"/users{Endpoints.REGISTER}", json=user_data)
    print(response.json())
    assert response.status_code == 201
    assert "email" in response.json()
    assert response.json()["email"] == user_data["email"]


@pytest.mark.parametrize("email, name, password, token", test_users)
# We do not need the name for the login test, so we use _ as a placeholder
def test_user_login(email, name, password, token):
    """Test user login endpoint"""
    # First register a user
    user_data = {
        "email": email,
        "password": password, 
    }
   
    response = client.post(f"/users{Endpoints.LOGIN}", json=user_data)
    assert response.status_code == 200
    assert "token" in response.json()
    token = response.json()["token"]
    # Update the token in the test_users list
    for i in range(len(test_users)):
        if test_users[i][0] == email:
            test_users[i] = (email, name, password, token)
    # Now you can use the token for further tests
    print(f"Generated token for {email}: {token}")

candidates = [
    (1, "Candidate A", "Party X"),
    (2, "Candidate B", "Party Y"),
    (3, "Candidate C", "Party Z"),
    (4, "Candidate D", "Party W")]
# Register some candidates
@pytest.mark.parametrize("candidate_id, candidate_name, party", candidates)
def test_register_candidate(candidate_id, candidate_name, party):
    """Test candidate registration endpoint"""
    candidate_data = {
        "id": candidate_id,
        "name": candidate_name,
        "party": party
    }
    response = client.post(f"/admin{Endpoints.CANDIDATE}", json=candidate_data)
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["id"] == candidate_data["id"]

# user_id, candidate_id
votes = [
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 2),
    (6, 2),
    (7, 2),
    (8, 3),
    (9, 3),
    (10, 4)
]
@pytest.mark.parametrize("user_id, candidate_id", votes)
def test_vote_candidate(user_id, candidate_id):
    """Test voting endpoint"""
    email, name, password, token = test_users[user_id - 1]  # user_id starts from 1
    voting_data = {
        "candidate_id": candidate_id
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post(f"/users{Endpoints.VOTING}", json=voting_data, headers=headers)
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["candidate_id"] == voting_data["candidate_id"]


vote_counts = {
    1: {"candidate_id": 1, "candidate_name": "Candidate A", "vote_count": 4},
    2: {"candidate_id": 2, "candidate_name": "Candidate B", "vote_count": 3},
    3: {"candidate_id": 3, "candidate_name": "Candidate C", "vote_count": 2},
    4: {"candidate_id": 4, "candidate_name": "Candidate D", "vote_count": 1}
}

# Get the vote counts 
def test_get_vote_counts():
    """Test get vote counts endpoint""" 
    response = client.get(f"/admin{Endpoints.VOTE_COUNTS}")
    assert response.status_code == 200
    for vote_count in response.json():
        assert vote_count["candidate_id"] == vote_counts[vote_count["candidate_id"]]["candidate_id"]
        assert vote_count["candidate_name"] == vote_counts[vote_count["candidate_id"]]["candidate_name"]
        assert vote_count["vote_count"] == vote_counts[vote_count["candidate_id"]]["vote_count"]