<template>
  <v-container v-if="exp">
    <v-card class="mb-4">
      <v-card-title>{{ exp.name }}</v-card-title>
      <v-card-text>
        <v-chip :color="statusColor(exp.status)" class="mb-2">{{ exp.status }}</v-chip>
      </v-card-text>
      <v-card-actions v-if="exp.status === 'created'">
        <v-btn color="blue" @click="updateStatus('running')">Start Training</v-btn>
      </v-card-actions>
      <v-card-actions v-if="exp.status === 'running'">
        <v-btn color="green" @click="updateStatus('completed')">Complete</v-btn>
        <v-btn color="red" @click="updateStatus('failed')">Fail</v-btn>
      </v-card-actions>
    </v-card>
    <h3>Parameters</h3>
    <v-table>
      <thead><tr><th>Key</th><th>Value</th></tr></thead>
      <tbody>
        <tr v-for="(v, k) in exp.params" :key="k"><td>{{ k }}</td><td>{{ v }}</td></tr>
      </tbody>
    </v-table>
  </v-container>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useExperimentsStore } from '../stores/experiments'

const route = useRoute()
const experimentsStore = useExperimentsStore()
const exp = computed(() => experimentsStore.current)

onMounted(() => experimentsStore.getById(route.params.eid as string))

async function updateStatus(status: string) {
  await experimentsStore.updateStatus(route.params.eid as string, status)
  await experimentsStore.getById(route.params.eid as string)
}

function statusColor(s: string) {
  const m: Record<string, string> = { created: 'grey', running: 'blue', completed: 'green', failed: 'red' }
  return m[s] || 'grey'
}
</script>
