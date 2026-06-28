<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  cars: { car_id: number; license_plate: string }[]
}>()

const emit = defineEmits<{
  (e: 'add', plate: string): void
  (e: 'delete', carId: number): void
}>()

const handleAdd = () => {
  if (!newPlate.value.trim()) return

  emit('add', newPlate.value)
  newPlate.value = ''
}

const newPlate = ref('')
</script>

<template>
  <div class="space-y-4">
    <!-- 新增 -->
    <div class="flex gap-2">
      <input v-model="newPlate" class="border px-3 py-2 rounded w-full" />
      <button @click="handleAdd()" class="bg-green-600 text-white px-4 py-2 rounded">＋</button>
    </div>

    <!-- 列表 -->
    <div v-for="car in cars" :key="car.car_id" class="flex justify-between border p-2 rounded">
      <span>{{ car.license_plate }}</span>
      <button @click="emit('delete', car.car_id)" class="text-red-500">刪除</button>
    </div>
  </div>
</template>
