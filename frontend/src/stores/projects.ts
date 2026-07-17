import { defineStore } from 'pinia'
import api from '../api/client'

export const useProjectsStore = defineStore('projects', {
  state: () => ({ projects: [] as any[], current: null as any }),
  actions: {
    async fetch() {
      const { data } = await api.get('/projects')
      this.projects = data.items
    },
    async create(name: string, description: string, team_id?: string) {
      const { data } = await api.post('/projects', { name, description })
      this.projects.push(data)
    },
    async getById(id: string) {
      const { data } = await api.get(`/projects/${id}`)
      this.current = data
    },
  },
})
