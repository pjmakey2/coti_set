import { createRouter, createWebHistory } from 'vue-router'
import ExchangeView from '../views/ExchangeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/Exchanges',
      name: 'exchanges',
      component: ExchangeView
    },
    {
      path: '/Suscribe',
      name: 'suscribe',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/ApiDocs',
      name: 'api_docs',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/ApiDocs.vue')
    }
    
  ]
})

export default router
