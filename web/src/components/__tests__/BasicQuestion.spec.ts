import { flushPromises, mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import BasicQuestion from '../BasicQuestion.vue'
import { getBasicQuestions, postAnswers } from '../../api/client'

vi.mock('../../api/client', () => ({
    getBasicQuestions: vi.fn(),
    postAnswers: vi.fn(),
}))

const questions = [
    {
        id: 1,
        text: 'きっかけはなんですか？',
        type: 'qs',
        options: [
            { id: 'strong', label: '強くなりたかったから' },
            { id: 'other', label: 'その他' },
        ],
    },
    {
        id: 2,
        text: 'その他を選んだ理由はなんですか？',
        type: 'text',
    },
    {
        id: 3,
        text: '継続している理由はなんですか？',
        type: 'qs',
        options: [{ id: 'fun', label: '楽しいから' }],
    },
]

describe('BasicQuestion', () => {
    beforeEach(() => {
        vi.mocked(getBasicQuestions).mockResolvedValue(questions)
        vi.mocked(postAnswers).mockResolvedValue({ received_count: 2 })
    })

    it('emits next after answers are posted successfully', async () => {
        const wrapper = mount(BasicQuestion)
        await flushPromises()

        await wrapper.findAll('button.option-button')[0]?.trigger('click')
        await wrapper.findAll('button.option-button')[1]?.trigger('click')
        await wrapper.find('textarea').setValue('友人に誘われたから')
        await wrapper.findAll('button.option-button')[2]?.trigger('click')
        await wrapper.find('button.next-button').trigger('click')
        await flushPromises()

        expect(postAnswers).toHaveBeenCalledWith([
            { question_id: 1, answer: ['strong', 'other'] },
            { question_id: 2, answer: '友人に誘われたから' },
            { question_id: 3, answer: ['fun'] },
        ])
        expect(wrapper.emitted('next')).toHaveLength(1)
    })

    it('does not emit next when posting answers fails', async () => {
        vi.mocked(postAnswers).mockRejectedValue(new Error('failed'))

        const wrapper = mount(BasicQuestion)
        await flushPromises()

        await wrapper.findAll('button.option-button')[0]?.trigger('click')
        await wrapper.findAll('button.option-button')[1]?.trigger('click')
        await wrapper.find('textarea').setValue('友人に誘われたから')
        await wrapper.findAll('button.option-button')[2]?.trigger('click')
        await wrapper.find('button.next-button').trigger('click')
        await flushPromises()

        expect(wrapper.emitted('next')).toBeUndefined()
        expect(wrapper.find('[role="alert"]').text()).toContain('回答の送信に失敗しました')
    })
})
