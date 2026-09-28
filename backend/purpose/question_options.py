BASIC_QUESTION_OPTIONS = {
    1: [
        {"id": "strong", "label": "強くなりたかったから"},
        {"id": "cool", "label": "動きがカッコよかったから"},
        {"id": "protect_myself", "label": "自分の身を守りたいと思ったから"},
        {"id": "protect_other", "label": "大切な人を守りたいと思ったから"},
        {"id": "introduce_other", "label": "人に誘われて"},
        {"id": "interested_budo", "label": "武道に興味があったから"},
        {"id": "fittness", "label": "運動・フィットネス感覚"},
        {"id": "other", "label": "その他"},
    ],
    3: [
        {"id": "growth", "label": "成長を感じられるから"},
        {"id": "fun", "label": "稽古が楽しいから"},
        {"id": "health", "label": "健康・体力づくりになるから"},
        {"id": "community", "label": "仲間がいるから"},
        {"id": "goal", "label": "目標や大会があるから"},
        {"id": "habit", "label": "習慣になっているから"},
    ],
}

CHOICE_QUESTION_OPTIONS = {
    101: [
        {"id": "yes", "label": "はい"},
        {"id": "no", "label": "いいえ"},
    ],
    102: [
        {"id": "competition", "label": "試合で力を試したい"},
        {"id": "training", "label": "稽古を深めたい"},
    ],
}

QUESTION_OPTIONS = BASIC_QUESTION_OPTIONS | CHOICE_QUESTION_OPTIONS
