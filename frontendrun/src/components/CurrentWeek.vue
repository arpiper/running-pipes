<template>
  <div class="content__item">
    <Loading type='spin' :loading='loading'></loading>
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
import Loading from './Loading.vue'

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
      totalsReady: false,
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
      // zero indexed with sunday the first day. -1 adjustment to make Monday the first day.
      let d = this.date.getDay() - 1
      if (d === 0) {
        return this.date
      }
      return new Date(this.date.getFullYear(), this.date.getMonth(), this.date.getDate() - d)
    },
    weekEnd () {
      let d = this.date.getDay() - 1
      if (d === -1) {
        return this.date
      }
      return new Date(this.date.getFullYear(), this.date.getMonth(), this.date.getDate() + (6 - d))
    },
    allReady () {
      return this.totalsReady && this.getGoals.length > 0
    },
  },
  watch: {
    getGoals (value) {
      console.log('curretn week wathc', value)
      if (this.allReady) {
        this.checkImplicitGoals()
      }
    },
    allReady (value) {
      if (value) {
        this.checkImplicitGoals()
      }
    }
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
      console.log('activities, totals', this.activities, this.totals)
      this.totalsReady = true
    },
    checkImplicitGoals () {
      console.log('implicit goals', this.getGoals)
      this.implicitGoals = this.getGoals
        .filter((goal) => goal.active)
        .map((goal) => {
          // 86400000 milliseconds = 1 day, js timestamps are in milliseconds
          let end = new Date(goal.end * 1000)
          let t = Math.ceil((end - this.date) / 86400000)
          let r = 0
          let total = this.totals.dist
          let ig = {
            name: goal.name, 
            _id: goal._id
          }
          if (goal.type === 'distance') {
            r = goal.target_m - goal.progress.current_distance
          } else if (goal.type === 'time') {
            r = goal.target_m - goal.progress.current_duration
            total = this.totals.time
          }
          console.log('r', r, 't', t)
          ig['perDay'] = r / t
          ig['perWeek'] = (r / t) * 7
          ig['percent'] = 100 * (total / (ig['perWeek']))
          return ig
        })
    },
    childLoaded () {
      this.$emit('loaded')
      this.loading = false
    },
  },
  created () {
    this.getActivities()
  },
  components: {
    GoalItemSmall,
    Loading,
  }
}
</script>

<style scoped>
</style>
