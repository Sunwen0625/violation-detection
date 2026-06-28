<script setup lang="ts">
defineProps<{
  user: {
    name: string
    email: string
    phone: string
    idNumber: string
    address: string
  }
  cars: {
    car_id: number
    license_plate: string
  }[]
  avatar: string
}>()
defineEmits(['edit', 'uploadAvatar'])
</script>

<template>
  <div class="flex justify-center py-10">
    <div class="w-full max-w-3xl p-8 text-gray-200">
      <!-- 標題 -->
      <h1 class="text-2xl font-bold text-white mb-6">使用者資料</h1>

      <!-- 上半部：頭像 + 基本資料 -->
      <div class="flex flex-col md:flex-row gap-8">
        <!-- 頭像 -->
        <div class="flex flex-col items-center gap-3">
          <div
            class="w-24 h-24 rounded-full overflow-hidden border-2 border-white bg-gray-500 flex items-center justify-center"
          >
            <img :src="avatar" alt="User Avatar" class="w-full h-full object-cover" />
          </div>

          <label class="text-sm text-blue-400 hover:underline cursor-pointer">
            上傳頭像
            <input
              type="file"
              accept="image/*"
              class="hidden"
              @change="$emit('uploadAvatar', $event)"
            />
          </label>
        </div>

        <!-- 基本資訊 -->
        <div class="flex-1 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p class="text-gray-400 text-sm">使用者名稱</p>
            <p class="text-white font-semibold">{{ user.name }}</p>
          </div>

          <div>
            <p class="text-gray-400 text-sm">電子郵件</p>
            <p class="text-white font-semibold">{{ user.email }}</p>
          </div>

          <div>
            <p class="text-gray-400 text-sm">電話號碼</p>
            <p class="text-white font-semibold">{{ user.phone }}</p>
          </div>

          <div>
            <p class="text-gray-400 text-sm">身分證號碼</p>
            <p class="text-white font-semibold">{{ user.idNumber }}</p>
          </div>

          <div class="md:col-span-2">
            <p class="text-gray-400 text-sm">地址</p>
            <p class="text-white font-semibold">{{ user.address }}</p>
          </div>
        </div>
      </div>

      <!-- 分隔線 -->
      <div class="my-6 border-t border-gray-600"></div>

      <!-- 車牌管理 -->
      <div>
        <h2 class="text-lg font-semibold text-white mb-3">車牌管理（選填）</h2>

        <div class="space-y-3">
          <!-- 單一車牌 -->
          <div class="flex flex-col gap-3">
            <div v-for="car in cars" :key="car.car_id">* {{ car.license_plate }}</div>
          </div>
        </div>
      </div>

      <!-- 分隔線 -->
      <div class="my-6 border-t border-gray-600"></div>

      <!-- 操作按鈕 -->
      <div class="flex justify-end gap-4">
        <button
          @click="$emit('edit')"
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
