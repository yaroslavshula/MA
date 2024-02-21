import os
import uvicorn
from fastapi import FastAPI,  HTTPException, status, Form
from typing import List
from model.show import Show
import pika
from keycloak import KeycloakOpenID

app = FastAPI()

db: List[Show] = [
    Show(id=1,
         type='Musical',
         theater_id=2),
    Show(id=2,
         type='Drama',
         theater_id=1)
]

# Данные для подключения к Keycloak
KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "shulindin"
KEYCLOAK_REALM = "myrealm"
KEYCLOAK_CLIENT_SECRET = "T678RfL6Jxtk5zmNQygPAn7ahcTnPzTr"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                  client_id=KEYCLOAK_CLIENT_ID,
                                  realm_name=KEYCLOAK_REALM,
                                  client_secret_key=KEYCLOAK_CLIENT_SECRET)

user_token = ""


###########
#Prometheus
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

@app.post("/get-token")
async def get_token(username: str = Form(...), password: str = Form(...)):
    try:
        # Получение токена
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        global user_token
        user_token = token
        return token
    except Exception as e:
        print(e)  # Логирование для диагностики
        raise HTTPException(status_code=400, detail="Не удалось получить токен")

def check_user_roles():
    global user_token
    token = user_token
    try:
        userinfo = keycloak_openid.userinfo(token["access_token"])
        token_info = keycloak_openid.introspect(token["access_token"])
        if "testRole" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")

@app.get("/healthCheck", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.get("/showList")
async def fetch_shows():
    return db

@app.get("/get_show_by_id")
async def get_show_by_id(show_id: int):
    for show in db:
        if show.id == show_id:
            return show
    raise HTTPException(
        status_code=404,
        detail=f'train with {show_id} does not exist'
    )

@app.post("/add_show")
async def add_show(show: Show):
    db.append(show)
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

@app.delete("/delete_show")
async def delete_show(show_id: int):
    for show in db:
        if show.id == show_id:
            db.remove(show)
            return "deleted"
    raise HTTPException(
        status_code=404,
        detail=f'train with {show_id} does not exist'
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
