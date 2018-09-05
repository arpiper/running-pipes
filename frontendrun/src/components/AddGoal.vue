<template>
  <div class="form__goal">
    <form name="add_goal" @submit.prevent="formSubmit">
      <input type="hidden" name="goal_userid" :value="userId" >
      <div class="form__group">
        <label>Name</label>
        <input type="text" v-model="goal_name">
      </div>
      <div class="form__group">
        <label >Goal Type</label>
        <select name="goal_type" v-model="goal_type">
          <option v-for="(type, idx) in types" :value="type" :key="idx">
            {{ type }}
          </option>
        </select>
      </div>
      <DatePicker 
        @datePicked="startDatePicked($event)" 
        label_name="Start Date" 
        wrapper_classes="form__group">
      </DatePicker>
      <DatePicker 
        @datePicked="endDatePicked($event)" 
        label_name="End Date" 
        wrapper_classes="form__group">
      </DatePicker>
      <div class="form__group">
        <label for="goal_target">Target</label>
        <input id="goal_target" name="goal_target" v-model="goal_target" />
      </div>
      <button>submit</button>
    </form>
  </div>
</template>

<script>
import DatePicker from './DatePicker.vue'
export default {
  name: 'add-goal',
  props: {
    userId: [String, Number],
  },
  data () {
    return {
      goal_target: '',
      types: [
        'distance',
        'time',
        'pace',
      ],
      goal_name: 'Goal',
      goal_type: undefined,
      goal_start: new Date().toISOString().split('T')[0],
      goal_end: new Date().toISOString().split('T')[0],
      url: 'http://localhost:5000/api/goals',
    }
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
