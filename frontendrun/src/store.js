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
        authorization: 'bearer ',
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
        'content-type': 'application/json',
        authorization: 'bearer ',
      },
    },
    goals: [],
    stats: undefined,
    current_week: undefined,
    token: undefined,
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
    getGoal (state) {
      return (id) => state.goals.find(v => v._id === id)
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
    getToken (state) {
      return state.token
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
    updateGoals (state, goal) {
      let i = state.goals.find(v => v._id === goal._id)
      if (i !== undefined) {
        state.goals[i] = goal
      } else {
        state.goals.push(goal)
      }
    },
    setStats (state, stats) {
      state.stats = stats
    },
    setWeek (state, activities) {
      state.current_week = activities
    },
    setToken (state, token) {
      state.token = token
      state.get_opts.headers.authorization += token
      state.post_opts.headers.authorization += token
    },
  },
})

export default store
