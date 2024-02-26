from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description = "Operations on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):

  @jwt_required()
  @blp.response(200, ItemSchema)
  def get(self, item_id):
    item = ItemModel.query.get_or_404(item_id)
    return item

  @jwt_required()
  @blp.arguments(ItemUpdateSchema)
  @blp.response(200, ItemSchema) # order of decorators matter, response should be deeper than arguments
  def put(self, item_data, item_id): # blue arguments schema request body goes in first, in this case: item_data
    item = ItemModel.query.get(item_id)

    if item:
      item.price = item_data["price"]
      item.name = item_data["name"]
    else:
      item = ItemModel(id = item_id, **item_data)

    db.session.add(item)
    db.session.commit()

    return item
  
  @jwt_required()
  def delete(self, item_id):
    
    jwt = get_jwt()
    if not jwt.get("is_admin"):
      abort(401, message = "Admin privilege required")

    item = ItemModel.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return {
      "message": "Item deleted"
    }
    # raise NotImplementedError("Deleting an item is not implemented.") # standard way for communicating to client that this feature is not implemented yet, used in development


@blp.route("/item")
class ItemList(MethodView):

  @jwt_required()
  @blp.response(200, ItemSchema(many = True)) # many = True makes ItemSchema into a list, basically
  def get(self):
    return ItemModel.query.all()
  
  @jwt_required(fresh = True)
  @blp.arguments(ItemSchema)
  @blp.response(201, ItemSchema)
  def post(self, item_data):
    item = ItemModel(**item_data) # ** will turn the dict into key-word arguments

    try:
      db.session.add(item)
      db.session.commit() # basically saves everything at once, so you add many things, then commit once
    except SQLAlchemyError:
      abort(500, message = "An error occured while inserting the item.")

    return item