<template>
  <div v-if="loading">
    <div class="loading__container">
      <span v-if="type == 'bar'" class="loading__bar">
      </span>
      <span v-else-if="type == 'spin'" class="loading__spin">
      </span>
    </div>
  </div>
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
.loading__spin {
  display: none;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  background-color: rgba(0,0,0,0.25);
}
.loading__spin:after {
  content: "";
  border-radius: 50%;
  width: 40px;
  height: 40px;
  margin: auto;
  position: absolute;
  border: 5px solid var(--color-gray-light);
  border-top: 5px solid var(--color-main);
  animation: spin 1.5s infinite linear;
  top: calc(50% - 20px);
  left: calc(50% - 20px);
}
</style>
