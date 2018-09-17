<template>
  <footer class="app__footer">
    <div class="footer__left">
      <span class="footer__left_text">
        &copy;2018 Andrew Piper
      </span>
      <span class="footer__left_logo">
        <a href="https://github.com/arpiper/running-pipes" target="_blank" noopener>
        <img class="footer__left_logo_github" :src="githubLogo">
          Github.com/arpiper
        </a>
      </span>
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
      githubLogo: require('@/assets/GitHub-Mark-64px.png'),
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
  font-size: 12px;
}
.footer__left {
  display: flex;
  align-items: center;
  flex-direction: column;
  height: 75%;
}
.footer__left_text {
  margin: 0;
}
.footer__left_logo {
  height: 14px;
}
.footer__left_logo_github {
  height: 100%;
}
.footer__right {
  display: flex;
  align-items: center;
  height: 75%;
}
.footer__right_logo_strava {
  height: 100%;
}
</style>
