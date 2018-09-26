<template>
  <transition name="fade">
  <div v-if="loading">
    <div class="loading__container">
      <span v-if="type == 'bar'" class="loading__bar">
      </span>
      <span v-else-if="type == 'spin'" class="loading__spin">
      </span>
    </div>
  </div>
  </transition>
</template>

<script>

export default {
  name: 'loading-cmp',
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
    type: {
      type: String,
      default: 'bar',
    },
  },
}
</script>

<style>
.fade-leave-active {
  transition: opacity 0.75s;
}
.fade-leave-to {
  opacity: 0;
}
</style>
