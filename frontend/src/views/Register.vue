<template>
  <div class="flex items-center justify-center h-full">
    <div class="w-[360px] p-8 rounded-2xl shadow-lg text-center text-gray-200">
      <h2 class="text-2xl font-bold text-white mb-5">註冊</h2>

      <form @submit.prevent="handleRegister">
        <div class="mb-4 text-left">
          <label class="block mb-1.5 text-sm text-gray-400"> 使用者名稱 </label>
          <input
            type="text"
            v-model="form.username"
            required
            class="w-full px-3 py-2 rounded-lg border border-gray-600 bg-[#2a2a2a] text-white outline-none text-sm focus:border-orange-500 transition-colors"
          />
        </div>

        <div class="mb-4 text-left">
          <label class="block mb-1.5 text-sm text-gray-400"> 電子郵件 </label>
          <input
            type="email"
            v-model="form.email"
            required
            class="w-full px-3 py-2 rounded-lg border border-gray-600 bg-[#2a2a2a] text-white outline-none text-sm focus:border-orange-500 transition-colors"
          />
        </div>

        <div class="mb-4 text-left">
          <label class="block mb-1.5 text-sm text-gray-400"> 密碼 </label>
          <input
            type="password"
            v-model="form.password"
            required
            class="w-full px-3 py-2 rounded-lg border border-gray-600 bg-[#2a2a2a] text-white outline-none text-sm focus:border-orange-500 transition-colors"
          />
        </div>

        <button
          type="submit"
          class="mt-2 w-full py-3 rounded-xl bg-orange-500 text-white text-base font-semibold hover:bg-orange-400 hover:-translate-y-0.5 transition-all duration-300"
        >
          註冊
        </button>

        <p class="mt-4 text-sm text-gray-400">
          已經有帳號了嗎？
          <RouterLink to="/login" class="text-blue-500 font-semibold hover:underline">
            立即登入
          </RouterLink>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const form = ref({
  username: '',
  email: '',
  password: '',
})

const handleRegister = () => {
  console.log('註冊資料：', form.value)
  alert('註冊成功！🎉')
}
</script>
