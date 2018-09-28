import Vue from 'vue'
import VueRouter from 'vue-router'
import Auth from './components/Auth.vue'
import Home from './components/Home.vue'
import GoalsList from './components/GoalsList.vue'

Vue.use(VueRouter)
const routes = [
  {
    name: 'home',
    path: '/', 
    component: Home, 
    alias: '/home'
  },
  {
    name: 'auth',
    path: '/auth', 
    component: Auth,
  },
  {
    name: 'goals',
    path: '/goals',
    component: GoalsList,
  },
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
