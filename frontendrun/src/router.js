import Vue from 'vue'
import VueRouter from 'vue-router'
import Auth from './components/Auth.vue'
import Home from './components/Home.vue'

Vue.use(VueRouter)
const routes = [
  {path: '/', component: Home},
  {path: '/auth', component: Auth}
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
