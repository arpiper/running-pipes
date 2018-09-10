<template>
  <div class="content__item">
    <span v-if="loading" class="loading-bar">
    </span>
    <div v-if="!loading" class="content__item_header">
      <span class="block__current_week">
        {{ weekStart | formatDate }} - {{ weekEnd | formatDate }}
      </span>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'current-week',
  props: {
  },
  data () {
    return {
      loading: true,
      activities: [],
      date: new Date(),
    }
  },
  computed: {
    ...mapGetters({
      userId: 'getUserId',
      GET: 'getGetOpts',
      api: 'api',
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
    userId (id) {
    },
  },
  filters: {
    formatDate (val) {
      let s = val.toUTCString().split(' ')
      return `${s[0]} ${s[1]} ${s[2]}`
    },
  },
  methods: {
    getActivities () {
      fetch(`${this.api}/activities`, this.GET)
        .then(res => res.json())
        .then(res => {
          console.log('activities', res)
          this.activities = res.data.activities
          this.loading = false
        })
    },
  },
  created () {
    this.getActivities()
  },
}
</script>

<style scoped>
</style>
