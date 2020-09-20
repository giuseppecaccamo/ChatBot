from flask import Flask, request, Response
from botbuilder.schema import Activity
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, ConversationState, UserState, MemoryStorage
from botdialog import BotDialog
import asyncio

app = Flask(__name__)
loop = asyncio.get_event_loop()

botadaptersetting = BotFrameworkAdapterSettings("5d341f2c-08ea-4091-b171-95e88774361f","KW5KrJZ7mnxrjVDMV7Mu_-3.p8reSYNy~6")
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
