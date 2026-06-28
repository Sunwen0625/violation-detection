<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<template>
  <div class="fixed bottom-4 right-4 bg-black/80 text-white p-3 rounded-lg shadow-lg z-50">
    <p class="text-sm mb-2">Dev Role Switch</p>

    <div class="flex gap-2">
      <button class="px-2 py-1 bg-gray-600 rounded" @click="auth.setRoleDebug('guest')">
        guest
      </button>

      <button class="px-2 py-1 bg-blue-600 rounded" @click="auth.setRoleDebug('user')">user</button>

      <button class="px-2 py-1 bg-purple-600 rounded" @click="auth.setRoleDebug('admin')">
        admin
      </button>
    </div>
  </div>
</template>
