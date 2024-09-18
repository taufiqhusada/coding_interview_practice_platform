
<template>
    <Header :currentPage="'feedback'"></Header>
    <div class="container">
      <Feedback></Feedback>
    </div>
    <Footer></Footer>
  
  </template>
  
  <script lang="ts">
  import Example from '@/components/Feedback.vue';
  import Header from '@/components/TheHeader.vue';
  import Footer from '@/components/TheFooter.vue';

  import Feedback from '@/components/Feedback.vue'
  
  export default {
    components: {
      Example,
      Header,
      Footer,
      Feedback,
    }
    
  };
  </script>
  
  <style scoped>
  
  </style>
  