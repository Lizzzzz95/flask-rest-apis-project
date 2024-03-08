# All functions need to have the word 'test' in them, like the file names. Would be the same for classes (Test)

def test_get_stores(client):
  response = client.get('/store')
  assert response.status_code == 200
  assert response.get_json() == []

def test_get_store_when_no_store(client):
  response = client.get('/store/1')
  assert response.status_code == 404

def test_get_store_when_store(client):
  # TODO: Set up db data
  response = client.get('/store/1')
  assert response.status_code == 404