<template>
  <nav class="app__nav">
    <router-link :to="{name: 'home'}" class="link__nav" :class="{link__nav_style_active: loc == 'home'}" >
      <span class="link__text">Home</span>
    </router-link>
    <router-link :to="{name : 'goals'}" class="link__nav" :class="{link__nav_style_active: loc == 'goals'}" >
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
