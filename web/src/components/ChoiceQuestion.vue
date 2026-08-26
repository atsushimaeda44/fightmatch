<template>
  <section class="choice-question" aria-labelledby="choice-question-title">
    <h2 id="choice-question-title" class="choice-question__title">
      {{ questionText }}
    </h2>

    <div class="choice-question__options" role="group" :aria-label="questionText">
      <button
        v-for="option in options"
        :key="option.id"
        class="choice-question__option"
        :class="{ 'choice-question__option--selected': selectedOptionId === option.id }"
        type="button"
        :aria-pressed="selectedOptionId === option.id"
        @click="selectOption(option.id)"
      >
        {{ option.label }}
      </button>
    </div>

    <button
      class="choice-question__next"
      type="button"
      :disabled="!selectedOptionId"
      @click="goToNextPhase"
    >
      次へ
    </button>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'

type ChoiceOption = {
  id: string
  label: string
}

const questionText = 'あなたは試合に出てみたいですか？'
const options: ChoiceOption[] = [
  { id: 'yes', label: 'はい' },
  { id: 'no', label: 'いいえ' },
]
const emit = defineEmits<{
  next: []
}>()

const selectedOptionId = ref<ChoiceOption['id'] | null>(null)

const selectOption = (optionId: ChoiceOption['id']) => {
  selectedOptionId.value = optionId
}

const goToNextPhase = () => {
  if (!selectedOptionId.value) return

  emit('next')
}
</script>

<style scoped>
.choice-question {
  width: min(100%, 640px);
  padding: 32px;
  border: 1px solid #d9dee7;
  border-radius: 8px;
  background: #ffffff;
  color: #1f2933;
}

.choice-question__title {
  margin: 0 0 24px;
  font-size: clamp(1.5rem, 1.2rem + 1vw, 2rem);
  line-height: 1.35;
}

.choice-question__options {
  display: grid;
  gap: 12px;
}

.choice-question__option {
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

.choice-question__option:hover,
.choice-question__option:focus-visible {
  border-color: #2563eb;
  outline: none;
}

.choice-question__option--selected {
  border-color: #2563eb;
  background: #eff6ff;
  color: #174ea6;
  font-weight: 700;
}

.choice-question__next {
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

.choice-question__next:disabled {
  background: #cbd5e1;
  color: #667085;
  cursor: not-allowed;
}

@media (max-width: 520px) {
  .choice-question {
    padding: 24px;
  }
}
</style>
