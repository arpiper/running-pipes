<template>
  <div id="app" class="app__container">
    <header class="app__header">
      Header
    </header>
    <div class="app__body">
      <div v-if="loading" class="loading__bar_container">
        <span  class="loading__bar">
        </span>
      </div>
      <CurrentWeek @loaded='currentWeekLoaded()'></CurrentWeek>
      <GoalsList @loaded='goalsLoaded()'></GoalsList>
    </div>
    <div class="app__sidebar">
      <AthleteInfo></AthleteInfo>
      <div class="goals__create">
        <ButtonCmp :toggle='addGoal' @click.native="toggleAdd()">
        </ButtonCmp>
        <div v-if="addGoal">
          <AddGoal></AddGoal>
        </div>
      </div>
    </div>
    <Footer></Footer> 
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import AthleteInfo from './components/AthleteInfo.vue'
import AddGoal from './components/AddGoal.vue'
import GoalsList from './components/GoalsList.vue'
import ButtonCmp from './components/ButtonCmp.vue'
import CurrentWeek from './components/CurrentWeek.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'app',
  data () {
    return {
      userId: undefined,
      addGoal: false,
      loading: true,
      currentWeek: false,
      goals: false,
    }
  },
  components: {
    AthleteInfo,
    AddGoal,
    GoalsList,
    ButtonCmp,
    CurrentWeek,
    Footer,
  },
  computed: {
    ...mapGetters([
      'getUserId',
      'getAthlete',
      'api',
    ]),
    mainComponents () {
      return this.currentWeek && this.goals
    }
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
    currentWeekLoaded () {
      this.currentWeek = true
    },
    goalsLoaded () {
      this.goals = true
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
  width: 100%;
  display: grid;
  margin: 0 auto;
  grid-template-rows: 100px 1fr 50px;
  grid-template-columns: 10% 60% 20% 10%;
  grid-template-areas: 
    'header header header header'
    'left body sidebar right'
    'footer footer footer footer'
}
.app__header {
  grid-area: header;
  /* temp for visual*/
  background-color: white;
}
.app__body {
  grid-area: body;
  padding: 10px 0;
}
.app__sidebar {
  grid-area: sidebar;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  /* temp for visual
  border-left: 1px solid var(--color-gray-medium);
  */
}
.app__footer {
  grid-area: footer;
  background-color: white;
  /* temp for visual
  border-top: 1px solid var(--color-gray-medium);
  */
}
.goals__create {
  width: 80%;
  margin: 0 auto;
}
</style>
