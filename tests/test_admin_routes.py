def login(client, username, password):
    return client.post("/", data={
        "username": username,
        "password": password
    })

def test_admin_page_admin_only(client, normal_user):
    login(client, "user", "user123")
    response = client.get("/admin")
    assert response.status_code == 302

def test_admin_page(client, admin_user):
    login(client, "admin", "admin123")
    response = client.get("/admin")
    assert response.status_code == 200

def test_change_role(client, admin_user, normal_user):
    login(client, "admin", "admin123")
    response = client.get(f"/admin/change_role/{normal_user.id}")
    assert response.status_code == 302

def test_delete_self_protected(client, admin_user):
    login(client, "admin", "admin123")
    response = client.get(f"/admin/delete_user/{admin_user.id}")
    assert response.status_code == 302
