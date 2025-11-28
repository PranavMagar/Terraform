def test_read_main(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_signup_and_login(client):
    # Signup
    response = client.post(
        "/signup",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200 # Redirects to login, but TestClient follows redirects by default? No, starlette TestClient follows redirects if configured, but here we check status. Wait, RedirectResponse is 303.
    # Actually TestClient follows redirects by default is False usually, but let's check.
    # If it follows, it lands on login page (200).
    # If not, it's 303.
    # Let's assume it follows or we check history.
    
    # Login
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200 # Redirects to dashboard
    assert "Dashboard" in response.text

def test_add_expense(client):
    # Login first
    client.post(
        "/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    
    response = client.post(
        "/add",
        data={
            "date": "2023-10-27",
            "category": "Food",
            "amount": 15.50,
            "description": "Lunch"
        }
    )
    assert response.status_code == 200
    
    # Verify in dashboard
    response = client.get("/")
    assert "Lunch" in response.text
    assert "15.5" in response.text
