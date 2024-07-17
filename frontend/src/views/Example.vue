
<template>
  <Header></Header>
  <div class="container">
    <ChatboxExample></ChatboxExample>
  </div>
  <Footer></Footer>

</template>

<script lang="ts">
import ChatboxExample from '@/components/ChatboxExample.vue';
import Header from '@/components/TheHeader.vue';
import Footer from '@/components/TheFooter.vue';

export default {
  components: {
    ChatboxExample,
    Header,
    Footer
  }
  
};
</script>

<style scoped>

</style>
