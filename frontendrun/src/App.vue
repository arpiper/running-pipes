<template>
  <div id="app">
    <AddGoal userid="2"></AddGoal>
  </div>
</template>

<script>
import AddGoal from './components/AddGoal.vue'

export default {
  name: 'app',
  components: {
    AddGoal,
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
