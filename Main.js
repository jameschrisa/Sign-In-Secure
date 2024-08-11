import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import bcrypt from 'bcryptjs'

Vue.prototype.$axios = axios
Vue.prototype.$bcrypt = bcrypt

new Vue({
  render: h => h(App)
}).$mount('#app')