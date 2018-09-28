<template>
  <header class="app__header">
    <div class="header__logo">
      <img class="header__logo_img" :src="logo">
    </div>
    <div class="header__text">
      <h1 class="header__name">{{ name | upper }}</h1>
      <h3 class="header__tagline">{{ tagline }}</h3>
    </div>
  </header>
</template>

<script>

export default {
  name: 'header-cmp',
  data () {
    return {
      name: 'Set Your Goals',
      tagline: 'Climb Past Your Plateaus',
      logo: require('@/assets/logo_gray_green.svg'),
    }
  },
}
</script>
