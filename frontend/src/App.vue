<template>
  <v-app>
    <v-app-bar app>
      <v-app-bar-title @click="$router.push('/')" style="cursor:pointer">MLOps</v-app-bar-title>
      <v-spacer />
      <v-btn v-if="auth.isLoggedIn" @click="logout">Logout</v-btn>
    </v-app-bar>
    <v-navigation-drawer app v-if="auth.isLoggedIn">
      <v-list>
        <v-list-item prepend-icon="mdi-view-dashboard" title="Dashboard" to="/" />
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

function logout() {
  auth.logout()
  router.push('/login')
}
</script>
