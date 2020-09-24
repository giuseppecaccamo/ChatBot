from flask import Flask, request, Response
from botbuilder.schema import Activity
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, ConversationState, UserState, MemoryStorage
from botdialog import BotDialog
import asyncio

app = Flask(__name__)
loop = asyncio.get_event_loop()

botadaptersetting = BotFrameworkAdapterSettings("4955118d-7d23-4531-bc1b-fa2389b81b7e","0hZ9uwLv~_I-46Wmr4kYWk3-6xWDtGIgkt")
botadapter = BotFrameworkAdapter(botadaptersetting)

memstore = MemoryStorage()
constate = ConversationState(memstore)

botdialog = BotDialog(constate)

@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["content-type"]:
        jsonmessage = request.json
    else:
        return Response(status=415)

    activity =Activity().deserialize(jsonmessage)
    auth_header = (request.headers['Authorization'] if 'Authorization' in request.headers else '')

    async def call_func(turn_context):
        await botdialog.on_turn(turn_context)

    task = loop.create_task(
        botadapter.process_activity( activity,auth_header,call_func )
    )
    loop.run_until_complete(task)


if __name__ == '__main__':
    app.run('localhost',3978)
