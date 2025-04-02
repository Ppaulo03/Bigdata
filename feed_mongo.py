from etl import etl
from tqdm import tqdm
import pandas as pd
import kagglehub
import pymongo
import os

 
def add_collection(db, collection_name, path, batch_size=5000):
    db[file_name].drop()
    collection = db[collection_name]
    total_rows = sum(1 for _ in open(path))
    
    with tqdm(total=total_rows, desc=f"Inserting {file_name}", unit="row") as pbar:
        for chunk in pd.read_csv(path, chunksize=batch_size):
            data = etl(chunk)
            collection.insert_many(data)
            pbar.update(len(chunk))

    print(f"{collection_name} inserted into MongoDB")


# Download latest version
path = kagglehub.dataset_download("sobhanmoosavi/us-accidents")

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["accidents"]
for file in os.listdir(path):
    if file.endswith(".csv"):
        file_path = os.path.join(path, file)
        file_name = file.split(".")[0]
        add_collection(db, "Acidentes - Tratados", file_path)


