import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
const store = new Vuex.Store({
  state: {
    userId: 0,
    api_uri: 'http://localhost:5000/api',
    athlete: undefined,
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
    }
  },
  mutations: {
    setAthlete (state, athlete) {
      state.athlete = athlete
      state.userId = athlete.id
    }
  },
})

export default store
