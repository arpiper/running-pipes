<template>
  <div>
    <form name="add_goal" @submit.prevent="formSubmit" class="form__goal">
      <input type="hidden" name="goal_userid" :value="userId" >
      <div class="form__group">
        <label>Name</label>
        <input type="text" v-model="goal_name" autocomplete="off">
      </div>
      <div class="form__group">
        <label >Goal Type</label>
        <select name="goal_type" v-model="goal_type">
          <option v-for="(type, idx) in goal_types" :value="type" :key="idx">
            {{ type }}
          </option>
        </select>
      </div>
      <div class="form__group">
        <label>Activity</label>
        <select name="goal_activity" v-model="goal_activity">
          <option v-for="type in goal_activities" :value="type" :key="type">
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
        <label for="goal_target">Target</label>
        <input id="goal_target" name="goal_target" v-model="goal_target" autocomplete="off" />
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
      goal_target: '',
      goal_types: [
        'distance',
        'time',
        'pace',
      ],
      goal_activities: [
        'Run',
        'Ride',
        'Swim',
      ],
      goal_name: "Goal",
      goal_activity: 'Run',
      goal_type: 'distance',
      goal_start: new Date().toISOString().split('T')[0],
      goal_end: new Date().toISOString().split('T')[0],
      url: 'http://localhost:5000/api/goals',
    }
  },
  computed: {
    ...mapGetters({
      userId: 'getUserId',
    }),
  },
  methods: {
    startDatePicked (date) {
      this.goal_start = date.toISOString().split('T')[0]
    },
    endDatePicked (date) {
      this.goal_end = date.toISOString().split('T')[0]
    },
    formSubmit () {
      let data = {
        name: this.goal_name,
        userid: this.userId,
        target: this.goal_target,
        type: this.goal_type,
        start: this.goal_start,
        end: this.goal_end,
      }
      let options = {
        method: 'POST',
        //credentials: 'include',
        body: JSON.stringify(data),
        mode: 'cors',
        headers: {
          'content-type': 'application/json'
        },
      }
      fetch(this.url, options)
        .then(res => {
          console.log(res)
          return res.json()
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
