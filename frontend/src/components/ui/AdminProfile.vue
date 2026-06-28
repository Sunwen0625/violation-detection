<script setup lang="ts">
defineProps<{
  user: {
    name: string
    adminId: string
  }
}>()
</script>

<template>
  <div class="flex justify-center py-10">
    <div class="w-full max-w-3xl bg-[#2a2a2a] rounded-2xl shadow-lg p-8 text-gray-200">
      <!-- 標題 -->
      <h1 class="text-2xl font-bold text-white mb-6">使用者資料</h1>

      <!-- 上半部：頭像 + 基本資料 -->
      <div class="flex flex-col md:flex-row gap-8">
        <!-- 頭像 -->
        <div class="flex flex-col items-center gap-3">
          <div
            class="w-24 h-24 rounded-full overflow-hidden border-2 border-white bg-gray-500 flex items-center justify-center"
          >
            <img src="@/assets/user.png" alt="User Avatar" class="w-full h-full object-cover" />
          </div>

          <button class="text-sm text-blue-400 hover:underline">上傳頭像</button>
        </div>

        <div>
          <p class="text-gray-400 text-sm">管理員姓名</p>
          <p class="text-white font-semibold">{{ user.name }}</p>
        </div>

        <div>
          <p class="text-gray-400 text-sm">管理員編號</p>
          <p class="text-white font-semibold">{{ user.adminId }}</p>
        </div>
      </div>
      <!-- 分隔線 -->
      <div class="my-6 border-t border-gray-600"></div>
      <!-- 操作按鈕 -->
      <div class="flex justify-end gap-4">
        <button
          class="px-5 py-2 rounded-xl bg-yellow-600 hover:bg-yellow-500 transition text-white font-semibold"
        >
          編輯資料
        </button>

        <button
          class="px-5 py-2 rounded-xl bg-red-500 hover:bg-red-400 transition text-white font-semibold"
        >
          登出
        </button>
      </div>
    </div>
  </div>
</template>
