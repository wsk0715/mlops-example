import { defineStore } from 'pinia'
import api from '../api/client'

export const useDatasetsStore = defineStore('datasets', {
  state: () => ({ datasets: [] as any[], current: null as any, versions: [] as any[] }),
  actions: {
    async fetch(projectId: string) {
      const { data } = await api.get('/datasets', { params: { project_id: projectId } })
      this.datasets = data.items
    },
    async upload(formData: FormData) {
      const { data } = await api.post('/datasets', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      this.datasets.push(data)
    },
    async getById(id: string) {
      const { data } = await api.get(`/datasets/${id}`)
      this.current = data
    },
    async fetchVersions(id: string) {
      const { data } = await api.get(`/datasets/${id}/versions`)
      this.versions = data.items
    },
  },
})
