from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload
from sqlalchemy import select, text

from models import *
from schemas import *

import os


BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, 'db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
    
DB_PATH = os.path.join(DB_DIR, 'fastapi.db')    

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")
# engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}", echo=True) # echo=True - все sql в консоль
# engine = create_async_engine("sqlite+aiosqlite:///example//fastapi//db//fastapi.db")
# engine = create_async_engine("sqlite+aiosqlite:///db//fastapi.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)
# expire_on_commit=False отключает истечение (сброс) атрибутов объектов после commit() в SQLAlchemy сессии.
# если True - после комита обращение к любому полю создаст новый запрос, если False -возмет из памяти



class  DataRepository:
    @classmethod
    async def create_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.create_all)
    
    @classmethod            
    async def delete_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.drop_all)     

    @classmethod
    async def add_test_data(cls):
        async with new_session() as session:
            users = [
                UserOrm(name='user1', age=20),
                UserOrm(name='user2', age=30, phone='123456789'),
                UserOrm(name='user3', age=41, phone='11'),
                UserOrm(name='user4', age=42, phone='22'),
                UserOrm(name='user5', age=43, phone='33'),
                UserOrm(name='user6', age=44),
                UserOrm(name='user7', age=45)
            ]
            
                        
            session.add_all(users)            
            
            # flush() - используется для синхронизации изменений с базой данных без завершения транзакции
            # проверяет, что операции (вставка, обновление) не вызывают ошибок
            # Если последующие действия в транзакции зависят от предыдущих изменений, 
            # flush() делает эти изменения видимыми в рамках текущей сессии
            await session.flush() 
            await session.commit()




class UserRepository:
    
    @classmethod
    async def add_user(cls, user: UserAdd) -> int:
        async with new_session() as session:
            data = user.model_dump() # -> dict
            user = UserOrm(**data)
            session.add(user) # не производит операций с БД только с памятью поэтому синхронно
            await session.flush()
            await session.commit()
            return user.id
            
    @classmethod        
    async def get_users(cls, limit, offset,) -> list[UserOrm]:
        async with new_session() as session:
            
            # query = select(UserOrm)
            query = select(UserOrm).limit(limit).offset(offset)
            
            # query = user_filter.filter(query).limit(limit).offset(offset)
            # query = user_filter.sort(query)
            # query = text(f"SELECT * FROM users WHERE id={id}")
            
            res = await session.execute(query)
            users = res.scalars().all()
            return users
        
    @classmethod
    async def get_user(cls, id) -> UserOrm:
        async with new_session() as session:
            query = select(UserOrm).filter(UserOrm.id==id)
            # query = text(f"SELECT * FROM users WHERE id={id}")
            res = await session.execute(query) 
            user = res.scalars().first()
            return user
        

class QuizRepository:

    @classmethod
    async def add_quiz(cls, quiz: QuizAdd):
        async with new_session() as session:
            data = QuizOrm(**quiz.model_dump())
            session.add(data)
            await session.flush()
            await session.commit()
            return data.id
    
    @classmethod
    async def get_quizes(cls, limit, offset):
        async with new_session() as session:
            qeury = select(QuizOrm).limit(limit).offset(offset)
            res = await session.execute(qeury)
            quizes = res.scalars().all()
            return quizes
        
    classmethod
    async def get_quiz(cls, id):
        async with new_session() as session:
            qeury = select(QuizOrm).where(QuizOrm.id == id)
            res = await session.execute(qeury)
            quiz = res
            return quiz
        
    @classmethod
    async def get_quiz_question(cls, id):
        async with new_session() as session:
            qeury = select(QuizOrm).options(selectinload(QuizOrm.questions)).where(QuizOrm. id == id)
            res = await session.execute(qeury)
            quiz_question = res.scalars().first()
            return quiz_question
        
    async def link_question_to_quiz (cls, quiz_id, question_id):
        async with new_session() as session:
            quiz = await session.get(QuizOrm, quiz_id)
            if not quiz:
                return
            
            qeury = select(QuestionOrm).where(QuestionOrm.id.in_(question_id))
            res = await session.execute(qeury)
            questions = res.scalars().all()

            quiz.question.extend(questions)
            await session.commit()


class QuestionRepositore:

    @classmethod
    async def add_question(cls, question: QuestionAdd):
        async with new_session() as session:
            data = QuestionOrm(**question.model_dump())
            session.add(data)
            await session.flush()
            await session.commit()
            return data.id
        
    @classmethod 
    async def get_questions(cls, limit, offset):
        async with new_session() as session:
            qeury = select(QuestionOrm).limit(limit).offset(offset)
            res = await session.execute(qeury)
            questions = res.scalars().all()
            return questions
        
    @classmethod
    async def get_question(cls, id):
        async with new_session() as session:
            qeury = select(QuestionOrm).where(QuestionOrm.id == id)
            res = await session.execute(qeury)
            question = res.scalars().first()
            return question

