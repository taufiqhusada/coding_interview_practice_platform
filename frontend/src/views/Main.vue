<template>
  <Header></Header>
  <div class="container">
    <Simulation></Simulation>
  </div>
  <!-- <Footer></Footer> -->

</template>

<script lang="ts">
import Simulation from '@/components/Simulation.vue';
import Header from '@/components/TheHeader.vue';
import Footer from '@/components/TheFooter.vue';

export default {
  components: {
    Simulation,
    Header,
    Footer
  }
  
};
</script>

<style scoped>

</style>
