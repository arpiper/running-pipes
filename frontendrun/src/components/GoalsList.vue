<template>
  <div>
    <div class="goals">
      <transition-group name="goallist" tag='div' @enter="enter" @beforeEnter="beforeEnter" class='goals' :css="false">
      <GoalItem 
        v-for="(goal, i) of goals"
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
    beforeEnter (el) {
      el.style.opacity = 0
      el.style.top = `-100px`
      el.style.backgroundColor = 'blue'
      console.log('beforeenter', el)
    },
    enter (el) {
      let d = el.dataset.index * 550
      let t = el.dataset.index * 135
      console.log('enter', el)
      setTimeout( () => {
        el.style.opacity = 1
        el.style.top = `${t}px`
        el.style.backgroundColor = 'white'
      }, d)
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
  position: relative;
}
.goal__item {
  position: absolute;
  width: 100%;
}
.goallist {
  transition: all 1s;
}
</style>
