<template>
  <div id="app" class="app__container">
    <Header></Header>
    <main class="app__body">
      <router-view></router-view>
    </main>
    <div class="app__sidebar" v-if="getUserId">
      <AthleteInfo></AthleteInfo>
      <div class="goals__create">
        <ButtonCmp :toggle='addGoal' @click.native="toggleAdd()">
        </ButtonCmp>
        <div v-if="addGoal">
          <AddGoal @goalAdded='toggleAdd()'></AddGoal>
        </div>
      </div>
    </div>
    <Footer></Footer> 
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import AddGoal from './components/AddGoal.vue'
import AthleteInfo from './components/AthleteInfo.vue'
import ButtonCmp from './components/ButtonCmp.vue'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'app',
  data () {
    return {
      addGoal: false,
    }
  },
  components: {
    AddGoal,
    AthleteInfo,
    ButtonCmp,
    Header,
    Footer,
  },
  computed: {
    ...mapGetters([
      'getUserId',
      'getAthlete',
      'getToken',
      'api',
    ]),
    ...mapGetters({
      GET: 'getGetOpts',
    }),
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
    toggleAdd () {
      this.addGoal = !this.addGoal
    },
  },
  created () {
    if (this.getToken === undefined) {
      this.checkToken()
    } else {
      this.getAuthUser()
    }
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
  position: relative;
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
