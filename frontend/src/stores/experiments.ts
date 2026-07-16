import { defineStore } from 'pinia'
import api from '../api/client'

export const useExperimentsStore = defineStore('experiments', {
  state: () => ({ experiments: [] as any[], current: null as any }),
  actions: {
    async fetch(projectId: string, status?: string) {
      const params: any = { project_id: projectId }
      if (status) params.status = status
      const { data } = await api.get('/experiments', { params })
      this.experiments = data.items
    },
    async create(projectId: string, name: string, params: Record<string, string> = {}) {
      const { data } = await api.post('/experiments', { project_id: projectId, name, params })
      this.experiments.push(data)
      return data
    },
    async getById(id: string) {
      const { data } = await api.get(`/experiments/${id}`)
      this.current = data
    },
    async updateStatus(id: string, status: string) {
      await api.put(`/experiments/${id}`, { status })
    },
  },
})
