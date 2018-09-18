<template>
  <div>
    <div class="block__athlete" v-if="athlete">
      <div class="block__info">
        <span>  
          <img :src="athlete.profile_medium" />
        </span>
        <span>{{ athlete.firstname }}</span>
        <span>{{ athlete.lastname }}</span>
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
            this.setStats(res.data.stats)
          })
      }
    },
  },
  mounted () {
  }
}
</script>
