<template>
  <footer class="app__footer">
    <div class="footer__left">
      <p class="footer__left_text">
        &copy;2018 Andrew Piper
      </p>
    </div>
    <div class="footer__right">
      <img class="footer__right_logo_strava" :src="pwrdByStrava" alt="Powered By Strava">
    </div>
  </footer>
</template>

<script>
export default {
  name: 'footer-cmp',
  data () {
    return {
      pwrdByStrava: require('@/assets/api_logo_pwrdBy_strava_horiz_light.png'),
    }
  },
}
</script>

<style scoped>
.app__footer {
  display: flex;
  align-items: center;
  justify-content: space-around;
  height: 50px;
}
.footer__left {
  display: flex;
  align-items: center;
}
.footer__right {
  display: flex;
  align-items: center;
  height: 75%;
}
.footer__left_text {
  margin: 0;
}
.footer__right_logo_strava {
  height: 100%;
}
</style>
