<template>
  <div class="app__body">
    <!--lOADing :loading='loading'></Loading-->
    <div v-if="getUserId">
      <CurrentWeek @loaded='currentWeekLoaded()'></CurrentWeek>
      <GoalsList @loaded='goalsLoaded()'></GoalsList>
    </div>
    <div v-if="showStravaAuth" class="content__item">
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
import Loading from './Loading.vue'

export default {
  name: 'home-cmp',
  data () {
    return {
      showStravaAuth: false,
      loading: true,
      userId: undefined,
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
      } else {
        this.showStravaAuth = true
        this.loading = false
      }
    },
    getAuthUser () {
      let opts = this.GET
      fetch(`${this.api}/athlete`, opts)
        .then(response => {
          if (response.status === 200) {
            return response.json()
          } 
          throw new Error('Response not ok')
        })
        .then(response => {
          this.setAthlete(response.data.athlete)
          this.userId = response.data.athlete.id
          this.loading = false
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
    Loading,
  },
}
</script>
