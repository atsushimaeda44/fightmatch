import { request } from './base'

export type BasicQuestion = {
    id: number
    text: string
    type: string
    options?: {
        id: string
        label: string
    }[]
}

export type Answer = {
    question_id: number
    answer: string | string[]
}

export function getBasicQuestions() {
    return request<BasicQuestion[]>('/api/purpose/questions/basic')
}

export function postAnswers(answers: Answer[]) {
    return request<{ received_count: number }>('/api/purpose/answers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(answers),
    })
}
