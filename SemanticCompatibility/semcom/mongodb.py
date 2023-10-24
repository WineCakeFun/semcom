import pymongo

def save_incompatibilities_to_mongodb(incompatibilities):
    # Підключення до бази даних
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["mydb"]
    collection = db["incompatibilities"]

    # Додавання несумісностей в базу даних
    for incompatibility in incompatibilities:
        collection.insert_one({
            "data_type": incompatibility[0],
            "element_name": incompatibility[1]
        })
def retrieve_incompatibilities_from_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["mydb"]
    collection = db["incompatibilities"]
    incompatibilities = list(collection.find({}, {"_id": 0}))  # Retrieve all records excluding _id
    return incompatibilities