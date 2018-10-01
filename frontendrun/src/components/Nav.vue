<template>
  <nav class="app__nav">
    <router-link to="home" class="link__nav" :class="{link__nav_style_active: loc == 'home'}" >
      <span class="link__text">Home</span>
    </router-link>
    <router-link to="goals" class="link__nav" :class="{link__nav_style_active: loc == 'goals'}" >
      <span class="link__text">Goals</span>
    </router-link>
  </nav>
</template>

<script>
export default {
  name: 'nav-cmp',
  props: {
    loc: {
      type: String,
      default: 'home'
    },
  },
  data () {
    return {
    }
  },
}
</script>

<style>
.app__nav {
  grid-area: nav;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}
.link__nav {
  text-decoration: none;
  color: var(--color-main);
  font-weight: bold;
  display: inline-flex;
  height: 100%;
  align-items: center;
}
.link__text {
  padding: 0 25px;
  width: 100%;
  height: 100%;
}
.link__nav_style_active {
  text-decoration: underline;
}
.link__text:hover {
  background-color: var(--color-main-dark-02);
}
</style>
