import { createRouter, createWebHistory } from 'vue-router'
// 匯入頁面
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Profile from '@/views/Profile.vue'
import Report from '@/views/Report.vue'
import Records from '@/views/Records.vue'
import Appeals from '@/views/Appeals.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login, meta: { hideNav: true } },
  { path: '/register', name: 'Register', component: Register, meta: { hideNav: true } },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/report', name: 'Report', component: Report },
  { path: '/records', name: 'Records', component: Records },
  { path: '/appeals', name: 'Appeals', component: Appeals },
  { path: '/map', name: 'Map', component: () => import('@/views/MapView.vue') }, // 使用 lazy loading
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
