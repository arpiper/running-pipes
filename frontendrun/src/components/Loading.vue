<template>
  <div v-if="loading">
    <div class="loading__bar_container">
      <span  class="loading__bar">
      </span>
    </div>
  </div>
</template>

<script>

export default {
  name: 'loading-cmp',
  props: {
    loading: Boolean,
  },
}
</script>

<style>

</style>
