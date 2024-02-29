# Steps:
# Use: python -m venv .venv
# This installs virtual env in project folder
# User Ctrl+Shift+P -> Python Interpreter -> choose the one with 'venv' in it
# User Ctrl+J to open virtual env terminal
# Use: pip install flask
# Use: flask run
# Install all dependencies using: pip install -r requirements.txt
# For Docker build image: docker build -t <image-name> .
# For Docker volume: docker run -dp 5000:5000 -w /app -v "$(pwd):/app" <image-name>
# For Docker volume after gunicorn integration: docker run -dp 5000:5000 -w /app -v "$(pwd):/app" <image-name> sh -c "flask run --host 0.0.0.0"

# For Flask-Migrate => Start db init: flask db init  
# When you have made a change in your columns e.g. adding description = db.Column(db.String) to item model, use: flask db migrate
# This will create a new revision, then use: flask db upgrade
# This will run the upgrade() function and complete the process

import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

from db import db
from blocklist import BLOCKLIST
import models # This import is needed to SQLAlchemy knows what tables to create, essentially. Even though the import is 'unused'

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

def create_app(db_url = None):
  app = Flask(__name__)
  load_dotenv()

  app.config["PROPAGATE_EXCEPTIONS"] = True
  app.config["API_TITLE"] = "Stores REST API"
  app.config["API_VERSION"] = "v1"
  app.config["OPENAPI_VERSION"] = "3.0.3"
  app.config["OPENAPI_URL_PREFIX"] = "/"
  app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
  app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
  app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.init_app(app)
  migrate = Migrate(app, db)

  api = Api(app)

  app.config["JWT_SECRET_KEY"] = "4210685582973358662315039165615419812"
  jwt = JWTManager(app)

  @jwt.token_in_blocklist_loader
  def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST
  
  @jwt.revoked_token_loader
  def revoked_token_callback(jwt_header, jwt_payload):
    return (
      jsonify({
        "description": "The token has been revoked.",
        "error": "token_revoked"
      }),
      401
    )
  
  @jwt.needs_fresh_token_loader
  def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
      jsonify({
        "description": "The token is not fresh.",
        "error": "fresh_token_required"
      }),
      401
    )

  @jwt.additional_claims_loader
  def add_claims_to_jwt(identity):
    return {
      "is_admin": True
    }

  @jwt.expired_token_loader
  def expired_token_callback(jwt_header, jwt_payload):
    return (
      jsonify({
        "message": "The token has expired",
        "error": "token_expired"
      }),
      401
    )
  
  @jwt.invalid_token_loader
  def invalid_token_callback(error):
    return (
      jsonify({
        "message": "Signature verification failed",
        "error": "invalid_token"
      }),
      401
    )
  
  @jwt.unauthorized_loader
  def missing_token_callback(error):
    return (
      jsonify({
        "description": "Request does not contain an access token",
        "error": "authorization_required"
      }),
      401
    )

  # This code is commented out when we added migrate = Migrate(app, db). This is because Flask-Migrate will create our tables now, not SQLAlchemy
  # with app.app_context():
  #   db.create_all()

  api.register_blueprint(ItemBlueprint)
  api.register_blueprint(StoreBlueprint)
  api.register_blueprint(TagBlueprint)
  api.register_blueprint(UserBlueprint)

  return app