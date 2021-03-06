<template>
  <div>
    <div class="goals">
      <transition-group name="goallist" tag='div' @enter="enter" @before-enter="beforeEnter" class='goals' :css="false">
        <GoalItem 
          v-for="(goal, i) of goals"
          :key="goal._id"
          :goal="goal"
          :data-index="i">
        </GoalItem>
      </transition-group>
    </div>
    <div class="goals goals__inactive" v-if="showAll">
      <h3>Past Goals</h3>
      <transition-group name="goallist" tag='div' @enter="enter" @before-enter="beforeEnter" class='goals' :css="false">
        <GoalItem 
          v-for="(goal, i) of inactiveGoals"
          :key="goal._id"
          :goal="goal"
          :data-index="i">
        </GoalItem>
      </transition-group>
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
      inactiveGoals: [],
      showAll: false,
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
      this.splitGoals(value)
    },
  },
  methods: {
    ...mapMutations([
      'updateGoals',
      'setGoals',
    ]),
    getGoals () {
      if (this.getStoreGoals.length > 0) {
        this.splitGoals(this.getStoreGoals)
      } else {
        fetch(`${this.api}/goals?userid=${this.userId}`, this.GET)
          .then(res => res.json())
          .then(res => {
            // split the goals between active/inactive
            this.splitGoals(res.data.goals)
            this.setGoals(res.data.goals)
          })
      }
    },
    checkGoals () {
      // current timestamp in seconds
      let now = new Date().getTime() / 1000
      this.goals
        .filter(v => v.active)
        .filter(v => v.progress.most_recent.date < now)
        .forEach((v) => {
          fetch(`${this.api}/goals/${v._id}`, this.GET)
            .then(response => response.json())
            .then(response => {
              this.updateGoals(response.data.goal)
            })
        })
    },
    splitGoals (list) {
      // splits the list of all goals given into active/inactive
      [this.goals, this.inactiveGoals] = list.reduce(([act, inact], el) => {
        return (el.active) ? [[...act, el], inact] : [act, [...inact, el]]
      }, [[],[]])
    },
    beforeEnter (el) {
      el.style.opacity = 0
      el.style.height = 0
    },
    enter (el, done) {
      let d = el.dataset.index * 550
      setTimeout( () => {
        el.style.opacity = 1
        el.style.height = '125px'
      }, d)
      done()
    },
  },
  created () {
    if (this.$route.name === 'goals') {
      this.showAll = true
    }
    if (this.userId !== undefined) {
      this.getGoals ()
    }
  },
  mounted () {
    this.$emit('loaded')
  },
  destroyed () {
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
  position: relative;
}
.goal__item {
  transition: all 1s;
}
.goallist {
}
</style>
