import os
import peewee as pw 
import datetime
from playhouse.postgres_ext import PostgresqlDatabase

db = PostgresqlDatabase(os.getenv('DATABASE'))

class BaseModel(pw.Model):
    created_at = pw.DateTimeField(default=datetime.datetime.now)
    updated_at = pw.DateTimeField(default=datetime.datetime.now)

    # new save
    def save(self, *args, **kwargs):
        self.errors = []
        self.validate()

        if len(self.errors) == 0:
            self.updated_at = datetime.datetime.now()
            # inherits save() from Model
            return super(BaseModel, self).save(*args, **kwargs)
        else:
            return 0
    
    def validate(self):
        print("validate() is not implemented for this class")

    class Meta:
        database = db
        legacy_table_names = False

class Store(BaseModel):
    name = pw.CharField(unique=True)

    def validate(self):
        duplicate_store = Store.get_or_none(Store.name == self.name)
        if duplicate_store:
            self.errors.append("A store with this name already exists!")

class Warehouse(BaseModel):
    store = pw.ForeignKeyField(Store, backref='warehouses')
    location = pw.TextField()

class Product(BaseModel):
    name = pw.CharField(index=True)
    description = pw.TextField()
    warehouse = pw.ForeignKeyField(Warehouse, backref='products')
    colour = pw.CharField(null=True)