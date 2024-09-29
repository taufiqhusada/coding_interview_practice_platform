import { type RouteRecordRaw, createRouter, createWebHistory } from 'vue-router';
import Main from '@/views/Main.vue';
import Example from '@/views/Example.vue';
import Feedback from '@/views/Feedback.vue';
import GranularSimulation from '@/views/GranularSimulation.vue'

const routes = [
  {
    path: '/example',
    name: 'Example',
    component: Example,
  },
  {
    path: '/feedback',
    name: 'Feedback',
    component: Feedback,
  },
  {
    path: '/guidedSimulation',
    name: 'GranularSimulation',
    component: GranularSimulation,
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