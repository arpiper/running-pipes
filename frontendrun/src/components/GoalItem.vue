<template>
  <div class="goal__item">
    <div class="goal__header">
      <span v-if="goal.name" class="goal__info">
        <h3 class="goal__name">{{ goal.name }}</h3>
        <span class="goal__target">{{ goal.target }} {{ units }}</span>
      </span>
      <span class="goal__progress_bar" :style="borderBottom()"></span>
      <span class="goal__dates">
        {{ start_date | date('%b%d%Y') }} - {{ end_date | date('%b%d%Y') }}
      </span>
    </div>
    <div v-if="goal.progress && goal.type === 'distance'" class="goal__progress">
      <span class="goal__progress_item">
        {{ goal.progress.current_distance | distance | units }}
      </span>
      <span class="goal__progress_item">
        {{ goal.progress.percent_complete | number(0) }}% Completed
      </span>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'goal-item',
  props: {
    id: [String, Number],
    goal: [Object, Array],
  },
  data () {
    return {
    }
  },
  computed: {
    ...mapGetters({
      api: 'api',
      userId: 'getUserId',
    }),
    start_date () {
      return new Date(`${this.goal.start}T00:00:00`)
    },
    end_date () {
      return new Date(`${this.goal.end}T00:00:00`)
    },
    units () {
      if (this.goal.type == 'distance') {
        return 'miles'
      } else if (this.goal.type == 'time') {
        return 'hours'
      }
      return 'minutes/mile'
    },
  },
  methods: {
    borderBottom () {
      let width = '0'
      if (this.goal.progress) {
        width = `${this.goal.progress.percent_complete}%`
      }
      return {
        'border-bottom': '2px solid var(--color-main)',
        'width': width,
      }
    },
  },
  created () {
  }
}
</script>

<style>
.goal__item {
  display: flex;
  padding: 10px;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  height: 125px;
  background-color: white;
  box-shadow: 0px 8px 24px rgba(13, 13, 18, 0.04);
  margin-top: 10px;
  margin-bottom: 5px;
}
.goal__header {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-content: flex-start;
}
.goal__info {
  display: flex;
  align-items: center;
}
.goal__name { 
  margin: 0;
  display: inline-block;
}
.goal__target {
  margin-left: 15%;
}
.goal__dates {
  margin-right: auto;
  padding-top: 5px;
  font-size: 14px;
}
.goal__progress_bar {
  display: inline-block;
}
.goal__progress {
  display: flex;
  align-items: center;
  width: 100%;
  font-size: 1.5em;
}
.goal__progress_item {
  margin-left: 10px;
}
</style>
