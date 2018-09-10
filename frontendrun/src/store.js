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
      mode: 'cors',
      headers: {
        'content-type': 'application/json'
      },
    },
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
    getGetOpts (state) {
      return state.get_opts
    },
    getPostOpts (state) {
      return state.post_opts
    },
  },
  mutations: {
    setAthlete (state, athlete) {
      state.athlete = athlete
      state.userId = athlete.id
    }
  },
})

export default store
