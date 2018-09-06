<template>
  <div class="goal">
    <div class="goal__info">
      <span v-if="goal.name">
        <h3>{{ goal.name }}</h3>
      </span>
      <span>{{ goal.target }}</span>
      <span>{{ goal.end_date }}</span>
    </div>
    <div v-if="goal.progress" class="goal__progress">
      <span>{{ goal.progress.current_distance | formatNumber }}</span>
      <span>{{ goal.progress.percent_complete | formatNumber(0) }}%</span>
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
  filters: {
    formatNumber (num, decimals=2) {
      return num.toFixed(decimals)
    },
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
  }
}
</script>

<style>
.goal {
  display: flex;
}
.goal__info {
  padding: 10px;
}
</style>
