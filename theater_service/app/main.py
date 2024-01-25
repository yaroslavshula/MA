import os
import uvicorn
from fastapi import FastAPI,  HTTPException, status
from typing import List
from model.show import Show
import pika

app = FastAPI()

db: List[Show] = [
    Show(id=1,
         type='Musical',
         theater_id=2),
    Show(id=2,
         type='Drama',
         theater_id=1)
]

@app.get("/healthCheck", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.get("/showList")
async def fetch_shows():
    return db

@app.get("/get_show_by_id")
async def get_train_by_id(show_id: int):
    for show in db:
        if show.id == show_id:
            return show
    raise HTTPException(
        status_code=404,
        detail=f'train with {show_id} does not exist'
    )

@app.post("/add_show")
async def add_show(show: Show):
    db.append(Show)
    url = "amqps://hhouuwcj:whH-ZWJiQ1qCWcOdoX4PFxFhtooS_sIj@cow.rmq2.cloudamqp.com/hhouuwcj"
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)

    queue_name = "shows"
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=str(show.id),
                          properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    print(f" [x] Sent 'Create Show': {show.id}")
    connection.close()
    return {"id": show.id}

@app.delete("/delele_show/{show_id}")
async def delete_show(show_id: int):
    for show in db:
        if show.id == show_id:
            db.remove(show)
            return
    raise HTTPException(
        status_code=404,
        detail=f'train with {show_id} does not exist'
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
