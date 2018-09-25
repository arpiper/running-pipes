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
import { mapGetters, mapMutations } from 'vuex'

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
      GET: 'getGetOpts',
      getStoreGoals: 'getGoals',
    }),
  },
  watch: {
    userId (id) {
      if (id !== undefined) {
        this.getGoals()
      }
    },
    goals (value) {
      if (value.length > 0) {
        this.checkGoals()
      }
    },
    getStoreGoals (value) {
      this.goals = value
    },
  },
  methods: {
    ...mapMutations([
      'setGoals',
    ]),
    getGoals () {
      if (this.getStoreGoals.length > 0) {
        console.log('goals', this.getStoreGoals)
        this.goals = this.getStoreGoals
      } else {
        fetch(`${this.api}/goals?userid=${this.userId}`, this.GET)
          .then(res => res.json())
          .then(res => {
            this.goals = res.data.goals
            this.setGoals(res.data.goals)
          })
      }
    },
    checkGoals () {
      // current timestamp in seconds
      let now = new Date().getTime() / 1000
      this.goals
        .filter(v => v.active)
        .forEach((v, i) => {
          if (v.progress.most_recent.date < now) {
            console.log('updating goal progress')
            fetch(`${this.api}/goals/${v._id}`, this.GET)
              .then(response => response.json())
              .then(response => {
                console.log('update fecth',response)
                this.goals[i] = response.data.goal
              })
          }
        })
    },
  },
  created () {
    if (this.userId !== undefined) {
      this.getGoals ()
    }
  },
  mounted () {
    this.$emit('loaded')
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
