<script setup lang="ts">
import MapTaiwan from '@/features/MapTaiwan.vue'
</script>

<template>
  <section class="w-full">
    <div class="text-3xl font-bold text-center mb-4">台灣違規車輛統計</div>

    <MapTaiwan url="/data/cases.json" :circleRadius="150" :maxClusterZoom="12" />
  </section>
</template>
