import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

const routes = [
  { path: '/', component: () => import('../views/LoginView.vue') },
  { path: '/cars', component: () => import('../views/CarsView.vue'), meta: {requireLogin: true} },
  {path: '/:pathMatch(.*)*', redirect: "/"}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({ path: '/'});
  } else {
    next()
  }
})

export default router
