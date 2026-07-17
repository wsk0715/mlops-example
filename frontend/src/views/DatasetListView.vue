<template>
  <v-container>
    <v-btn @click="dialog = true" color="primary" class="mb-4">Upload Dataset</v-btn>
    <v-table>
      <thead>
        <tr><th>Name</th><th>Classes</th><th>Created</th></tr>
      </thead>
      <tbody>
        <tr v-for="ds in datasetsStore.datasets" :key="ds.id"
            @click="$router.push('/projects/' + projectId + '/datasets/' + ds.id)"
            style="cursor:pointer">
          <td>{{ ds.name }}</td>
          <td>{{ ds.class_names?.join(', ') }}</td>
          <td>{{ ds.created_at?.slice(0, 10) }}</td>
        </tr>
      </tbody>
    </v-table>
    <v-dialog v-model="dialog" max-width="500">
      <v-card title="Upload Dataset">
        <v-card-text>
          <v-text-field v-model="name" label="Dataset name" placeholder="e.g. chess-pieces" />
          <v-text-field v-model="version" label="Version" placeholder="v1" />
          <v-text-field v-model="classNames" label="Classes (comma separated)" placeholder="king,queen,bishop,knight,rook,pawn" />
          <v-file-input v-model="files" label="ZIP file" accept=".zip" />
          <v-btn @click="upload" color="primary">Upload</v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useDatasetsStore } from '../stores/datasets'

const props = defineProps<{ projectId: string }>()
const datasetsStore = useDatasetsStore()
const dialog = ref(false)
const name = ref('')
const version = ref('v1')
const classNames = ref('')
const files = ref<File | null>(null)

onMounted(() => datasetsStore.fetch(props.projectId))

async function upload() {
  const fd = new FormData()
  fd.append('name', name.value)
  fd.append('project_id', props.projectId)
  fd.append('version', version.value)
  fd.append('class_names', classNames.value)
  if (files.value) fd.append('files', files.value)
  await datasetsStore.upload(fd)
  dialog.value = false
  name.value = ''
  version.value = 'v1'
  classNames.value = ''
}
</script>
