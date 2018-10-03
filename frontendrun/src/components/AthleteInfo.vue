<template>
  <div class="athlete" v-if="athlete && stats">
    <div class="info info__athlete">
      <span class="info__img">
        <img :src="athlete.profile_medium" />
      </span>
      <span class="info__name">
        <span class="info__firstname">{{ athlete.firstname }}</span>
        <span class="info__lastname">{{ athlete.lastname }}</span>
      </span>
    </div>
    <div class="info">
      <span class="info__date">{{ year }}</span>
      <span class="info__activity">Run</span>
      <div class="info__stats">
        <span>{{ stats.ytd_run_totals.count }}</span>
        <span>{{ stats.ytd_run_totals.distance | distance | units }}</span>
      </div>
      <span class="info__activity">Ride</span>
      <div class="info__stats">
        <span>{{ stats.ytd_ride_totals.count }}</span>
        <span>{{ stats.ytd_ride_totals.distance | distance | units }}</span>
      </div>
      <span class="info__activity">Swim</span>
      <div class="info__stats">
        <span>{{ stats.ytd_swim_totals.count }}</span>
        <span>{{ stats.ytd_swim_totals.distance | distance | units }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'

export default {
  name: 'athlete-info',
  data () {
    return {
      stats: undefined,
      year: new Date().getUTCFullYear(),
    }
  },
  computed: {
    ...mapGetters({
      athlete: 'getAthlete',
      getStoreStats: 'getStats',
      userId: 'getUserId',
      GET: 'getGetOpts',
      api: 'api',
    }),
  },
  watch: {
    userId (id) {
      if (id !== undefined) {
        this.getStats()
      }
    }
  },
  methods: {
    ...mapMutations([
      'setStats',
    ]),
    getStats () {
      if (this.getStoreStats) {
        this.stats = this.getStoreStats
      } else {
        fetch(`${this.api}/stats/${this.userId}`, this.GET)
          .then(res => res.json())
          .then(res => {
            console.log('stats', res)
            this.stats = res.data.stats
            this.setStats(res.data.stats)
          })
      }
    },
  },
  mounted () {
    if (this.userId !== undefined) {
      this.getStats()
      console.log('athlete', this.athlete, this.stats)
    }
  }
}
</script>
