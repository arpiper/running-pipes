<template>
  <div class="content__item goal" v-if="goal">
    <div class="content__item_header">
      <h2>{{ goal.name }}</h2>
    </div>
    <div class="content__item_left">
      <span>
        {{ start | date('%b%d%Y') }} - {{ end | date('%b%d%Y') }}
      </span>
      <span>
        {{ goal.target | units }}
      </span>
    </div>
    <div class="content__item_right">
      {{ goal.progress.activity_cnt }}
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'goal-detail-cmp',
  props: {
    id: String,
  },
  data () {
    return {
      goal: undefined,
    }
  },
  computed: {
    ...mapGetters({
      getGoal: 'getGoal',
      getGoals: 'getGoals',
      GET: 'getGetOpts',
      api: 'api',
    }),
    start () {
      return new Date(this.goal.start * 1000)
    },
    end () {
      return new Date(this.goal.end * 1000)
    }
  },
  methods: {
    fetchGoal () {
      fetch(`${this.api}/goals/${this.id}`, this.GET)
        .then(response => response.json())
        .then(response => {
          console.log("geh," , response)
          this.goal =response.data.goal
        })
    },
  },
  created () {
    console.log('created detal')
  },
  mounted () {
    this.goal = this.getGoal(this.id)
    if (this.goal === undefined) {
      this.fetchGoal()
    }
    console.log(this.id)
    console.log(this.goal)
    console.log('mounted detal')
  },
}
</script>
