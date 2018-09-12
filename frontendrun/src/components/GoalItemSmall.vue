<template>
  <div class="goal__item_size_small">
    <h4 class="goal__header">{{ goal.name }}</h4>
    <span>{{ goal.percent | number(0) }}%</span>
    <span>{{ goal.perWeek | number }}</span>
  </div>
</template>

<script>
export default {
  name: 'goal-item-small',
  props: {
    goal: [Array, Object],
  },
}
</script>

<style>
</style>
