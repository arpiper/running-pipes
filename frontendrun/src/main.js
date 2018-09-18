import Vue from 'vue'
import App from './App.vue'

import './filters/Filters.js'
import store from './store.js'
import router from './router.js'

Vue.config.productionTip = false
new Vue({
  render: h => h(App),
  store,
  router,
}).$mount('#app')
