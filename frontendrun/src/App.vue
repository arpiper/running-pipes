<template>
  <div id="app" class="app__container">
    <div class="app__body">
      <Goals></Goals>
    </div>
    <div class="app__sidebar">
      <AthleteInfo></AthleteInfo>
      <div class="goals__create">
        <div class="button__addgoal">
          <span @click="toggleAdd()">add</span>
        </div>
        <div v-show="addGoal">
          <AddGoal></AddGoal>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import AthleteInfo from './components/AthleteInfo.vue'
import AddGoal from './components/AddGoal.vue'
import Goals from './components/Goals.vue'

export default {
  name: 'app',
  data () {
    return {
      userId: undefined,
      addGoal: false,
    }
  },
  components: {
    AthleteInfo,
    AddGoal,
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
    toggleAdd () {
      this.addGoal = !this.addGoal
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
}
.app__container {
  width: 80%;
  display: grid;
  margin: 0 auto;
  grid-template-rows: 100px 1fr 50px;
  grid-template-columns: 70% 30%;
  grid-template-areas: 
    'header header'
    'body sidebar'
    'footer footer'
}
.app__body {
  grid-area: 'body';
}
.app__sidebar {
  grid-area: 'sidebar';
}
</style>
