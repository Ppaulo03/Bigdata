import pandas as pd
import pymongo
import kagglehub
import os
from tqdm import tqdm
 
def add_collection(db, file_name, path, batch_size=1000):
    db[file_name].drop()
    collection = db[file_name]
    total_rows = sum(1 for _ in open(path))
    with tqdm(total=total_rows, desc=f"Inserting {file_name}", unit="row") as pbar:
        for chunk in pd.read_csv(path, chunksize=batch_size):
            data = chunk.to_dict(orient='records')
            collection.insert_many(data)
            pbar.update(len(chunk))

    print(f"{file_name} inserted into MongoDB")


# Download latest version
path = kagglehub.dataset_download("sobhanmoosavi/us-accidents")

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["accidents"]
for file in os.listdir(path):
    if file.endswith(".csv"):
        file_path = os.path.join(path, file)
        file_name = file.split(".")[0]
        add_collection(db, file_name, file_path)


