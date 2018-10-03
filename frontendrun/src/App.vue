<template>
  <div id="app" class="app__container">
    <Header></Header>
    <Nav :loc="loc"></Nav>
    <main class="app__body">
      <transition name="fade">
      <router-view></router-view>
      </transition>
    </main>
    <div class="app__sidebar" v-if="getUserId">
      <AthleteInfo></AthleteInfo>
      <div class="goals__create">
        <ButtonCmp :toggle='addGoal' @click.native="toggleAdd()">
        </ButtonCmp>
        <div v-show="addGoal">
          <AddGoal @goalAdded='toggleAdd()' :show="addGoal"></AddGoal>
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
import Nav from './components/Nav.vue'

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
    Nav,
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
    loc () {
      return this.$route.name
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
  color: var(--color-secondary);
}
.roll-enter {
  height: 0;
}
.roll-enter-to {
  height: 200px;
}
.roll-leave-to { 
  height: 0;
}
.roll-enter-active {
  transition: height 3s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.fade-enter-to,
.fade-leave {
  opacity: 1;
}
.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s;
}
</style>
