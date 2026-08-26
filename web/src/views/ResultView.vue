<template>
  <section class="result-view" aria-labelledby="result-title">
    <p class="result-view__eyebrow">
      最終結果
    </p>

    <h1 id="result-title" class="result-view__title">
      回答ありがとうございました
    </h1>
  </section>
</template>

<script setup lang="ts">
</script>

<style scoped>
.result-view {
  width: min(100%, 640px);
  padding: 32px;
  border: 1px solid #d9dee7;
  border-radius: 8px;
  background: #ffffff;
  color: #1f2933;
}

.result-view__eyebrow {
  margin: 0 0 12px;
  color: #667085;
  font-size: 0.875rem;
  font-weight: 700;
}

.result-view__title {
  margin: 0;
  font-size: clamp(1.5rem, 1.2rem + 1vw, 2rem);
  line-height: 1.35;
}

@media (max-width: 520px) {
  .result-view {
    padding: 24px;
  }
}
</style>
