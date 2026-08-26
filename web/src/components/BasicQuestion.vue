<template>
  <section class="question-panel" aria-labelledby="basic-question-title">
    <p class="question-progress">
      基本質問
    </p>

    <h1 id="basic-question-title" class="question-title">
      基本質問
    </h1>

    <div
      v-for="question in visibleQuestions"
      :key="question.id"
      class="question-block"
    >
      <h2 class="question-block__title">
        {{ question.text }}
      </h2>

      <div
        v-if="question.type === 'qs'"
        class="option-list"
        role="group"
        :aria-label="question.text"
      >
        <button
          v-for="option in question.options"
          :key="option.id"
          class="option-button"
          :class="{ 'option-button--selected': getSelectedOptionIds(question.id).includes(option.id) }"
          type="button"
          role="checkbox"
          :aria-checked="getSelectedOptionIds(question.id).includes(option.id)"
          @click="selectOption(question.id, option.id)"
        >
          {{ option.label }}
        </button>
      </div>

      <textarea
        v-else-if="question.type === 'text'"
        class="text-answer"
        :value="getTextAnswer(question.id)"
        @input="updateTextAnswer(question.id, ($event.target as HTMLTextAreaElement).value)"
      ></textarea>
    </div>

    <button
      class="next-button"
      type="button"
      :disabled="!canGoNext || isSubmitting"
      @click="goToNextPhase"
    >
      次へ
    </button>

    <p v-if="submitError" class="submit-error" role="alert">
      回答の送信に失敗しました。時間をおいてもう一度お試しください。
    </p>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { getBasicQuestions, postAnswers, type Answer } from '../api/client'
import type { Question, QuestionOption } from './types/type'
import {
  getSelectedOptionIds as getSelectedOptionIdsFromAnswers,
  getTextAnswer as getTextAnswerFromAnswers,
  toggleOptionAnswer,
  upsertAnswer,
} from './basicAnswerState'

const FIRST_QUESTION_ID = 1
const OTHER_OPTION_ID = 'other'
const OTHER_REASON_QUESTION_ID = 2
const emit = defineEmits<{
  next: []
}>()

const questions = ref<Question[]>([])
const answers = ref<Answer[]>([])
const isSubmitting = ref(false)
const submitError = ref('')

const getSelectedOptionIds = (questionId: Question['id']) => {
  return getSelectedOptionIdsFromAnswers(answers.value, questionId)
}

const firstQuestionSelectedOptionIds = computed(() => getSelectedOptionIds(FIRST_QUESTION_ID))
const shouldAskOtherReason = computed(() => firstQuestionSelectedOptionIds.value.includes(OTHER_OPTION_ID))
const visibleQuestions = computed(() => {
  return questions.value.filter((question) => {
    if (question.id === OTHER_REASON_QUESTION_ID) return shouldAskOtherReason.value

    return question.id !== OTHER_REASON_QUESTION_ID
  })
})
const canGoNext = computed(() => {
  return visibleQuestions.value
    .filter((question) => question.type === 'qs')
    .every((question) => getSelectedOptionIds(question.id).length > 0)
})

const getTextAnswer = (questionId: Question['id']) => {
  return getTextAnswerFromAnswers(answers.value, questionId)
}

const selectOption = (questionId: Question['id'], optionId: QuestionOption['id']) => {
  submitError.value = ''
  answers.value = toggleOptionAnswer(answers.value, questionId, optionId)
}

const updateTextAnswer = (questionId: Question['id'], value: string) => {
  submitError.value = ''
  answers.value = upsertAnswer(answers.value, questionId, value)
}

const goToNextPhase = async () => {
  if (!canGoNext.value || isSubmitting.value) return

  isSubmitting.value = true
  submitError.value = ''

  try {
    await postAnswers(answers.value)
    emit('next')
  } catch {
    submitError.value = 'failed'
  } finally {
    isSubmitting.value = false
  }
}

onMounted(async () => {
  questions.value = await getBasicQuestions()
})
</script>

<style scoped>
.question-panel {
  width: min(100%, 640px);
  padding: 32px;
  border: 1px solid #d9dee7;
  border-radius: 8px;
  background: #ffffff;
}

.question-progress {
  margin: 0 0 12px;
  color: #667085;
  font-size: 0.875rem;
  font-weight: 700;
}

.question-title {
  margin: 0 0 24px;
  font-size: clamp(1.5rem, 1.2rem + 1vw, 2rem);
  line-height: 1.35;
}

.question-block {
  display: grid;
  gap: 12px;
}

.question-block + .question-block {
  margin-top: 28px;
}

.question-block__title {
  margin: 0;
  font-size: 1rem;
  line-height: 1.5;
}

.option-list {
  display: grid;
  gap: 12px;
}

.option-button {
  width: 100%;
  min-height: 56px;
  padding: 14px 16px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: #ffffff;
  color: #1f2933;
  font: inherit;
  text-align: left;
  cursor: pointer;
}

.option-button:hover,
.option-button:focus-visible {
  border-color: #2563eb;
  outline: none;
}

.option-button--selected {
  border-color: #2563eb;
  background: #eff6ff;
  color: #174ea6;
  font-weight: 700;
}

.next-button {
  width: 100%;
  min-height: 48px;
  margin-top: 24px;
  border: 0;
  border-radius: 8px;
  background: #1f2937;
  color: #ffffff;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
}

.next-button:disabled {
  background: #cbd5e1;
  color: #667085;
  cursor: not-allowed;
}

.submit-error {
  margin: 12px 0 0;
  color: #b42318;
  font-size: 0.875rem;
  line-height: 1.5;
}

.text-answer {
  width: 100%;
  min-height: 160px;
  padding: 14px 16px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  color: #1f2933;
  font: inherit;
  resize: vertical;
}

.text-answer:focus-visible {
  border-color: #2563eb;
  outline: none;
}

@media (max-width: 520px) {
  .question-panel {
    padding: 24px;
  }
}
</style>
