<template>
  <div >
    auth loading...
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import router from '../router.js'

export default {
  name: 'auth-cmp',
  data () {
    return {
      url: 'https://www.strava.com/oauth/token',
      opts: {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
        },
        mode: 'cors',
      }
    }
  },
  computed: {
    ...mapGetters({
      'api': 'api',
      'POST': 'getPostOpts',
    }),
  },
  methods: {
    ...mapMutations([
      'setToken',
    ]),
    getAccessToken () {
      let opts = this.POST
      opts.body = JSON.stringify({
        code: this.$route.query.code
      })
      // send code to api backend
      fetch(`${this.api}/auth`, opts)
        .then(response => {
          if (response.ok) {
            return response.json()
          }
          throw new Error(`Response not ok - status ${response.status}`)
        })
        .then(response => {
          console.log('second',response)
          // save the token in the store and localstorage
          localStorage.setItem('acc-tok-ath', JSON.stringify({
            accessToken: response.access_token
          }))
          this.setToken(response.access_token)
          // redirect to /home
          router.push('home')
        })
        .catch(error => {
          console.error('Error', error)
        })
    },
  },
  created () {
    console.log('roue',this.$route)
    this.getAccessToken()
  },
}
</script>
