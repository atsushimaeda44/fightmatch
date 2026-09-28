import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from purpose.database import Base, get_db
from purpose.models import Answer as AnswerModel
from purpose.seed import seed_development_data


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as db:
        seed_development_data(db)
        yield db

    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session: Session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_get_basic_questions_still_returns_questions(client: TestClient):
    response = client.get("/api/purpose/questions/basic")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "text": "あなたが1番最初に剣護身術に惹かれたきっかけはなんですか？",
            "type": "qs",
            "options": [
                {"id": "strong", "label": "強くなりたかったから"},
                {"id": "cool", "label": "動きがカッコよかったから"},
                {"id": "protect_myself", "label": "自分の身を守りたいと思ったから"},
                {"id": "protect_other", "label": "大切な人を守りたいと思ったから"},
                {"id": "introduce_other", "label": "人に誘われて"},
                {"id": "interested_budo", "label": "武道に興味があったから"},
                {"id": "fittness", "label": "運動・フィットネス感覚"},
                {"id": "other", "label": "その他"},
            ],
        },
        {
            "id": 2,
            "text": "その他を選んだ理由はなんですか？",
            "type": "text",
        },
        {
            "id": 3,
            "text": "今継続してる理由はなんですか？",
            "type": "qs",
            "options": [
                {"id": "growth", "label": "成長を感じられるから"},
                {"id": "fun", "label": "稽古が楽しいから"},
                {"id": "health", "label": "健康・体力づくりになるから"},
                {"id": "community", "label": "仲間がいるから"},
                {"id": "goal", "label": "目標や大会があるから"},
                {"id": "habit", "label": "習慣になっているから"},
            ],
        },
    ]


def test_get_choice_questions_returns_questions(client: TestClient):
    response = client.get("/api/purpose/questions/choice")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 101,
            "text": "あなたは試合に出てみたいですか？",
            "type": "binary",
            "options": [
                {"id": "yes", "label": "はい"},
                {"id": "no", "label": "いいえ"},
            ],
        },
        {
            "id": 102,
            "text": "今のあなたに近い目的はどちらですか？",
            "type": "qs",
            "options": [
                {"id": "competition", "label": "試合で力を試したい"},
                {"id": "training", "label": "稽古を深めたい"},
            ],
        },
    ]


def test_post_answers_accepts_answer_array_and_saves_to_db(
    client: TestClient, db_session: Session
):
    response = client.post(
        "/api/purpose/answers",
        json=[
            {"question_id": 1, "answer": ["strong", "other"]},
            {"question_id": 2, "answer": "友人に誘われたから"},
        ],
    )

    assert response.status_code == 200
    assert response.json() == {"received_count": 2}

    saved_answers = db_session.scalars(
        select(AnswerModel).order_by(AnswerModel.id)
    ).all()
    assert len(saved_answers) == 2
    assert saved_answers[0].question_id == 1
    assert saved_answers[0].answer == ["strong", "other"]
    assert saved_answers[1].question_id == 2
    assert saved_answers[1].answer == "友人に誘われたから"


def test_post_answers_accepts_string_answer(client: TestClient, db_session: Session):
    response = client.post(
        "/api/purpose/answers",
        json=[{"question_id": 2, "answer": "自由回答"}],
    )

    assert response.status_code == 200
    saved_answer = db_session.scalar(select(AnswerModel))
    assert saved_answer.answer == "自由回答"


def test_post_answers_rejects_unknown_question_id(
    client: TestClient, db_session: Session
):
    response = client.post(
        "/api/purpose/answers",
        json=[{"question_id": 9999, "answer": "unknown"}],
    )

    assert response.status_code == 404
    assert response.json()["detail"] == {
        "message": "Question not found",
        "question_ids": [9999],
    }
    assert db_session.scalars(select(AnswerModel)).all() == []
