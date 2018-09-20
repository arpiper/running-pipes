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
    }
  },
  methods: {
    ...mapMutations([
      'setGoals',
    ]),
    getGoals () {
      if (this.getStoreGoals !== undefined) {
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
