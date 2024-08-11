<template>
  <div>
    <form @submit.prevent="register">
      <input type="email" v-model="email" placeholder="Email" :class="{ 'error': !isValidEmail(email) }">
      <input type="password" v-model="password" placeholder="Password" :class="{ 'error': !isValidPassword(password) }">
      <input type="password" v-model="confirmPassword" placeholder="Confirm Password" :class="{ 'error': password !== confirmPassword }">
      <button type="submit">Register</button>
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
      password: '',
      confirmPassword: ''
    }
  },
  methods: {
    isValidEmail(email) {
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      return emailRegex.test(email);
    },
    isValidPassword(password) {
      const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
      return passwordRegex.test(password);
    },
    register() {
      const hashedPassword = bcrypt.hashSync(this.password, 10);
      axios.post('/register', { email: this.email, password: hashedPassword })
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