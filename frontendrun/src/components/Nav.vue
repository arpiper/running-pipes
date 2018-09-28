<template>
  <nav class="app__nav">
    <a href="/" class="link__nav">
      <span class="link__text">Home</span>
    </a>
    <a href="/goals" class="link__nav">
      <span class="link__text">Goals</span>
    </a>
  </nav>
</template>

<script>
export default {
  name: 'nav-cmp',
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
  width: 100%;
}
.link__nav {
  text-decoration: none;
  color: var(--color-main);
  font-weight: bold;
  display: inline-flex;
}
.link__text {
  padding: 10px 25px;;
  width: 100%;
}
.link__text:hover {
  background-color: var(--color-main-dark);
  opacity: 0.75;
}
</style>
