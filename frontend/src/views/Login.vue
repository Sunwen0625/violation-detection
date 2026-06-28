<template>
  <div class="flex justify-center items-center h-full">
    <div class="w-[360px] p-8 rounded-2xl shadow-lg text-center text-gray-200">
      <h2 class="text-2xl font-bold text-white mb-5">登入</h2>

      <form @submit.prevent="handleLogin">
        <!-- Email -->
        <div class="mb-4 text-left">
          <label class="block mb-1.5 text-sm text-gray-400"> 電子郵件 </label>
          <input
            type="email"
            v-model="form.email"
            required
            class="w-full px-3 py-2 rounded-lg border border-gray-600 bg-[#2a2a2a] text-white outline-none text-sm focus:border-blue-500"
          />
        </div>

        <!-- Password -->
        <div class="mb-4 text-left">
          <label class="block mb-1.5 text-sm text-gray-400"> 密碼 </label>
          <input
            type="password"
            v-model="form.password"
            required
            class="w-full px-3 py-2 rounded-lg border border-gray-600 bg-[#2a2a2a] text-white outline-none text-sm focus:border-blue-500"
          />
        </div>

        <!-- Button -->
        <button
          type="submit"
          class="mt-2 w-full py-3 rounded-xl bg-blue-500 text-white text-base font-semibold hover:bg-blue-400 hover:-translate-y-0.5 transition-all duration-300"
        >
          登入
        </button>

        <!-- Register -->
        <p class="mt-4 text-sm text-gray-400">
          還沒有帳號嗎？
          <RouterLink to="/register" class="text-orange-500 font-semibold hover:underline">
            立即註冊
          </RouterLink>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const form = ref({
  email: '',
  password: '',
})

const handleLogin = () => {
  console.log('登入資料：', form.value)

  // 🔹 模擬登入邏輯（之後換 API）
  if (form.value.email === 'admin@test.com') {
    auth.loginAsAdmin({
      name: 'Admin',
    })
  } else {
    auth.loginAsUser({
      name: 'User',
    })
  }

  // 🔹 導回首頁（Navbar 會自動更新）
  router.push('/profile')
}
</script>
