import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
const store = new Vuex.Store({
  state: {
    userId: undefined,
    api_uri: 'http://localhost:5000/api',
    athlete: undefined,
    get_opts: {
      headers: {
        'content-type': 'application/json',
      },
      mode: 'cors',
      methods: 'GET',
    },
    post_opts: {
      method: 'POST',
      //credentials: 'include',
      body: '',
      mode: 'cors',
      headers: {
        'content-type': 'application/json'
      },
    },
    goals: undefined,
    stats: undefined,
    current_week: undefined,
  },
  getters: {
    api (state) {
      return state.api_uri
    },
    getUserId (state) {
      return state.userId
    },
    getAthlete (state) {
      return state.athlete
    },
    getGoals (state) {
      return state.goals
    },
    getStats (state) {
      return state.stats
    },
    getGetOpts (state) {
      return state.get_opts
    },
    getPostOpts (state) {
      return state.post_opts
    },
    getWeek (state) {
      return state.current_week
    },
  },
  mutations: {
    setAthlete (state, athlete) {
      state.athlete = athlete
      state.userId = athlete.id
    },
    setGoals (state, goals) {
      state.goals = goals
    },
    setStats (state, stats) {
      state.stats = stats
    },
    setWeek (state, activities) {
      state.current_week = activities
    },
  },
})

export default store
