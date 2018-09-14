<template>
  <div class="goal__item_size_small">
    <h4 class="goal__header">{{ goal.name }}</h4>
    <span class="goal__data_pos_center" ref="percent" :style="percentStyle">
      {{ percent | number(0) }}%
    </span>
    <span >{{ goal.perWeek | distance }}</span>
    <div class="goal__progress-chart" :id="goalId">
    </div>
  </div>
</template>

<script>
let d3 = require('d3')

export default {
  name: 'goal-item-small',
  props: {
    goal: [Array, Object],
    id: [String, Number],
  },
  data () {
    return {
      svg: undefined,
      arcs: undefined,
      // radii
      ir: 35,
      or: 50,
      color: '#4caf40',
      percent: 0,
      leftPercent: 0,
      percentStyle: {left: 'calc(50%)'},
    }
  },
  computed: {
    goalId () {
      return `goal-${this.goal._id}`
    },
    angle () {
      return (this.goal.percent / 100) * (Math.PI * 2)
    },
    tau () {
      return Math.PI * 2
    },
  },
  watch: {
    leftPercent (l) {
      this.percentStyle = {left: `calc(50% - ${l / 2}px)`}
    },
  },
  methods: {
    drawCircle () {
      this.svg = d3.select(`#${this.goalId}`).append('svg')
        .attr('viewBox', `0 0 ${this.or * 2} ${this.or * 2}`)
        //.attr('preserveAspectRatio', 'none')
      let g = this.svg.append('g')
        .attr('class', 'goal-progress')
        .attr('transform', `translate(${this.or}, ${this.or})`)
      let g_back = this.svg.append('g')
        .attr('class', 'arc-background')
        .attr('transform', `translate(${this.or}, ${this.or})`)

      let arc0 = d3.arc()
        .innerRadius(this.ir)
        .outerRadius(this.or)
        .startAngle(0)

      let arc = d3.arc()({
        innerRadius: this.ir,
        outerRadius: this.or,
        startAngle: 0,
        endAngle: this.tau,
      })

      g_back.append('path')
        .attr('fill', '#9E9E9E4D')
        .attr('d', arc)

      let start = g.append('path')
        .datum({endAngle: 0})
        .attr('fill', this.color)
        .attr('d', arc0)
      
      start.transition()
        .duration(3500)
        .attrTween('d', arcTween(this.angle))

      function arcTween (newAngle) {
        return (d) => {
          var interpolate = d3.interpolate(d.endAngle, newAngle)
          return (t) => {
            d.endAngle = interpolate(t)
            return arc0(d)
          }
        }
      }
    },
    clearCircle () {
      d3.select(`#${this.goalId} svg`).remove()
    },
    countPercent () {
      let step = 2000 / this.goal.percent
      let timer = setInterval(() => {
        this.percent++
        if (this.$refs.percent.offsetWidth > this.leftPercent) {
          this.leftPercent = this.$refs.percent.offsetWidth
        }
        if (this.percent === 100 || this.percent === Math.round(this.goal.percent)) {
          clearInterval(timer)
        }
      }, step)
    },
  },
  mounted () {
    this.drawCircle()
    this.countPercent()
    this.$emit('loaded')
  },
}
</script>

<style scoped>
.goal__progress-chart {
  width: 110px;
  margin: auto;
}
.goal__item_size_small {
  position: relative;
}
.goal__data_pos_center {
  position: absolute;
  bottom: 33%;
  color: var(--color-secondary-dark);
  font-weight: bold;
}
</style>
