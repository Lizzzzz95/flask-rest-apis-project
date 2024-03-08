import pytest
from app import create_app, db

@pytest.fixture()
def app():
  app = create_app("sqlite://") # this is a temp testing db url

  with app.app_context():
    db.create_all()

  yield app

  # Anything after 'yield' means the code will run after the tear down

@pytest.fixture()
def client(app): # this will pass the fixture we created above called 'app'
  return app.test_client()
