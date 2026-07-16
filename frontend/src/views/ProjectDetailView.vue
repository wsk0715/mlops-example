<template>
  <v-container>
    <h2 v-if="projectsStore.current">{{ projectsStore.current.name }}</h2>
    <v-tabs v-model="tab">
      <v-tab value="datasets">Datasets</v-tab>
      <v-tab value="experiments">Experiments</v-tab>
    </v-tabs>
    <v-tabs-window v-model="tab">
      <v-tabs-window-item value="datasets">
        <DatasetListView :projectId="projectId" />
      </v-tabs-window-item>
      <v-tabs-window-item value="experiments">
        <ExperimentListView :projectId="projectId" />
      </v-tabs-window-item>
    </v-tabs-window>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useProjectsStore } from '../stores/projects'
import DatasetListView from './DatasetListView.vue'
import ExperimentListView from './ExperimentListView.vue'

const route = useRoute()
const projectsStore = useProjectsStore()
const projectId = route.params.id as string
const tab = ref('datasets')

onMounted(() => projectsStore.getById(projectId))
</script>
