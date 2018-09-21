<template>
  <div class="datepicker" :class="wrapper_classes">
    <label ref="label" :class="label_classes" class="datepicker__label">
      {{ label_name }}
    </label>
    <input 
      readonly="true" 
      :class="input_classes" 
      class="datepicker__input"
      type="text" 
      :name="name" 
      :id="input_datepicker_id" 
      @click="showDatePicker()" 
      ref="input"
      :value="isoFormat">
    <div v-if="show" class="datepicker__calendar" ref:container :style="calendarPos">
      <div class="datepicker__header">
        <span class="datepicker__prev" @click="setMonth(month.index - 1)">&lt;-</span>
        <span>{{ month.name }}</span>
        <span class="datepicker__next" @click="setMonth(month.index + 1)">-&gt;</span>
      </div>
      <span 
        v-for="(day, i) of days" 
        :key="i+day" 
        class="datepicker__dayname"
        :style="{left: i * (100 / 7) + '%', top: 20 + 'px'}">
        {{ day }}
      </span>
      <span 
        v-for="(date, idx) of dates"
        :key="idx"
        :style="getDateBlockStyle(date)"
        class="datepicker__day"
        :class="date.classes"
        @click='pickDate($event, date.day)'>
        {{ date.day.getDate() }}
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'date-picker',
  props: {
    label_classes: String,
    wrapper_classes: String,
    input_classes: String,
    label_name: {
      type: String,
      default: 'Date',
    },
    input_datepicker_id: [String, Number],
  },
  data () {
    return {
      show: false,
      days: ["S","M","T","W","T","F","S"], 
      today: new Date(),
      month: {
        name: '',
        index: 0
      },
      insert: false,
      name: 'date',
      date: new Date(),
      dates: [],
      months: [
        'January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December'
      ],
      calendarPos: undefined,
    }
  },
  computed: {
    isoFormat () {
      return this.date.toISOString().split('T')[0]
    },
    year () {
      return this.today.getFullYear()
    },
  },
  created () {
    // set the month/dates for the current month
    this.month.index = this.today.getUTCMonth()
    this.month.name = this.months[this.month.index]
    this.dates = this.createDatesArray(this.today)

  },
  mounted () {
    //console.log('mount',this.$refs.input.offsetHeight)
    let height = this.$refs.input.offsetHeight + this.$refs.label.offsetHeight
    this.calendarPos = {
      top: `${height}px`,
    }
  },
  methods: {
    // toggle whether to show/hide the datepicker calendar
    showDatePicker () {
      this.show = !this.show
    },
    // pick the date and emit the datePicked event
    pickDate (evt, date) {
      this.date = date
      this.showDatePicker()
      this.$emit('datePicked', date)
    },
    // set the the month to the given value
    setMonth (m) {
      let d = new Date(this.year, m, 1)
      this.dates = this.createDatesArray(d)
      this.month = {
        name: this.months[d.getUTCMonth()],
        index: m,
      }
    },
    // return a style object for individual date blocks
    getDateBlockStyle (d) {
      return {
        left: `${(100 / 7) * d.day.getDay()}%`,
        top: `${d.row * 20}px`,
      }
    },
    // create an array of date objects for the selected month 
    // and any trailing/leading days
    createDatesArray (d) {
      let month = d.getUTCMonth()
      let year = d.getUTCFullYear()
      let last = new Date(year, month + 1, 0)
      let first = new Date(year, month, 1)
      let rowValue = 2
      let a = []
      // create the leading days for the month before the selected one.
      let end = first.getDay() > 0 ? first.getDay() : 7
      for (let i = 1; i <= end; i++) {
        a.push({
          day: new Date(year, month, i - end),
          row: rowValue,
          classes: 'datepicker__day_extra',
        })
      }
      // create array with the selected month's dates
      let m = Array(last.getDate())
        .fill(1, 0, last.getDate())
        .map((v,i) => {
          let day = new Date(year, month, i + 1)
          //rowValue = Math.abs(Math.floor((day.getDay() - day.getDate()) / 7)) + 1
          if (day.getDay() === 0) {
            rowValue++
          }
          if (day.toDateString() === this.today.toDateString()) {
            return {day: day, row: rowValue, classes: 'datepicker__day_today'}
          }
          return {day: day, row: rowValue, classes: ''}
        })
      // create array of trailing days for following month
      let b = []
      if (last.getDay() !== 6) {
        for (let i = 1; i < 7 - last.getDay(); i++) {
          b.push({
            day: new Date(year, month + 1, i),
            row: rowValue,
            classes: 'datepicker__day_extra',
          })
        }
      }
      // return a single array with the three groups of dates
      return a.concat(m, b)
    },
    positionContainer (target) {
      this.$refs.container.styles ={
        "left": target.offsetLeft
      }
    },

  },
};
</script>

<style scoped>
.datepicker,
.datepicker__input,
.datepicker__label,
.datepicker__calendar,
.datepicker__header,
.datepicker__dayname,
.datepicker__day,
.datepicker__next,
.datepicker__prev {
  box-sizing: border-box;
}
.datepicker {
  position: relative;
}
.datepicker__input {
  width: 100%;
}
.datepicker__calendar {
  position: absolute;
  left: 0;
  z-index: 100;
  background-color: #ddd;
  width: 100%;
  height: auto;
}
.datepicker__header,
.datepicker__dayname,
.datepicker__day {
  text-align: center;
  background-color: #ddd;
  height: 20px;
  padding: 2px;
}
.datepicker__header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.datepicker__dayname,
.datepicker__day {
  position: absolute;
  width: 14.29%;
}
.datepicker__day_extra {
  color: #888;
}
.datepicker__day_today {
  color: #a33;
}
.datepicker__next,
.datepicker__prev {
  width: 20%;
}
.datepicker__day:hover,
.datepicker__next:hover,
.datepicker__prev:hover {
  cursor: pointer;
  background-color: rgba(76, 175, 80, 1);
}
</style>
