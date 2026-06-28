<script lang="ts" setup>
import { RouterLink } from 'vue-router'
import { Icon } from '@iconify/vue'

import logo from '@/assets/logo.jpg'
import AuthButton from '@/components/ui/AuthButton.vue'
import UserMenu from '@/components/UserMenu.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<template>
  <header class="flex items-center justify-between bg-[#303030]">
    <RouterLink
      to="/"
      class="flex items-center flex-grow text-2xl font-bold text-white px-5 py-[10px] gap-3"
    >
      <img
        :src="logo"
        alt="Logo"
        class="w-10 h-10 object-cover rounded-[25%] border-2 border-white"
      />
      <span>違規停車系統</span>
    </RouterLink>

    <!-- 右邊 -->
    <div class="flex items-center">
      <!-- 1️⃣ 訪客 -->
      <div v-if="auth.isGuest" class="flex gap-3">
        <AuthButton to="/login" color="blue">
          <Icon icon="ic:baseline-log-in" width="20" />
          <span>登入</span>
        </AuthButton>

        <AuthButton to="/register" color="orange">
          <Icon icon="mdi:account-plus" width="20" />
          <span>註冊</span>
        </AuthButton>
      </div>

      <!-- 2️⃣ 一般使用者 -->
      <div v-else-if="auth.isUser" class="flex items-center gap-4">
        <UserMenu :name="auth.user?.name || ''" :avatar="auth.user?.avatar" />
      </div>

      <!-- 3️⃣ 管理者 -->
      <div v-else-if="auth.isAdmin" class="flex items-center gap-4">
        <!-- 管理功能入口 -->
        <RouterLink
          to="/admin"
          class="text-white font-semibold px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-500 transition"
        >
          管理後台
        </RouterLink>

        <!-- 使用者資訊 -->
        <UserMenu :name="auth.user?.name || ''" :avatar="auth.user?.avatar" />
      </div>
    </div>
  </header>
</template>
