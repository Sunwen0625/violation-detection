<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { sidebarConfig } from '@/config/sidebar'

const auth = useAuthStore()

// 🔹 根據角色取得 menu
const menuItems = computed(() => {
  return sidebarConfig[auth.role] || []
})
</script>

<template>
  <aside
    class="sticky top-0 self-start h-screen w-64 flex-shrink-0 overflow-y-auto bg-[#2b2a2a] px-3 py-4"
  >
    <nav class="flex flex-col gap-2">
      <!-- 主選單 -->
      <template v-for="item in menuItems" :key="item.name">
        <!-- 沒有 children -->
        <RouterLink
          v-if="!item.children"
          :to="item.path!"
          class="block px-3 py-2.5 rounded-lg text-white transition hover:bg-[#3a3a3a]"
          active-class="bg-[#424242] font-semibold"
        >
          {{ item.name }}
        </RouterLink>

        <!-- 有 children（子選單） -->
        <div v-else>
          <p class="px-3 py-2 text-gray-400 text-sm">
            {{ item.name }}
          </p>

          <RouterLink
            v-for="child in item.children"
            :key="child.path"
            :to="child.path!"
            class="block ml-3 px-3 py-2 rounded-lg text-white text-sm transition hover:bg-[#3a3a3a]"
            active-class="bg-[#424242] font-semibold"
          >
            {{ child.name }}
          </RouterLink>
        </div>
      </template>
    </nav>
  </aside>
</template>
