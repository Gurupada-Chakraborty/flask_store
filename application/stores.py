import logging
import datetime as datetime
import mongoengine

# connecting to mongodb
mongoengine.connect(
    db='db',
    username='db_mongo_user',
    password='mongo_db_2894',
    host='mongodb+srv://db_mongo_user:mongo_db_2894@cluster0.lw2qew9.mongodb.net/?retryWrites=true&w=majority',
    port=0
)
logger = logging.getLogger(__name__)

# schema definition
class Stores(mongoengine.DynamicDocument):
    store_id = mongoengine.StringField(required=True)
    sku = mongoengine.StringField(required=True, unique=True)
    product_name = mongoengine.StringField(required=True)
    price = mongoengine.IntField(required=True)
    date = mongoengine.DateTimeField(null=True)

    # setting up schema object
    def set_store_details(self, record):
        store_schema = Stores()
        store_schema.store_id = str(record['id'])
        store_schema.sku = record['sku']
        store_schema.product_name = record['name']
        store_schema.price = record['price']
        try:
            store_schema.date = record['date']
        except:
            store_schema.date = datetime.datetime.now()

        return store_schema

    # validating and adding records to db
    @staticmethod
    def add_record(store_schema):
        flag = 0
        try :
            store_schema.validate()
            store_schema.save()
            print("Record saved successfully!")
            flag = 1
            return flag
        except Exception as e:
            logger.error(str(e))
            return flag
