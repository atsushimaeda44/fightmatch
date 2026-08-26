export type QuestionOption = {
    id: string
    label: string
}

export type Question = {
    id: number
    text: string
    type: string
    options?: QuestionOption[]
}

export type Answer = {
    question_id: number
    answer: string | string[]
}
