<template>
  <div class="block__datepicker datepicker-wrapper" :class="wrapper_classes">
    <label ref="label" for="#input_datepicker" :class="labels_classes">
      {{ label_name }}
    </label>
    <input 
      readonly="true" 
      :class="input_classes" 
      type="text" 
      :name="name" 
      id="input__datepicker" 
      @click="init(event)" 
      ref="input"
      :value="isoFormat" 
    >
    <div class="datepicker hide" ref:container>
      <span 
        v-for="(date, idx) of dates"
        :key="idx"
        :style="date.style"
      >
        {{ date.day }}
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
  },
  data () {
    return {
      days: ["S","M","T","W","T","F","S"], 
      leap_year: false,
      today: new Date(),
      year: 0,
      month: 0,
      insert: false,
      name: "date",
      dates: [],
      months = {
        0: {name: "January", days: 31},
        1: {name: "February", days: 28},
        2: {name: "March", days: 31},
        3: {name: "April", days: 30},
        4: {name: "May", days: 31},
        5: {name: "June", days: 30},
        6: {name: "July", days: 31},
        7: {name: "August", days: 31},
        8: {name: "September", days: 30},
        9: {name: "October", days: 31},
        10: {name: "November", days: 30},
        11: {name: "December", days: 31}
      }
    }
  },
  computed: {
    isoFormat (d) {
      return d.toISOString().split('T')[0]
    }
    month () {
      return this.today.getMonth()
    },
    year () {
      return this.today.getFullYear()
    },
  },
  oncreate() {
    // global click to close on click away event.
  },
  methods: {
    pickDate (evt, date) {
    },
    nextMonth (m) {
    },
    prevMonth (m) {
      let d = new Date(this.year, m, 1)
      this.dates = this.createDatesArray(d)
    }
    createDatesArray(d) {
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
div, 
span {
  box-sizing: border-box;
}
.datepicker {
  width: 50%;
  box-sizing: border-box;
  text-align: center;
  position: absolute;
  z-index: 1000;
  cursor: default;
  background-color: #eee;
}
.datepicker.hide {
  display: none;
}
.datepicker span {
  display: inline-block;
}
.datepicker .month {
  width: 71.42%;
}
.datepicker .day-name {
  font-wieght: bold;
  background-color: #bbb;
}
.datepicker .day, 
.datepicker .day-name, 
.datepicker .month, 
.datepicker .spacer, 
.datepicker .gap, 
.datepicker .arrow {
  font-size: 1em;
  height: 30px;
  line-height: 30px;
  /*border-left: 1px solid grey;
  border-top: 1px solid gray;*/
}
.datepicker .day, 
.datepicker .day-name, 
.datepicker .arrow, 
.datepicker .gap, 
.datepicker .spacer {
  width: 14.28%;
  vertical-align: top;
}
.datepicker .weekend {
  background-color: hsla(110, 90%, 50%, .5);
}
.datepicker .today {
  background-color: hsla(200, 100%, 50%, .75 );
}
.datepicker .day:hover, 
.datepicker .arrow:hover {
  background-color: hsla(220, 100%, 50%, .75);
}
.datepicker .gap, 
.datepicker .spacer {
  background-color: #ddd;
  font-size: 16px;
}
</style>
