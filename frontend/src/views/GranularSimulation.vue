<template>
    <Header :currentPage="'guidedPractice'"></Header>
    <div class="container">
      <GranularSimulation></GranularSimulation>
    </div>
    <!-- <Footer></Footer> -->
  
  </template>
  
  <script lang="ts">
  import GranularSimulation from '@/components/GranularSimulation.vue';
  import Header from '@/components/TheHeader.vue';
  import Footer from '@/components/TheFooter.vue';
  
  export default {
    components: {
      GranularSimulation,
      Header,
      Footer
    }
    
  };
  </script>
  
  <style scoped>
  
  </style>
  