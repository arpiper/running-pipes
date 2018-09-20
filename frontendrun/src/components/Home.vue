<template>
  <div class="app__body">
    <div v-if="loading">
      <div class="loading__bar_container">
        <span  class="loading__bar">
        </span>
      </div>
    </div>
    <div v-if="getUserId">
      
      <CurrentWeek @loaded='currentWeekLoaded()'></CurrentWeek>
      <GoalsList @loaded='goalsLoaded()'></GoalsList>
    </div>
    <div v-if="!getUserId" class="content__item">
      <p>no authorized user</p>
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
import GoalsList from './GoalsList.vue'
import CurrentWeek from './CurrentWeek.vue'

export default {
  name: 'home-cmp',
  data () {
    return {
      userId: undefined,
      loading: true,
      currentWeek: false,
      goals: false,
      connectStrava: require('@/assets/btn_strava_connectwith_orange.png'),
      oauthUrl: 'https://www.strava.com/oauth/authorize?',
      oauth: {
        client_id: '27099',
        response_type: 'code',
        redirect_uri: 'http://localhost:8080/auth',
        approval_prompt: 'force',
      },
    }
  },
  computed: {
    ...mapGetters([
      'getUserId',
      'getAthlete',
      'getToken',
      'api',
    ]),
    ...mapGetters({
      'GET': 'getGetOpts',
    }),
    mainComponents () {
      return this.currentWeek && this.goals
    },
    oauthURI () {
      let s = this.oauthUrl
      for (var key in this.oauth) {
        if (s.slice(-1) === '?') {
          s += `${key}=${this.oauth[key]}`
        } else {
          s += `&${key}=${this.oauth[key]}`
        }
      }
      return s
    },
  },
  watch: {
    mainComponents (value) {
      if (value) {
        this.loading = false
      }
    }
  },
  methods: {
    ...mapMutations([
      'setAthlete',
      'setToken',
    ]),
    checkToken () {
      let t = JSON.parse(localStorage.getItem('acc-tok-ath'))
      if (t) {
        this.setToken(t.accessToken)
        this.getAuthUser()
      }
    },
    getAuthUser () {
      let opts = this.GET
      fetch(`${this.api}/athlete`, opts)
        .then(response => {
          if (response.ok) {
            return response.json()
          }
          throw new Error('Response not ok')
        })
        .then(response => {
          if (response !== 401) {
            this.setAthlete(response.data.athlete)
            this.userId = response.data.athlete.id
          }
        })
        .catch(response => {
          console.error('error', response)
        })
    },
    currentWeekLoaded () {
      this.currentWeek = true
    },
    goalsLoaded () {
      this.goals = true
    },
  },
  created () {
    if (this.getToken === undefined) {
      this.checkToken()
    } else {
      this.getAuthUser()
    }
  },
  components: {
    GoalsList,
    CurrentWeek,
  },
}
</script>
