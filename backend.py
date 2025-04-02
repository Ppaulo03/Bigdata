from fastapi import FastAPI, HTTPException, Query
import pymongo
import uvicorn

app = FastAPI()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["accidents"]
collection = db["US_Accidents_March23"]

sort_accidents = {'$sort': { 'accidentCount': -1 }}
sort_accidents_acc = {'$sort': { 'accidentCount': 1 }}

@app.get("/")
def read_root():
    return {"Hello": "World"}


def aggregation(pipeline):
    result = list(collection.aggregate(pipeline))
    if not result:
        raise HTTPException(status_code=404, detail="No data found")
    return result


@app.get("/top_10_days")
def get_top_10_days():
    pipeline = [{
            '$project': {
                'date': { '$dateToString': { 'format': '%Y-%m-%d', 'date': '$Data_Hora_Inicio' } }
            }
        },
        {
            # Group by the date and count the accidents
            '$group': {
                '_id': '$date',
                'accidentCount': { '$sum': 1 }
            }
        },sort_accidents,
        {
            '$limit': 10
        }]
    
    return aggregation(pipeline)


@app.get("/least_10_days")
def get_least_10_days():
    pipeline = [{
            '$project': {
                'date': { '$dateToString': { 'format': '%Y-%m-%d', 'date': '$Data_Hora_Inicio' } }
            }
        },
        {
            # Group by the date and count the accidents
            '$group': {
                '_id': '$date',
                'accidentCount': { '$sum': 1 }
            }
        },sort_accidents_acc,
        {
            '$limit': 10
        }]
    
    return aggregation(pipeline)


@app.get("/accidents_by_state")
def get_accidents_by_state():
    pipeline = [{
        '$group': {
            '_id': '$Estado',
            'accidentCount': { '$sum': 1 }
        }
    },sort_accidents]
    
    return aggregation(pipeline)


@app.get("/accidents_by_city")
def get_accidents_by_city(state: str = Query(None)):
    if state:
        pipeline = [{
            '$match': { 'Estado': state }
        }]
    else:
        pipeline = []
    
    pipeline += [{
        '$group': {
            '_id': '$Cidade',
            'accidentCount': { '$sum': 1 }
        }
    },sort_accidents]
    
    return aggregation(pipeline)

@app.get("/accidents_by_weather")
def get_accidents_by_weather(state: str = Query(None)):
    if state:
        pipeline = [{
            '$match': { 'Estado': state }
        }]
    else:
        pipeline = []
    
    pipeline += [{
        '$group': {
            '_id': '$Condição_Tempo',
            'accidentCount': { '$sum': 1 }
        }
    },sort_accidents]
    
    return aggregation(pipeline)


@app.get("/list_weather_conditions")
def get_list_weather_conditions():
    pipeline = [{
        '$group': {
            '_id': '$Weather_Condition',
            'accidentCount': { '$sum': 1 }
        }
    },sort_accidents]
    
    agg = aggregation(pipeline)
    conditions = [str(item['_id']) for item in agg ]
    return conditions

if __name__ == '__main__':
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)