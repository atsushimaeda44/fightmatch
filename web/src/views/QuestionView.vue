<template>
  <main class="question-view">
    <BasicQuestion v-if="currentPhase === 'basic'" @next="goToChoiceQuestion" />
    <ChoiceQuestion v-else-if="currentPhase === 'choice'" @next="goToResult" />
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import BasicQuestion from '../components/BasicQuestion.vue'
import ChoiceQuestion from '../components/ChoiceQuestion.vue'

const router = useRouter()

type QuestionPhase = 'basic' | 'choice' | 'result'

const currentPhase = ref<QuestionPhase>('basic')

const goToChoiceQuestion = () => {
  currentPhase.value = 'choice'
}

const goToResult = () => {
  router.push('/result')
}
</script>

<style scoped>
.question-view {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 32px 20px;
  background: #f6f8fb;
  color: #1f2933;
}
</style>
