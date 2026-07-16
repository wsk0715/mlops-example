<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="4" v-for="p in projectsStore.projects" :key="p.id">
        <v-card :title="p.name" :subtitle="p.description || 'No description'" @click="$router.push('/projects/' + p.id)" hover>
          <v-card-text>Team: {{ p.team_id }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-btn color="primary" @click="dialog = true" class="mt-4">New Project</v-btn>
    <v-dialog v-model="dialog" max-width="400">
      <v-card title="New Project">
        <v-card-text>
          <v-text-field v-model="name" label="Project name" />
          <v-btn @click="create" color="primary">Create</v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useProjectsStore } from '../stores/projects'

const projectsStore = useProjectsStore()
const dialog = ref(false)
const name = ref('')

onMounted(() => projectsStore.fetch())

async function create() {
  await projectsStore.create(name.value, '')
  dialog.value = false
  name.value = ''
}
</script>
