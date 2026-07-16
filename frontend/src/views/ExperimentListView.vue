<template>
  <v-container>
    <v-btn @click="dialog = true" color="primary" class="mb-4">New Experiment</v-btn>
    <v-table>
      <thead><tr><th>Name</th><th>Status</th><th>Created</th></tr></thead>
      <tbody>
        <tr v-for="e in experimentsStore.experiments" :key="e.id"
            @click="$router.push('/projects/' + projectId + '/experiments/' + e.id)"
            style="cursor:pointer">
          <td>{{ e.name }}</td>
          <td><v-chip :color="statusColor(e.status)" size="small">{{ e.status }}</v-chip></td>
          <td>{{ e.created_at?.slice(0, 10) }}</td>
        </tr>
      </tbody>
    </v-table>
    <v-dialog v-model="dialog" max-width="400">
      <v-card title="New Experiment">
        <v-card-text>
          <v-text-field v-model="name" label="Name" />
          <v-btn @click="create" color="primary">Create</v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useExperimentsStore } from '../stores/experiments'

const props = defineProps<{ projectId: string }>()
const experimentsStore = useExperimentsStore()
const dialog = ref(false)
const name = ref('')

onMounted(() => experimentsStore.fetch(props.projectId))

async function create() {
  await experimentsStore.create(props.projectId, name.value)
  dialog.value = false
  name.value = ''
}

function statusColor(s: string) {
  const m: Record<string, string> = { created: 'grey', running: 'blue', completed: 'green', failed: 'red' }
  return m[s] || 'grey'
}
</script>
