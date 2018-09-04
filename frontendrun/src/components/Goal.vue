<template>
  <div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'goal',
  props: {
    id: [String, Number]
  },
  data () {
    return {
    }
  },
  computed: {
    ...mapGetters({
      api: 'api',
      userId: 'getUserId',
    }),
    fetchBody () {
      return {
        _id: this.id,
        userId: this.userId,
      }
    },
  },
  methods: {
    getGoalData () {
      let options = {
        //body: JSON.stringify(this.fetchBody)
        method: 'GET',
        //withCredentials: true,
        mode: 'cors',
        headers: {
          'content-type': 'application/json',
        },
      }
      fetch(`${this.api}/goals/${this.id}`, options)
        .then(res => res.json())
        .then(res => {
          console.log('fetch one goal', res)
        })
    },
  },
  created () {
    this.getGoalData()
  }
}
</script>

<style>
</style>
