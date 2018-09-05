<template>
  <div class="goal">
    <div>
      <span v-if="goal.name">{{ goal.name }}</span>
      <span>{{ goal.target }}</span>
      <span>{{ goal.end_date }}</span>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'goal',
  props: {
    id: [String, Number],
    goal: [Object, Array],
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
  },
  methods: {
    getGoalData () {
      let options = {
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
    //this.getGoalData()
  }
}
</script>

<style>
</style>
