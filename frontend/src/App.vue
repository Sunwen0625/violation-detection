<script setup lang="ts">
import { RouterView } from 'vue-router'
import HeaderView from './components/layout/HeaderView.vue'
import Sidebar from './components/layout/Sidebar.vue'
import DevRoleSwitcher from '@/components/DevRoleSwitcher.vue'
import { useLayout } from '@/components/useLayout'

const isDev = import.meta.env.DEV
const { showSidebar, layoutClass } = useLayout()
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <!-- Header -->
    <HeaderView />

    <!-- 主區塊 -->
    <div class="flex-1" :class="layoutClass">
      <!-- Sidebar -->
      <Sidebar v-if="showSidebar" class="h-full" />

      <!-- 內容 -->
      <section class="p-5 bg-black flex justify-center items-center overflow-auto flex-1">
        <RouterView />
        <DevRoleSwitcher v-if="isDev" />
      </section>
    </div>
  </div>
</template>
