<template>
  <v-container class="mt-10" max-width="400">
    <v-card title="Login">
      <v-card-text>
        <v-text-field v-model="username" label="Username" variant="outlined" />
        <v-text-field v-model="password" label="Password" type="password" variant="outlined" />
        <v-btn color="primary" block @click="handleLogin">Login</v-btn>
        <v-btn variant="text" block to="/register" class="mt-2">Register</v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const username = ref('')
const password = ref('')

async function handleLogin() {
  await auth.login(username.value, password.value)
  await auth.fetchUser()
  router.push('/')
}
</script>
