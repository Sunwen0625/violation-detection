<script setup lang="ts">
import BaseRecordTable from '@/components/ui/BaseRecordTable.vue'
import { useAppealStore } from '@/stores/appeal'

const appealStore = useAppealStore()
</script>

<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold text-white mb-4">申訴重審</h2>

    <BaseRecordTable :data="appealStore.appeals">
      <template #actions="{ item }">
        <div class="flex gap-2">
          <!-- 同意 -->
          <button
            @click="appealStore.approveAppeal(item)"
            class="px-3 py-1 rounded bg-green-600 hover:bg-green-500 text-white text-sm"
          >
            同意
          </button>

          <!-- 拒絕 -->
          <button
            @click="appealStore.rejectAppeal(item)"
            class="px-3 py-1 rounded bg-red-600 hover:bg-red-500 text-white text-sm"
          >
            不同意
          </button>
        </div>
      </template>
    </BaseRecordTable>
  </div>
</template>
