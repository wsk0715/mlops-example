import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/login', component: () => import('../views/LoginView.vue') },
  { path: '/register', component: () => import('../views/RegisterView.vue') },
  { path: '/', component: () => import('../views/DashboardView.vue'), meta: { requiresAuth: true } },
  { path: '/projects/:id', component: () => import('../views/ProjectDetailView.vue'), meta: { requiresAuth: true } },
  { path: '/projects/:id/datasets', component: () => import('../views/DatasetListView.vue'), meta: { requiresAuth: true } },
  { path: '/projects/:id/datasets/:did', component: () => import('../views/DatasetDetailView.vue'), meta: { requiresAuth: true } },
  { path: '/projects/:id/experiments', component: () => import('../views/ExperimentListView.vue'), meta: { requiresAuth: true } },
  { path: '/projects/:id/experiments/:eid', component: () => import('../views/ExperimentDetailView.vue'), meta: { requiresAuth: true } },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !token) next('/login')
  else next()
})

export default router
