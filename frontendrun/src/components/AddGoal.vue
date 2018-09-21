<template>
  <div>
    <form name="add_goal" @submit.prevent="formSubmit" class="form__goal">
      <input type="hidden" name="goalUserId" :value="userId" >
      <div class="form__group">
        <label>Name</label>
        <input type="text" v-model="goalName" autocomplete="off">
      </div>
      <div class="form__group">
        <label >Goal Type</label>
        <select name="goalType" v-model="goalType">
          <option v-for="(type, idx) in goalTypes" :value="type" :key="idx">
            {{ type }}
          </option>
        </select>
      </div>
      <div class="form__group">
        <label>Activity</label>
        <select name="goalActivity" v-model="goalActivity">
          <option v-for="type in goalActivities" :value="type" :key="type">
            {{ type }}
          </option>
        </select>
      </div>
      <DatePicker 
        @datePicked="startDatePicked($event)" 
        label_name="Start Date" 
        id="goal_start_date"
        wrapper_classes="form__group">
      </DatePicker>
      <DatePicker 
        @datePicked="endDatePicked($event)" 
        label_name="End Date" 
        id="goal_end_date"
        wrapper_classes="form__group">
      </DatePicker>
      <div class="form__group">
        <label for="goalTarget">Target</label>
        <input id="goalTarget" name="goalTarget" v-model="goalTarget" autocomplete="off" />
      </div>
      <button>submit</button>
    </form>
  </div>
</template>

<script>
import DatePicker from './DatePicker.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'add-goal',
  props: {
    //userId: [String, Number],
  },
  data () {
    return {
      goalTarget: '',
      goalTypes: [
        'distance',
        'time',
        'pace',
      ],
      goalActivities: [
        'Run',
        'Ride',
        'Swim',
      ],
      goalName: "Goal",
      goalActivity: 'Run',
      goalType: 'distance',
      goalStart: new Date(),
      goalEnd: new Date(),
      url: 'http://localhost:5000/api/goals',
    }
  },
  computed: {
    ...mapGetters({
      userId: 'getUserId',
      POST: 'getPostOpts',
    }),
  },
  methods: {
    startDatePicked (date) {
      this.goalStart = date
    },
    endDatePicked (date) {
      this.goalEnd = date
    },
    formSubmit () {
      let target_m = 0
      if (this.goalType === 'distance') {
        target_m = (this.goalTarget / 0.000621371) // convert to meters
      } else if (this.goalType === 'time') {
        target_m = (this.goalTarget / 60 / 60) // convert to seconds
      }
      let data = {
        name: this.goalName,
        userid: this.userId,
        target: this.goalTarget,
        target_m: target_m,
        type: this.goalType,
        start: this.goalStart.getTime() / 1000,
        end: this.goalEnd.getTime() / 1000,
        activity: this.goalActivity,
        active: true,
      }
      console.log("post data", data)
      let options = this.POST
      options.body = JSON.stringify(data),
      fetch(this.url, options)
        .then(res => res.json())
        .then(res => {
          console.log(res)
          // emit event to notify parent of new goal
        })
    },
  },
  components: {
    DatePicker,
  }
}
</script>

<style>
.form__goal {
  width: 100%;
  flex-direction: column;
  width: 100%;
}
.form__group {
  display: flex;
  flex-direction: column;
  width: 100%;
}
</style>
