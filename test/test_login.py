import json

class TestLogin:
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    def test_create_user(self, client):
        new_user = {
    	    "name": "test_root",
    	    "email": "test_root@email.com",
    	    "password": "toor_test"
        }
    
        response = client.post('/usuario', data=json.dumps(new_user), headers=self.headers)
        body = json.loads(response.data)
    
        assert response.status == '201 CREATED'
        assert body is not None
    
    def test_login(self, client):
        login_request = {
    	    "username": "test_root@email.com",
    	    "password": "toor_test"
        }
    
        response = client.post('/usuario/login', data=json.dumps(login_request), headers=self.headers)
        body = json.loads(response.data)
    
        assert response.status == '200 OK'
        assert body is not None
        assert body["token"] is not None