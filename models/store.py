from db import db

class StoreModel(db.Model):
  
  __tablename__ = "stores"

  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(80), unique = True, nullable = False)
  items = db.relationship("ItemModel", back_populates = "store", lazy = "dynamic", cascade = "all, delete")
  # lazy = "dynamic" means the items won't be fetched from the db until we tell it to, faster
  # cascade = "all, delete" means that if we delete a store, all its items will be deleted too. this means no item will not have a store attached to it, which is good. delete-orphan is also an option, look this up https://docs.sqlalchemy.org/en/20/orm/cascades.html#delete-orphan
  tags = db.relationship("TagModel", back_populates = "store", lazy = "dynamic")