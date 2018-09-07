<template>
  <div>
    <div class="goals">
      <GoalItem 
        v-for="goal of goals"
        :key="goal._id"
        :goal="goal">
      </GoalItem>
    </div>

  </div>
</template>

<script>
import GoalItem from './GoalItem.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'goals',
  data () {
    return {
      goals: [],
    }
  },
  computed: {
    ...mapGetters({
      api: 'api',
      userId: 'getUserId',
    }),
  },
  watch: {
    userId (id) {
      if (id !== undefined) {
        this.getGoals()
      }
    }
  },
  methods: {
    getGoals () {
      let options = {
        method: 'GET',
        mode: 'cors',
        headers: {
          'content-type': 'application/json',
        },
      }
      fetch(`${this.api}/goals?userid=${this.userId}`, options)
        .then(res => res.json())
        .then(res => {
          this.goals = res.data.goals
        })
    },
  },
  created () {
  },
  mounted () {
  },
  components: {
    GoalItem,
  },
}
</script>

<style scoped>
.goals {
  display: flex;
  flex-direction: column;
  width: 100%;
}
</style>
