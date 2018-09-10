<template>
  <div class="block__athlete" v-if="athlete">
    <div class="block__info">
      <span>  
        <img :src="athlete.profile_medium" />
      </span>
      <span>{{ athlete.firstname }}</span>
      <span>{{ athlete.lastname }}</span>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'athlete-info',
  data () {
    return {
    }
  },
  computed: {
    ...mapGetters({
      athlete: 'getAthlete',
    })
  },
  methods: {
    getStats () {
      fetch(`${this.api}/stats/${this.userId}`, this.GET)
        .then(res => res.json())
        .then(res => {
          console.log('stats', res)
        })
    },
  },
  mounted () {
  }
}
</script>
