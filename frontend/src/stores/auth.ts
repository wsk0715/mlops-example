import { defineStore } from 'pinia'
import api from '../api/client'

interface User { id: string; username: string; is_active: boolean; created_at: string }

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    accessToken: localStorage.getItem('access_token') || '',
  }),
  getters: {
    isLoggedIn: (s) => !!s.accessToken,
  },
  actions: {
    async login(username: string, password: string) {
      const { data } = await api.post('/auth/login', { username, password })
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      this.accessToken = data.access_token
    },
    async register(username: string, password: string) {
      await api.post('/auth/register', { username, password })
    },
    async fetchUser() {
      const { data } = await api.get('/users/me')
      this.user = data
    },
    logout() {
      localStorage.clear()
      this.user = null
      this.accessToken = ''
    },
  },
})
