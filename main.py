from fastapi import FastAPI, status, Header
from fastapi.exceptions import RequestValidationError
from langchain.chat_models import ChatOpenAI
from AI.Models.DoctorAIModel import DoctorAIModel
from AI.Models.IFModel import IfModel
from AI.Models.SecretaryAIModel import SecretaryAIModel
from AI.Models.SummarizerModel import SummarizerModel
from AI.Tools.SearchTool import SearchTool
from Interface.Models.chatMessageModel import ChatMessage
from Interface.Utilities.Authorizer import Authorizer
from Interface.Utilities.Exceptioner import Exceptioner
from Interface.Utilities.Responser import Responser
from Interface.Models.bodyModel import Body

app = FastAPI()
llm = ChatOpenAI(openai_api_key='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', temperature=0)

searchTool = SearchTool(
    name='Search',
    description='useful for when you need to answer questions about current events',
    sites=['www.cdc.gov', 'www.healthline.com']
)
summarizer = SummarizerModel(
    llm=llm,
)
doctor_ai = DoctorAIModel(
    llm=llm,
    tools=[]
)
ifAI = IfModel(
    llm=llm
)
# secretary = SecretaryAIModel(
#     llm=llm,
#     tools=[
#         SearchTool
#     ]
# )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return Responser.respond(status.HTTP_422_UNPROCESSABLE_ENTITY, "required field is missing",
                             "HTTP_422_UNPROCESSABLE_ENTITY")


@app.exception_handler(Exceptioner)
async def exception_handler(request, exc):
    return Responser.respond(exc.error_status, exc.message, exc.result)


fakeDB = [{'id': 1, 'name': 'ali'}, {'id': 2, 'name': 'waleed'}]
conversation = [
    ChatMessage.parse_obj({
        "role": "human",
        "content": "Hello there, I am Mutasim"
    }),
    ChatMessage.parse_obj({
        "role": "AI",
        "content": "Nice to meet you. How can I help you?"
    }),
    ChatMessage.parse_obj({
        "role": "human",
        "content": "what is the sum of 2 + 2?"
    })
]


@app.get('/test')
async def test():
    response = searchTool.run('suger')
    print(response)
    return Responser.respond(200, 'successful', response)


@app.post('/talkToDoctorAI')
async def talk_with_doctor_ai(body: Body, authorization: str = Header(None)):
    # validation
    if not Authorizer.is_authorized(authorization):
        raise Exceptioner(
            status.HTTP_401_UNAUTHORIZED,
            "unauthorized",
            "HTTP_401_UNAUTHORIZED",
        )
    if len(body.chats) > 3:
        raise Exceptioner(
            status.HTTP_406_NOT_ACCEPTABLE,
            "chats number should be less than 4",
            "HTTP_406_NOT_ACCEPTABLE",
        )

    # summarization
    memory = summarizer.prompt_format(summary=body.summary, conversation=Body.chats)
    response = summarizer.handle(memory)

    return Responser.respond(200, 'successful operation', 'AI: how can I help you?')
