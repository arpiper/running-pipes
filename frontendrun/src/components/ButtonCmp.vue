<template>
  <button class="button__button button__button_addgoal" ref='button'>
    <span class="button__icon_cross cross" ref='icon'></span>
    <span class="button__text_cross" ref='text'>{{ text }}</span>
  </button>
</template>

<script>
export default {
  name: 'button-cmp',
  props: {
    toggle: Boolean,
    text: {
      type: String,
      default: 'Add Goal',
    }
  },
  data () {
    return {
      cancel: 'Cancel',
      defaultText: 'Add Goal'
    }
  },
  watch: {
    toggle: function (value) {
      this.$refs.icon.classList.toggle('cross__x')
      this.$refs.button.classList.toggle('button__button_cancel')
      // set text to 'cancel'
      if (value) {
        this.defaultText = this.$refs.text.innerText
        this.$refs.text.innerText = this.cancel
      } else {
        this.$refs.text.innerText = this.defaultText
      }
    }
  },
}
</script>

<style>
.button__button {
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-main);
  border-radius: 2px;
  padding: 5px 20px;
  margin: 0 auto;
  transition: all 0.5s;
}
.button__button_cancel {
  background-color: var(--color-red);
  transition: all 0.5s;
}
.button__button:hover {
  cursor: pointer;
}
.button__icon {
}
.button__text_cross {
  margin-left: 15px;
}
</style>
