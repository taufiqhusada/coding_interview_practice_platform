<template>
    <div class="loader"></div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'LoaderSimple'
});
</script>

<style scoped>
.loader {
    width: 15px;
    aspect-ratio: 1;
    border-radius: 50%;
    animation: l5 1s infinite linear alternate;
}

@keyframes l5 {
    0% {
        box-shadow: 20px 0 #000, -20px 0 #0002;
        background: #000
    }

    33% {
        box-shadow: 20px 0 #000, -20px 0 #0002;
        background: #0002
    }

    66% {
        box-shadow: 20px 0 #0002, -20px 0 #000;
        background: #0002
    }

    100% {
        box-shadow: 20px 0 #0002, -20px 0 #000;
        background: #000
    }
}
</style>