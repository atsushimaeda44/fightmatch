<template>
  <main>
    <p v-for="question in questions" :key="question.id">{{ question }}</p>
  </main>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getBasicQuestions, type BasicQuestion } from '../api/client'

const questions = ref<BasicQuestion[]>([])

onMounted(async () => {
  questions.value = await getBasicQuestions()
  console.log(questions.value)
})
</script>
