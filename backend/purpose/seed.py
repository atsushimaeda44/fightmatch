from sqlalchemy.orm import Session

from .database import Base, engine
from .models import Question, User


BASIC_QUESTIONS = [
    {
        "id": 1,
        "text": "あなたが1番最初に剣護身術に惹かれたきっかけはなんですか？",
        "question_group": "basic",
        "answer_type": "qs",
    },
    {
        "id": 2,
        "text": "その他を選んだ理由はなんですか？",
        "question_group": "basic",
        "answer_type": "text",
    },
    {
        "id": 3,
        "text": "今継続してる理由はなんですか？",
        "question_group": "basic",
        "answer_type": "qs",
    },
]

CHOICE_QUESTIONS = [
    {
        "id": 101,
        "text": "あなたは試合に出てみたいですか？",
        "question_group": "choice",
        "answer_type": "binary",
    },
    {
        "id": 102,
        "text": "今のあなたに近い目的はどちらですか？",
        "question_group": "choice",
        "answer_type": "qs",
    },
]

DEV_USER = {"id": 1, "name": "Development User"}


def seed_development_data(db: Session) -> None:
    if db.get(User, DEV_USER["id"]) is None:
        db.add(User(**DEV_USER))

    for question_data in [*BASIC_QUESTIONS, *CHOICE_QUESTIONS]:
        question = db.get(Question, question_data["id"])
        if question is None:
            db.add(Question(**question_data))
        else:
            for key, value in question_data.items():
                setattr(question, key, value)

    db.commit()


def main() -> None:
    Base.metadata.create_all(bind=engine)
    with Session(engine) as db:
        seed_development_data(db)


if __name__ == "__main__":
    main()
