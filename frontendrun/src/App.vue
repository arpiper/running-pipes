<template>
  <div id="app">
    <AthleteInfo></AthleteInfo>
    <Goals></Goals>
    <AddGoal :userId="userId"></AddGoal>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import AddGoal from './components/AddGoal.vue'
import AthleteInfo from './components/AthleteInfo.vue'
import Goals from './components/Goals.vue'

export default {
  name: 'app',
  data () {
    return {
      userId: undefined,
    }
  },
  components: {
    AddGoal,
    AthleteInfo,
    Goals,
  },
  computed: {
    ...mapGetters([
      'getUserId',
      'getAthlete',
      'api',
    ]),
  },
  methods: {
    ...mapMutations([
      'setAthlete',
    ]),
    getAuthUser () {
      let opts = {
        method: 'GET',
        mode: 'cors',
        headers: {
          'content-type': 'application/json',
        },
      }
      fetch(`${this.api}/athlete`, opts)
        .then(response => {
          return response.json()
        })
        .then(response => {
          this.setAthlete(response.data.athlete)
          this.userId = response.data.athlete.id
        })
    },
  },
  created () {
    this.getAuthUser()
  },
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
