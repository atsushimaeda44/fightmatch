from fastapi import APIRouter

from .schemas import Answer

router = APIRouter(prefix="/api/purpose", tags=["purpose"])


@router.get("/questions/basic")
def get_basic_questions():
    return [
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


@router.post("/answers")
def post_answers(answers: list[Answer]):
    return {"received_count": len(answers)}
