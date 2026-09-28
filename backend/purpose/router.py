from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_db
from .models import Answer as AnswerModel
from .models import Question as QuestionModel
from .models import User
from .question_options import QUESTION_OPTIONS
from .schemas import Answer, Question

router = APIRouter(prefix="/api/purpose", tags=["purpose"])
DEV_USER_ID = 1


def _serialize_question(question: QuestionModel) -> Question:
    return Question(
        id=question.id,
        text=question.text,
        type=question.answer_type,
        options=QUESTION_OPTIONS.get(question.id),
    )


def _get_questions_by_group(db: Session, question_group: str) -> list[Question]:
    questions = db.scalars(
        select(QuestionModel)
        .where(QuestionModel.question_group == question_group)
        .order_by(QuestionModel.id)
    ).all()
    return [_serialize_question(question) for question in questions]


@router.get(
    "/questions/basic", response_model=list[Question], response_model_exclude_none=True
)
def get_basic_questions(db: Session = Depends(get_db)):
    return _get_questions_by_group(db, "basic")


@router.get(
    "/questions/choice", response_model=list[Question], response_model_exclude_none=True
)
def get_choice_questions(db: Session = Depends(get_db)):
    return _get_questions_by_group(db, "choice")


@router.post("/answers")
def post_answers(answers: list[Answer], db: Session = Depends(get_db)):
    question_ids = {answer.question_id for answer in answers}
    if question_ids:
        existing_question_ids = set(
            db.scalars(
                select(QuestionModel.id).where(QuestionModel.id.in_(question_ids))
            ).all()
        )
        missing_question_ids = sorted(question_ids - existing_question_ids)
        if missing_question_ids:
            raise HTTPException(
                status_code=404,
                detail={
                    "message": "Question not found",
                    "question_ids": missing_question_ids,
                },
            )

    if db.get(User, DEV_USER_ID) is None:
        db.add(User(id=DEV_USER_ID, name="Development User"))
        db.flush()

    db.add_all(
        [
            AnswerModel(
                user_id=DEV_USER_ID,
                question_id=answer.question_id,
                answer=answer.answer,
            )
            for answer in answers
        ]
    )
    db.commit()
    return {"received_count": len(answers)}
