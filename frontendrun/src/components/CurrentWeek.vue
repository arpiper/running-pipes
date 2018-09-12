<template>
  <div class="content__item">
    <span v-if="loading" class="loading-bar">
    </span>
    <div v-if="!loading" class="content__item_header">
      <span class="block__current_week">
        {{ weekStart | date('%b%d') }} - {{ weekEnd | date('%b%d') }}
      </span>
    </div>
    <div class="content__item_main">
      <div class="content__item_main_left">
        <span class="content__item_time">{{ totals.time | time }}</span>
        <span class="content__item_dist">{{ totals.dist | distance | units }}</span>
      </div>
      <div class="content__item_main_right">
        <GoalItemSmall v-for="(g, i) in implicitGoals" :key="i" :goal="g">
        </GoalItemSmall>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import GoalItemSmall from './GoalItemSmall.vue'

export default {
  name: 'current-week',
  props: {
  },
  data () {
    return {
      loading: true,
      activities: [],
      date: new Date(),
      totals: {
        time: 0,
        dist: 0,
      },
      implicitGoals: [],
    }
  },
  computed: {
    ...mapGetters({
      userId: 'getUserId',
      GET: 'getGetOpts',
      api: 'api',
      getGoals: 'getGoals',
      getWeek: 'getWeek',
    }),
    weekStart () {
      let d = this.date.getDay()
      if (d === 0) {
        return this.date
      }
      return new Date(this.date.getFullYear(), this.date.getMonth(), this.date.getDate() - d)
    },
    weekEnd () {
      let d = this.date.getDay()
      if (d === 6) {
        return this.date
      }
      return new Date(this.date.getFullYear(), this.date.getMonth(), this.date.getDate() + (6 - d))
    },
  },
  watch: {
    getGoals () {
      this.checkImplicitGoals()
    },
  },
  methods: {
    ...mapMutations([
      'setWeek',
    ]),
    getActivities () {
      if (this.getWeek) {
        this.activities = this.getWeek
      } else {
        fetch(`${this.api}/activities`, this.GET)
          .then(res => res.json())
          .then(res => {
            console.log('activities', res)
            this.setWeek(res.data.activities)
            this.activities = res.data.activities
            this.setTotals()
            this.loading = false
          })
      }
    },
    setTotals () {
      this.activities.forEach((a) => {
        this.totals.time += a.moving_time
        this.totals.dist += a.distance
      })
    },
    checkImplicitGoals () {
      // 86400000 milliseconds = 1 day
      this.getGoals.forEach((goal) => {
        let t = Math.ceil((new Date(goal.end) - this.date) / 86400000)
        console.log('time', t)
        if (goal.type === 'distance') {
          this.implicitGoals.push(this.distanceGoal(goal, t))
        } else if (goal.type === 'time') {
          this.implicitGoals.push(this.timeGoal(goal, t))
        } else {
          this.implicitGoals.push(this.paceGoal(goal, t))
        }
      })
      console.log(this.implicitGoals)
    },
    distanceGoal (goal, time) {
      let r = goal.target - goal.progress.current_distance
      console.log('remain', r)
      return {
        perDay: r / time,
        perWeek: (r / time) * 7,
        percent: this.totals.dist / ((r / time) * 7),
        name: goal.name,
      }
    },
    timeGoal (goal, time) {
      let r = goal.target - goal.progress.current_duration
      return {
        perDay: r / time,
        perWeek: (r / time) * 7,
        percent: this.totals.duration / ((r / time) * 7),
        name: goal.name,
      }
    },
    paceGoal (goal, time_remain) {
    },
  },
  created () {
    this.getActivities()
  },
  components: {
    GoalItemSmall,
  }
}
</script>

<style scoped>
</style>
