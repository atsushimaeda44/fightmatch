from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_post_answers_accepts_answer_array():
    response = client.post(
        "/api/purpose/answers",
        json=[
            {"question_id": 1, "answer": ["strong", "other"]},
            {"question_id": 2, "answer": "友人に誘われたから"},
        ],
    )

    assert response.status_code == 200
    assert response.json() == {"received_count": 2}


def test_get_basic_questions_still_returns_questions():
    response = client.get("/api/purpose/questions/basic")

    assert response.status_code == 200
    assert response.json()[0]["id"] == 1
