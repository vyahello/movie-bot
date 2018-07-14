from src.bot.message import Answer, BotAnswer, BotMessage
from src.bot.text import InputText, Text
from src.server import Server, SERVER, METHODS, POST, WELCOME_MESSAGE
from src.server.requests import Request, ServerRequest

_server: Server = SERVER


@_server.route('/', methods=METHODS)
def index():
    request: Request = ServerRequest()
    answer: Answer = BotAnswer(request)

    if request.method() == POST:
        text: Text = InputText(answer.message())

        if text.match():
            BotMessage(answer.chat_id(), text.get()).send()

    return WELCOME_MESSAGE
