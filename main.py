from fastapi import FastAPI, status, Header
from fastapi.exceptions import RequestValidationError
from langchain.chat_models import ChatOpenAI
from AI.Models.DBAIModel import DBAIModel
from AI.Models.DoctorAIModel import DoctorAIModel
from AI.Models.IFModel import IfModel
from AI.Models.SecretaryAIModel import SecretaryAIModel
from AI.Models.SecretaryIFModel import SecretaryIFModel
from AI.Models.SummarizerModel import SummarizerModel
from AI.Tools.DBTool import DBTool
from AI.Tools.DoctorTool import DoctorTool
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
doctorModel = DoctorAIModel(
    llm=llm,
)
doctorTool = DoctorTool(
    name="Medical Knowledge",
    description="useful for when you need to answer any medical questions",
    model=doctorModel
)
dbAIModel = DBAIModel(
    llm=llm,
)
dbTool = DBTool(
    name="People Database Table",
    description='useful for when you need to deal with people data from database',
    model=dbAIModel
)
summarizer = SummarizerModel(
    llm=llm,
)
secretary = SecretaryIFModel(
    llm=llm,
)


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
        "role": "patient",
        "content": "Hello there, I am Mutasim"
    }),
    ChatMessage.parse_obj({
        "role": "dr",
        "content": "Nice to meet you. How can I help you?"
    }),
    ChatMessage.parse_obj({
        "role": "patient",
        "content": "what is the sum of 2 + 2?"
    })
]


@app.get('/test')
async def test(message: str):
    response = secretary.handle('', message)
    print(response)
    return Responser.respond(200, 'successful', {'summary': '', 'response': response})


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
    new_summary = ''
    chats_to_answer = Body.chats[-1]
    if len(body.chats) == 3:
        chats_to_summarized = Body.chats[0:2]
        memory = summarizer.prompt_format(summary=body.summary, conversation=chats_to_summarized)
        new_summary = summarizer.handle(memory)

    # handling the request
    response = secretary.handle(new_summary, chats_to_answer.content)

    # returning response
    return Responser.respond(200, 'successful operation', {'summary': new_summary, 'response': response})
