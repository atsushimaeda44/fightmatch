import type { Answer } from '../api/client'
import type { Question, QuestionOption } from './types/type'

const findAnswer = (answers: Answer[], questionId: Question['id']) => {
    return answers.find((answer) => answer.question_id === questionId)
}

export const getSelectedOptionIds = (answers: Answer[], questionId: Question['id']) => {
    const answer = findAnswer(answers, questionId)?.answer

    return Array.isArray(answer) ? answer : []
}

export const getTextAnswer = (answers: Answer[], questionId: Question['id']) => {
    const answer = findAnswer(answers, questionId)?.answer

    return typeof answer === 'string' ? answer : ''
}

export const upsertAnswer = (
    answers: Answer[],
    questionId: Question['id'],
    answer: Answer['answer'],
) => {
    const nextAnswer = { question_id: questionId, answer }
    const answerIndex = answers.findIndex((currentAnswer) => currentAnswer.question_id === questionId)

    if (answerIndex === -1) return [...answers, nextAnswer]

    return answers.map((currentAnswer, index) => {
        return index === answerIndex ? nextAnswer : currentAnswer
    })
}

export const toggleOptionAnswer = (
    answers: Answer[],
    questionId: Question['id'],
    optionId: QuestionOption['id'],
) => {
    const selectedOptionIds = getSelectedOptionIds(answers, questionId)
    const nextAnswer = selectedOptionIds.includes(optionId)
        ? selectedOptionIds.filter((selectedOptionId) => selectedOptionId !== optionId)
        : [...selectedOptionIds, optionId]

    return upsertAnswer(answers, questionId, nextAnswer)
}
