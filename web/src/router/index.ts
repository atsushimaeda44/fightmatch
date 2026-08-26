import { createRouter, createWebHistory } from 'vue-router'
import QuestionView from '../views/QuestionView.vue'
import ResultView from '../views/ResultView.vue'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomeView
    },
    {
      path: '/question',
      name: 'question',
      component: QuestionView,
    },
    {
      path: '/result',
      name: 'result',
      component: ResultView,
    }
  ],
})

export default router
