from marshmallow import Schema, fields

# Using 'plain' schemas for avoiding recursion/nesting

class PlainItemSchema(Schema):
  id = fields.Int(dump_only = True)
  name = fields.Str(required = True)
  price = fields.Float(required = True)

class PlainStoreSchema(Schema):
  id = fields.Int(dump_only = True)
  name = fields.Str(required = True)

class PlainTagSchema(Schema):
  id = fields.Int(dump_only = True)
  name = fields.Str()

class ItemUpdateSchema(Schema):
  name = fields.Str()
  price = fields.Float()
  store_id = fields.Int()

class ItemSchema(PlainItemSchema):
  store_id = fields.Int(required = True, load_only = True)
  store = fields.Nested(PlainStoreSchema(), dump_only = True)
  tags = fields.List(fields.Nested(PlainTagSchema()), dump_only = True)

class StoreSchema(PlainStoreSchema):
  items = fields.List(fields.Nested(ItemSchema), dump_only = True) # Changed to ItemSchema from PlainItemSchema so I can get the tags in the items when I get a store. Expected a recursion error but I didn't get one... should test other scenarios
  tags = fields.List(fields.Nested(PlainTagSchema), dump_only = True)

class TagSchema(PlainTagSchema):
  store_id = fields.Int(load_only = True)
  store = fields.Nested(PlainStoreSchema(), dump_only = True)
  items = fields.List(fields.Nested(PlainItemSchema()), dump_only = True)

class TagAndItemsSchema(Schema):
  message = fields.Str()
  item = fields.Nested(ItemSchema)
  tag = fields.Nested(TagSchema)

class UserSchema(Schema):
  id = fields.Int(dump_only = True)
  username = fields.Str(required = True)
  password = fields.Str(required = True, load_only = True)