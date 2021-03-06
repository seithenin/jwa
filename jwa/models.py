from google.appengine.ext import db
from google.appengine.api import images

class BaseModel(object):
    @property
    def id(self):
        return self.key().id()

class Gallery(db.Model, BaseModel):
    title = db.StringProperty(required=True)
    description = db.TextProperty()
    icon_picture = db.ReferenceProperty()

    @property
    def icon(self):
        if self.icon_picture:
            return self.icon_picture
        else:
            return self.pictures.get()

class Picture(db.Model, BaseModel):
    gallery = db.ReferenceProperty(
        Gallery, required=True, collection_name='pictures'
    )
    image = db.BlobProperty()
    title = db.StringProperty(required=True)
    # put author here for simplicity, maybe can move to it's own table
    author = db.StringProperty()
    # tag = db.CategoryProperty() add tag table if needed
    width = db.IntegerProperty()
    height = db.IntegerProperty()
    media = db.StringProperty() # or change to dropdown ?
    _price_by_cent = db.IntegerProperty()
    original_available = db.BooleanProperty(default=False)
    description = db.TextProperty()
    create_date = db.DateTimeProperty(auto_now_add=True)
    update_date = db.DateTimeProperty(auto_now=True)

    def __init__(self, price=None, *args, **kwargs):
        if price != None:
            kwargs['_price_by_cent'] = int(price * 100)
        super(Picture, self).__init__(*args, **kwargs)

    @property
    def price(self):
        if self._price_by_cent == None:
            return None
        return self._price_by_cent / 100.0

    @price.setter
    def price(self, value):
        self._price_by_cent = int(value * 100)

    @property
    def gallery_id(self):
        return self.gallery.id

    @property
    def gallery_icon(self):
        return self.gallery.icon_picture.id == self.id

class UploadFile(db.Model, BaseModel):
    blob = db.BlobProperty()
    filename = db.StringProperty()
    type = db.StringProperty()

class Content(db.Model, BaseModel):
    name = db.StringProperty(required=True)
    content = db.TextProperty(default='')

    @classmethod
    def get_by_name(cls, name, create=False):
        obj = cls.all().filter('name =', name).get()
        if create and not obj:
            obj = cls(name=name)
            obj.put()
        return obj


