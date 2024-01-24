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
import json
import aio_pika
import asyncio

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

async def start_consumer_async():
    url = "amqps://hhouuwcj:whH-ZWJiQ1qCWcOdoX4PFxFhtooS_sIj@cow.rmq2.cloudamqp.com/hhouuwcj"

    async with aio_pika.connect_robust(url) as connection:
        channel = await connection.channel()

        queue_name = "shows"
        await channel.declare_queue(queue_name, durable=True)
        await channel.set_qos(prefetch_count=1)

        await channel.consume(
            callback,
            queue_name=queue_name
        )

        while True:
            await asyncio.sleep(1)

@app.get("/healthCheck", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.get("/ticketList")
async def fetch_tickets():
    return db


# @app.get("/get_show_by_id")
# async def get_train_by_id(show_id: int):
#     for show in db:
#         if show.id == show_id:
#             return show
#     raise HTTPException(
#         status_code=404,
#         detail=f'train with {show_id} does not exist'
#     )
#
#
#
# @app.delete("/delele_show/{show_id}")
# async def delete_show(show_id: int):
#     for show in db:
#         if show.id == show_id:
#             db.remove(show)
#             return
#     raise HTTPException(
#         status_code=404,
#         detail=f'train with {show_id} does not exist'
#     )
#

async def main():
    # Запуск консьюмера и FastAPI параллельно
    await asyncio.gather(
        start_consumer_async(),

    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))