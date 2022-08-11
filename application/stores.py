from asyncio.log import logger
import mongoengine


class Stores(mongoengine.DynamicDocument):
    store_id = mongoengine.StringField(required=True)
    sku = mongoengine.StringField(required=True, unique=True)
    product_name = mongoengine.StringField(required=True)
    price = mongoengine.IntField(required=True)
    date = mongoengine.DateField(required=True)

    def set_store_details(self, record):
        store_schema = Stores()
        store_schema.store_id = record['store_id']
        store_schema.sku = record['sku']
        store_schema.product_name = record['product_name']
        store_schema.price = record['price']
        store_schema.date = record['date']

        return store_schema

    @staticmethod
    def add_record(store_schema):
        check = Stores.objects.get(sku=store_schema['sku'])
        if check is None:
            store_schema.validate()
            store_schema.save()
        else:
            logger.error("Record already exists!")
