import { type RouteRecordRaw, createRouter, createWebHistory } from 'vue-router';
import Main from '@/views/Main.vue';
import Example from '@/views/Example.vue';

const routes = [
  {
    path: '/example',
    name: 'Example',
    component: Example,
  },
  {
    path: '/',
    name: 'Main',
    component: Main,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;