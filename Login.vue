<template>
  <div>
    <form @submit.prevent="login">
      <input type="email" v-model="email" placeholder="Email" :class="{ 'error': !isValidEmail(email) }">
      <input type="password" v-model="password" placeholder="Password">
      <button type="submit">Login</button>
      <p>Forgot password? <a @click="resetPassword">Reset password</a></p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import bcrypt from 'bcryptjs';

export default {
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    isValidEmail(email) {
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      return emailRegex.test(email);
    },
    login() {
      const hashedPassword = bcrypt.hashSync(this.password, 10);
      axios.post('/login', { email: this.email, password: hashedPassword })
        .then(response => {
          console.log(response.data)
        })
        .catch(error => {
          console.error(error)
        })
    },
    resetPassword() {
      axios.post('/reset-password', { email: this.email })
        .then(response => {
          console.log(response.data)
        })
        .catch(error => {
          console.error(error)
        })
    }
  }
}
</script>
