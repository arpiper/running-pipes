<template>
  <div>
    <div class="block__athlete" v-if="athlete">
      <div class="block__info">
        <span>  
          <img :src="athlete.profile_medium" />
        </span>
        <span>{{ athlete.firstname }}</span>
        <span>{{ athlete.lastname }}</span>
      </div>
    </div>
    <div v-else>
      <div class="block__athlete_auth">
        <span class="block_athlete_auth_button">
          <a :href="oauthURI">
            <img :src="connectStrava" alt="Connect with Strava">
          </a>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'

export default {
  name: 'athlete-info',
  data () {
    return {
      stats: undefined,
      connectStrava: require('@/assets/btn_strava_connectwith_orange.png'),
      oauthUrl: 'https://www.strava.com/oauth/authorize?',
      oauth: {
        client_id: '27099',
        response_type: 'code',
        redirect_uri: 'http://localhost',
        approval_prompt: 'force',
      },
    }
  },
  computed: {
    ...mapGetters({
      athlete: 'getAthlete',
      getStoreStats: 'getStats',
      userId: 'getUserId',
      GET: 'getGetOpts',
      api: 'api',
    }),
    oauthURI () {
      let s = this.oauthUrl
      for (var key of this.oauth) {
        if (s.slice(-1) === '?') {
          s += `${key}=${this.oauth[key]}`
        } else {
          s += `&${key}=${this.oauth[key]}`
        {
      }
      console.log(s)
      return s
    },
  },
  watch: {
    userId (id) {
      if (id !== undefined) {
        this.getStats()
      }
    }
  },
  methods: {
    ...mapMutations([
      'setStats',
    ]),
    getStats () {
      if (this.getStoreStats) {
        this.stats = this.getStoreStats
      } else {
        fetch(`${this.api}/stats/${this.userId}`, this.GET)
          .then(res => res.json())
          .then(res => {
            console.log('stats', res)
            this.setStats(res.data.stats)
          })
      }
    },
  },
  mounted () {
  }
}
</script>
