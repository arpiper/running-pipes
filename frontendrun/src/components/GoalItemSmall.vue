<template>
  <div class="goal__item_size_small">
    <h4 class="goal__header">{{ goal.name }}</h4>
    <span>{{ goal.percent | formatNum }}</span>
    <span>{{ goal.perWeek | formatNum }}</span>
  </div>
</template>

<script>
export default {
  name: 'goal-item-small',
  props: {
    goal: [Array, Object],
  },
  filters: {
    formatNum (val, decimals=2) {
      // reusing this a similar alot. consider a mixin'
      return val.toFixed(decimals)
    }
  },
}
</script>

<style>
</style>
