<template>
  <div id="app" class="app__container">
    <header class="app__header">
      Header
    </header>
    <router-view></router-view>
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
    Footer,
  },
  computed: {
    ...mapGetters([
      'getUserId',
      'getAthlete',
      'getToken',
      'api',
    ]),
  },
  watch: {
  },
  methods: {
    ...mapMutations([
      'setAthlete',
      'setToken',
    ]),
    toggleAdd () {
      this.addGoal = !this.addGoal
    },
  },
  created () {
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
