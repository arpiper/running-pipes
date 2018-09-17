<template>
  <div class="content__item">
    <div style="display: none;" class="loading__bar_container">
      <span  class="loading__bar">
      </span>
    </div>
    <div  class="content__item_header">
      <span class="block__current_week">
        <h2 class="item__header">
          {{ weekStart | date('%b%d') }} - {{ weekEnd | date('%b%d') }}
        </h2>
      </span>
    </div>
    <div class="content__item_main">
      <div class="content__item_main_left">
        <span class="content__item_time">{{ totals.time | time }}</span>
        <span class="content__item_dist">{{ totals.dist | distance | units }}</span>
      </div>
      <div class="content__item_main_right">
        <GoalItemSmall 
          v-for="g in implicitGoals" 
          :key="g._id" 
          :goal="g"
          @loaded="childLoaded()">
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
            this.setWeek(res.data.activities)
            this.activities = res.data.activities
            this.setTotals()
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
      this.implicitGoals = this.getGoals
        .filter((goal) => goal.active)
        .map((goal) => {
          // 86400000 milliseconds = 1 day
          let r = 0
          let total = this.totals.dist
          let t = Math.ceil((new Date(goal.end) - this.date) / 86400000)
          let ig = {
            name: goal.name, 
            _id: goal._id
          }
          if (goal.type === 'distance') {
            r = goal.target_m - goal.progress.current_distance
          } else if (goal.type === 'time') {
            r = goal.target_m - goal.progress.current_duration
            total = this.totals.duration
          }
          ig['perDay'] = r / t
          ig['perWeek'] = (r / t) * 7
          ig['percent'] = 100 * (total / (ig['perWeek']))
          return ig
        })
    },
    childLoaded () {
      this.loading = false
      this.$emit('loaded')
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
