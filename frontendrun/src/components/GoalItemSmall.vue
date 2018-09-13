<template>
  <div class="goal__item_size_small">
    <button @click="drawCircle()" >click</button>
    <h4 @click="clearCircle()" class="goal__header">{{ goal.name }}</h4>
    <span>{{ goal.percent | number(0) }}%</span>
    <span>{{ goal.perWeek | distance }}</span>
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
      color: '#4caf40'
    }
  },
  computed: {
    goalId () {
      return `goal-${this.goal._id}`
    },
  },
  methods: {
    drawCircle () {
      console.log('draw', this.goal)
      this.svg = d3.select(`#${this.goalId}`).append('svg')
        .attr('viewBox', `0 0 ${this.or * 2} ${this.or * 2}`)
        //.attr('preserveAspectRatio', 'none')
      let g = this.svg.append('g')
        .attr('class', 'goal-progress')
        .attr('transform', `translate(${this.or}, ${this.or})`)

      let arc0 = d3.arc()
        .innerRadius(this.ir)
        .outerRadius(this.or)
        .startAngle(0)

      let arc = d3.arc()({
        innerRadius: this.ir,
        outerRadius: this.or,
        startAngle: 0,
        endAngle: ((this.goal.percent / 100) * (Math.PI * 2)),
      })

      /*
      let bg = g.append('path')
        .datum({endAngle: Math.PI * 2})
        .attr('fill', '#9e9e9e')
        .attr('d', arc0)
      */

      let start = g.append('path')
        .datum({endAngle: Math.PI / 2})
        .attr('fill', this.color)
        .attr('d', arc0)
      
      start.transition()
        .duration(2000)
        .attrTween('d', arcTween(Math.PI))
        //.attrTween('d', arcTween((this.goal.percent / 100) * (Math.PI * 2)))

      /*
      let a = g.selectAll('path').data([1])
        .enter().append('path')
          .attr('class', 'arc')
          .attr('fill', this.color)
          .attr('d', arc)
          */
      function arcTween (angle) {
        return (d) => {
          var interpolate = d3.interpolate(d.endAngle, angle)
          return (t) => {
            d.engAngle = interpolate(t)
            return arc0(d)
          }
        }
      }
    },
    clearCircle () {
      d3.select(`#${this.goalId} svg`).remove()
    },
    
  },
  mounted () {
    this.drawCircle()
    this.$emit('loaded')
  },
}
</script>

<style>
.goal__progress-chart {
  width: 110px;
  margin: auto;
}
</style>
