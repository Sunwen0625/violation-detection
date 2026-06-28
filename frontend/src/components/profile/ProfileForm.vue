<script setup lang="ts">
import CarList from '@/components/layout/CarList.vue'
defineProps<{
  form: {
    name: string
    email: string
    phone: string
    address: string
  }
  cars: {
    car_id: number
    license_plate: string
  }[]
}>()

defineEmits(['save', 'cancel', 'addLicense', 'removeLicense'])
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold text-white mb-6">編輯資料</h1>

    <div class="grid grid-cols-2 gap-4">
      <div>
        <p class="text-gray-400 text-sm">姓名</p>
        <input
          v-model="form.name"
          class="w-full px-3 py-2 rounded-lg bg-[#1f1f1f] border border-gray-600 text-white focus:border-blue-500"
        />
      </div>

      <div>
        <p class="text-gray-400 text-sm">Email</p>
        <input
          v-model="form.email"
          class="w-full px-3 py-2 rounded-lg bg-[#1f1f1f] border border-gray-600 text-white focus:border-blue-500"
        />
      </div>

      <div>
        <p class="text-gray-400 text-sm">電話</p>
        <input
          v-model="form.phone"
          class="w-full px-3 py-2 rounded-lg bg-[#1f1f1f] border border-gray-600 text-white focus:border-blue-500"
        />
      </div>

      <div>
        <p class="text-gray-400 text-sm">地址</p>
        <input
          v-model="form.address"
          class="w-full px-3 py-2 rounded-lg bg-[#1f1f1f] border border-gray-600 text-white focus:border-blue-500"
        />
      </div>
    </div>

    <!-- 車牌管理 -->
    <div>
      <p class="text-gray-400 text-sm mb-2 mt-4">車牌管理（選填）</p>
      <!-- 車牌列表垂直 -->
      <CarList
        :cars="cars"
        @add="$emit('addLicense', $event)"
        @delete="$emit('removeLicense', $event)"
      />
    </div>
  </div>

  <!-- 儲存按鈕 -->
  <div class="flex justify-end mt-6">
    <button
      @click="$emit('save')"
      class="px-5 py-2 rounded-xl bg-blue-500 hover:bg-blue-400 transition text-white font-semibold"
    >
      儲存
    </button>
  </div>
</template>
