import { describe, expect, it } from 'vitest'

import {
    getSelectedOptionIds,
    getTextAnswer,
    toggleOptionAnswer,
    upsertAnswer,
} from '../basicAnswerState'
import type { Answer } from '../../api/client'

describe('basicAnswerState', () => {
    it('adds and removes qs option answers', () => {
        let answers: Answer[] = []

        answers = toggleOptionAnswer(answers, 1, 'strong')
        expect(getSelectedOptionIds(answers, 1)).toEqual(['strong'])

        answers = toggleOptionAnswer(answers, 1, 'cool')
        expect(getSelectedOptionIds(answers, 1)).toEqual(['strong', 'cool'])

        answers = toggleOptionAnswer(answers, 1, 'strong')
        expect(getSelectedOptionIds(answers, 1)).toEqual(['cool'])
    })

    it('updates text answers', () => {
        const answers = upsertAnswer([], 2, '友人に誘われたから')

        expect(getTextAnswer(answers, 2)).toBe('友人に誘われたから')
    })

    it('overwrites an existing answer for the same question', () => {
        const answers = upsertAnswer([{ question_id: 2, answer: 'before' }], 2, 'after')

        expect(answers).toEqual([{ question_id: 2, answer: 'after' }])
    })
})
