<template>
    <div class="loader-container">
      <div class="loader mt-5 pt-5">
        <div class="circle"></div>
        <div class="circle"></div>
        <div class="circle"></div>
        <div class="circle"></div>
      </div>
      <p class="loading-text mt-3 pt-3">Loading...</p>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  
  export default defineComponent({
    name: 'Loader'
  });
  </script>
  
  <style scoped>
  .loader-container {
    text-align: center;
    margin-top: 20px; /* Adjust as needed to place it below the video */
  }
  
  .loader {
    --dim: 3rem;
    width: var(--dim);
    height: var(--dim);
    position: relative;
    animation: spin988 2s linear infinite;
    display: inline-block;
  }
  
  .loader .circle {
    --color: #333;
    --dim: 1.2rem;
    width: var(--dim);
    height: var(--dim);
    background-color: var(--color);
    border-radius: 50%;
    position: absolute;
  }
  
  .loader .circle:nth-child(1) {
    top: 0;
    left: 0;
  }
  
  .loader .circle:nth-child(2) {
    top: 0;
    right: 0;
  }
  
  .loader .circle:nth-child(3) {
    bottom: 0;
    left: 0;
  }
  
  .loader .circle:nth-child(4) {
    bottom: 0;
    right: 0;
  }
  
  @keyframes spin988 {
    0% {
      transform: scale(1) rotate(0);
    }
  
    20%, 25% {
      transform: scale(1.3) rotate(90deg);
    }
  
    45%, 50% {
      transform: scale(1) rotate(180deg);
    }
  
    70%, 75% {
      transform: scale(1.3) rotate(270deg);
    }
  
    95%, 100% {
      transform: scale(1) rotate(360deg);
    }
  }
  .loading-text {
    font-style: italic;
  }
  </style>
  