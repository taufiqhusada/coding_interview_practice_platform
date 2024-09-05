
<template>
  <Header></Header>
  <div class="container">
    <Example></Example>
  </div>
  <Footer></Footer>

</template>

<script lang="ts">
import Example from '@/components/Example.vue';
import Header from '@/components/TheHeader.vue';
import Footer from '@/components/TheFooter.vue';

export default {
  components: {
    Example,
    Header,
    Footer
  }
  
};
</script>

<style scoped>

</style>
