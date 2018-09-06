<template>
  <div>
    <div class="goals">
      <Goal 
        v-for="goal of goals"
        :key="goal._id"
        :goal="goal">
      </Goal>
    </div>

  </div>
</template>

<script>
import Goal from './Goal.vue'
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
          console.log('fetch goals', res)
          this.goals = res.data.goals
        })
    },
  },
  created () {
    //this.getGoals()
  },
  mounted () {
  },
  components: {
    Goal,
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
