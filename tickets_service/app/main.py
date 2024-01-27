import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Annotated
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID
from model.ticket import Ticket, TicketStatus
import pika
from threading import Thread

app = FastAPI()



db: List[Ticket] = [
    Ticket(id=1,
           show_id=1,
           status=TicketStatus.CREATED),
    Ticket(id=2,
           show_id=1,
           status=TicketStatus.CREATED)
]


def callback(ch, method, properties, body):
    print("got message")
    try:
        show_id = int(body)
        print(f" [x] Received 'Create Show': {show_id}")
        for i in range(len(db), len(db) + 20):
            db.append(Ticket(
                id=i,
                show_id=show_id,
                status=TicketStatus.CREATED
            ))
    except ValueError:
        print('Value Error')
    channel.basic_ack(delivery_tag=method.delivery_tag)

# RabbitMQ
url = "amqps://hhouuwcj:whH-ZWJiQ1qCWcOdoX4PFxFhtooS_sIj@cow.rmq2.cloudamqp.com/hhouuwcj"
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
queue_name = "shows"
channel.queue_declare(queue=queue_name, durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

@app.get("/healthCheck", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}

def get_shows():
    channel.start_consuming()
    return {'message': 'done'}

@app.get("/ticketList")
async def fetch_tickets():
    return db


@app.get("/get_ticket_by_show")
async def get_tickets_by_show(show_id: int):
    res = []
    for show in db:
        if show.id == show_id:
            res.append(show)
    return res
    raise HTTPException(
        status_code=404,
        detail=f'show with {show_id} does not exist'
    )


if __name__ == "__main__":
    th = Thread(target=get_shows)
    th.start()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))


