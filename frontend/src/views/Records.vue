<script setup lang="ts">
import { ref, onBeforeUnmount, onMounted } from 'vue'
import BaseRecordTable from '@/components/ui/BaseRecordTable.vue'

type CaseItem = {
  經緯度: { lat: number | null; lon: number | null }
  車牌: string
  照片: string
  時間: string
  完整路名: string
}

const REFRESH_INTERVAL_MS = 5000

const data = ref<CaseItem[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
let refreshTimer: ReturnType<typeof window.setInterval> | null = null

const fetchData = async () => {
  if (loading.value) return

  loading.value = true

  try {
    const res = await fetch(`/api/reports?_=${Date.now()}`, {
      cache: 'no-store',
    })

    if (!res.ok) {
      throw new Error('API Error')
    }

    const json = await res.json()

    data.value = json.map((item: any) => ({
      車牌: item.license_plate,

      時間: item.report_time,

      完整路名: item.full_address,

      經緯度: {
        lat: item.latitude,
        lon: item.longitude,
      },

      // 這裡改成後端圖片 API
      照片: `/api/reports/${item.report_id}/image`,
    }))

    error.value = null
  } catch (e) {
    console.error(e)
    error.value = '讀取失敗'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
  refreshTimer = window.setInterval(fetchData, REFRESH_INTERVAL_MS)
})

onBeforeUnmount(() => {
  if (refreshTimer) {
    window.clearInterval(refreshTimer)
  }
})
</script>

<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold text-white mb-4">檢舉歷史</h2>

    <BaseRecordTable :data="data" :loading="loading" :error="error" />
  </div>
</template>
