<template>
  <!-- <TheHeader></TheHeader> -->
    <router-view />
  <!-- <TheFooter></TheFooter> -->
</template>

<script lang="ts">
import TheHeader from '@/components/TheHeader.vue';
import TheFooter from '@/components/TheFooter.vue';

export default {
  components: {
    TheHeader,
    TheFooter,
  }
  
};
</script>

<style>

</style>
