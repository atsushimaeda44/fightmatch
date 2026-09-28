import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from main import app
from purpose.database import Base, get_db
from purpose.models import Answer as AnswerModel
from purpose.seed import seed_development_data


@pytest.mark.skipif(
    os.getenv("RUN_POSTGRES_TESTS") != "1" or not os.getenv("TEST_DATABASE_URL"),
    reason="Set RUN_POSTGRES_TESTS=1 and TEST_DATABASE_URL to run PostgreSQL tests.",
)
def test_post_answers_saves_jsonb_values_to_postgresql():
    database_url = os.environ["TEST_DATABASE_URL"]
    engine = create_engine(database_url)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as db:
        seed_development_data(db)

        def override_get_db():
            yield db

        app.dependency_overrides[get_db] = override_get_db
        response = TestClient(app).post(
            "/api/purpose/answers",
            json=[
                {"question_id": 1, "answer": ["strong", "other"]},
                {"question_id": 2, "answer": "友人に誘われたから"},
            ],
        )
        app.dependency_overrides.clear()

        assert response.status_code == 200
        assert response.json() == {"received_count": 2}

        saved_answers = db.scalars(select(AnswerModel).order_by(AnswerModel.id)).all()
        assert saved_answers[0].answer == ["strong", "other"]
        assert saved_answers[1].answer == "友人に誘われたから"
