<template>
  <v-container v-if="ds">
    <h2>{{ ds.name }}</h2>
    <v-card class="mb-4">
      <v-card-text>
        <div>Classes: {{ ds.class_names?.join(', ') }}</div>
        <div>Created: {{ ds.created_at?.slice(0, 10) }}</div>
      </v-card-text>
    </v-card>
    <h3>Versions</h3>
    <v-table>
      <thead><tr><th>Version</th><th>Images</th><th>Format</th><th>Download</th></tr></thead>
      <tbody>
        <tr v-for="v in datasetsStore.versions" :key="v.id">
          <td>v{{ v.version }}</td>
          <td>{{ v.image_count }}</td>
          <td>{{ v.annotation_format }}</td>
          <td><v-btn size="small" @click="download(v.id)">Download</v-btn></td>
        </tr>
      </tbody>
    </v-table>
  </v-container>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useDatasetsStore } from '../stores/datasets'
import api from '../api/client'

const route = useRoute()
const datasetsStore = useDatasetsStore()
const ds = computed(() => datasetsStore.current)

onMounted(async () => {
  await datasetsStore.getById(route.params.did as string)
  await datasetsStore.fetchVersions(route.params.did as string)
})

async function download(vId: string) {
  const { data } = await api.get(`/datasets/${route.params.did}/versions/${vId}/download`)
  window.open(data.signed_url, '_blank')
}
</script>
