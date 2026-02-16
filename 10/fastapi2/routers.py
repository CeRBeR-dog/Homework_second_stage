from fastapi import APIRouter, HTTPException, Depends, Query

from schemas import *
from database import UserRepository as ur
from database import QuizRepository as qr
from database import QuestionRepositore as qsr


# pip install fastapi_filter
from fastapi_filter import FilterDepends

default_router = APIRouter()

users_router = APIRouter(
    prefix="/users",
    tags = ["Пользователи"]
)

quizes_router = APIRouter(
    prefix="/quizes",
    tags = ["Квизы"]
)

questions_router = APIRouter(
    prefix="/questions",
    tags=["Вопросы"]
)



@default_router.get('/', tags=['API V1'])
async def index():    
    return {'data':'ok'}



# ответ в виде одиночного списка
@users_router.get('')
async def users_get(
            limit:int = Query(ge=1, lt=10, default=3), 
            offset:int = Query(ge=0, default=0),
            # user_filter: UserFilter = FilterDepends(UserFilter)
        ) -> dict[str, int | list[User]]: 
     
    # users =   await ur.get_users(limit, offset, user_filter)
    users =   await ur.get_users(limit, offset)
    
    # return users
    
    # с развернутым ответом 
    return {"data":users, "limit":limit, "offset":offset}


@users_router.get('/u2')
async def users_get2() -> dict[str, list[User] | str]: 
    users =   await ur.get_users()
    return {'status':'ok', 'data':users}


@users_router.get('/{id}')
async def user_get(id: int) -> User :  
    user =   await ur.get_user(id)
    if user:
        return user    
    raise HTTPException(status_code=404, detail="User not found")
    # или return {'err':"User not found, ..."} # но тогда get_user(id) -> User | dict[str,str]
    
    
@users_router.post('')
async def add_user(user:UserAdd = Depends()) -> UserId:
    id = await ur.add_user(user)
    return {'id':id}    


@quizes_router.get('')
async def quizes_get(
                limit: int = Query(ge=1, lt=25, default=4),
                offset: int = Query(ge=0, default=0)
                ) -> dict[str, int | list[Quiz]]:
    
    quizes = await qr.get_quizes(limit, offset)
    return quizes


@quizes_router.post('')
async def add_quiz(quiz:QuizAdd = Depends()) -> QuizId:
    id = await qr.add_quiz(quiz)
    return {'id':id}


@quizes_router.get('/{id}')
async def quiz_get(id: int) -> Quiz:
    quiz = await qr.get_quiz(id)
    if not quiz:
        raise HTTPException(404)
    return quiz


@quizes_router.get('/{id}/question')
async def quiz_with_question(id: int) -> Quiz_Questions:
    quiz = await qr.get_quiz_question(id)
    if not quiz:
        raise HTTPException(404)
    return quiz


@questions_router.post('/{id}/link')
async def link_question(id: int, data: QuizQuestionLink):
    await qr.link_question_to_quiz(id, data.question_id)
    return {'статус': 'связанно'}


@questions_router.get('')
async def questions_get(
                limit: int = Query(ge=1, lt=25, default=4),
                offset: int = Query(ge=0, default=0)
                ) -> dict[str, int | list[Question]]:
    
    questions = await qsr.get_questions(limit, offset)
    return questions


@questions_router.post('')
async def add_question(question:QuestionAdd = Depends()) -> QuestionId:
    id = await qsr.add_question(question)
    return {'id': id}


@questions_router.get('/{id}')
async def question_get(id: int) -> QuestionId:
    question = await qsr.get_question(id)
    if not question:
        raise HTTPException(404)
    return question
    




















































# пример развернутого ответа
#     {
            # "items": [...],
            # "total": 100,
            # "page": 1,
            # "size": 10,
            # "pages": 10
            # }

            # Или с ссылками:

            # {
            # "items": [...],
            # "total": 100,
            # "page": 1,
            # "size": 10,
            # "pages": 10,
            # "links": {
            # "next": "http://api.example.com/items?page=2",
            # "prev": null,
            # "first": "http://api.example.com/items?page=1",
            # "last": "http://api.example.com/items?page=10"
            # }
            # }