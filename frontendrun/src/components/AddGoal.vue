<template>
  <div class="form__goal">
    <form name="add_goal" @submit.prevent="formSubmit">
      <input type="hidden" name="goal_userid" :value="userid" >
      <select name="goal_type" v-model="goal_type">
        <option v-for="(type, idx) in goal_types" :value="type" :key="idx">
          {{ type }}
        </option>
      </select>
      <div class="form__group">
        <label>Start Date</label>
        <input v-model="goal_start" >
      </div>
      <div class="form__group">
        <label>End Date</label>
        <input v-model="goal_end">
      </div>
      <div class="form__group">
        <label for="goal_target">Target</label>
        <input id="goal_target" name="goal_target" v-model="goal_target" />
      </div>
      <button>submit</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'add-goal',
  props: {
    userid: [String, Number],
  },
  data () {
    return {
      goal_target: '',
      goal_types: [
        'distance',
        'time',
        'pace',
      ],
      goal_type: undefined,
      goal_start: 0,
      goal_end: 0,
      goal_url: 'http://localhost:5000/api/goals',
    }
  },
  methods: {
    formSubmit(evt) {
      console.log('ect', evt)
      let data = {
        userid: this.userid,
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
        header: {
          'content-type': 'application/json'
        },
      }
      fetch(this.goal_url, options)
        .then(res => {
          console.log(res)
        })
    }
  }
}
</script>
