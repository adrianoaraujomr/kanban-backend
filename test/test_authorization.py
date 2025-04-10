import json

class TestAuthorization:
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    def test_authorization_success(self, client):    
        response = client.post('/usuario/login', data=json.dumps({"username": "root@email.com", "password": "toor"}), headers=self.headers)
        body = json.loads(response.data)
    
        assert response.status == '200 OK'
        assert body is not None
        assert body["token"] is not None

        token = body["token"]
        auth_header = self.headers
        auth_header["Authorization"] = f"Bearer {token}"
        response = client.get('/usuario', headers=auth_header)
        body = json.loads(response.data)

        assert response.status == '200 OK'
        assert len(body) == 1


    def test_fail_authentication(self, client):
        new_user = {
     	   "name": "test_root",
     	   "email": "test_root@email.com",
     	   "password": "toor_test"
        }
        login_request = {
     	   "username": "test_root@email.com",
     	   "password": "toor_test"
        }
    
        response = client.post('/usuario', data=json.dumps(new_user), headers=self.headers)
        body = json.loads(response.data)
    
        assert response.status == '201 CREATED'
        assert body is not None
    
        response = client.post('/usuario/login', data=json.dumps(login_request), headers=self.headers)
        body = json.loads(response.data)
    
        assert response.status == '200 OK'
        assert body is not None
        assert body["token"] is not None

        token = body["token"]
        auth_header = self.headers
        auth_header["Authorization"] = f"Bearer {token}"

        response = client.get('/to-do-card', headers=auth_header)

        assert response.status == '200 OK'
        
        response = client.get('/usuario', headers=auth_header)

        assert response.status == '403 FORBIDDEN'