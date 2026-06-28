<script setup lang="ts">
import { computed, ref, watch } from 'vue'

type CaseItem = {
  經緯度: { lat: number | null; lon: number | null }
  車牌: string
  照片: string
  時間: string
  完整路名: string
}

const props = defineProps<{
  data: CaseItem[]
  loading?: boolean
  error?: string | null
}>()

const PAGE_SIZE = 10
const currentPage = ref(1)

// 🔹 當資料變動，自動回到第一頁（重要 UX）
watch(
  () => props.data,
  () => {
    currentPage.value = 1
  },
)

const totalPages = computed(() => Math.max(1, Math.ceil(props.data.length / PAGE_SIZE)))

const paginated = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return props.data.slice(start, start + PAGE_SIZE)
})

const goToPage = (p: number) => {
  if (p >= 1 && p <= totalPages.value) currentPage.value = p
}

const formatTime = (iso: string) => {
  try {
    return new Date(iso).toLocaleString('zh-TW', { hour12: false })
  } catch {
    return iso
  }
}

const gmapUrl = (lat?: number | null, lon?: number | null) => {
  if (lat == null || lon == null) return null
  return `https://www.google.com/maps?q=${lat},${lon}`
}
// 🔹 圖片預覽邏輯
const previewVisible = ref(false)
const previewImage = ref('')

const openPreview = (url: string) => {
  previewImage.value = url
  previewVisible.value = true
}

const closePreview = () => {
  previewVisible.value = false
  previewImage.value = ''
}
</script>

<template>
  <div class="space-y-4">
    <!-- 狀態 -->
    <div v-if="error" class="p-3 rounded bg-red-900 text-red-200">
      {{ error }}
    </div>

    <div v-else>
      <div v-if="loading" class="mb-3 text-sm text-gray-300">資料更新中...</div>

      <!-- 表格 -->
      <div class="overflow-x-auto border border-gray-700 rounded-lg">
        <table class="min-w-full text-gray-200">
          <thead class="bg-gray-800 text-white">
            <tr>
              <th class="px-4 py-2 text-left">車牌</th>
              <th class="px-4 py-2 text-left">時間</th>
              <th class="px-4 py-2 text-left">完整路名</th>
              <th class="px-4 py-2 text-left">經緯度</th>
              <th class="px-4 py-2 text-left">照片</th>
              <th class="px-4 py-2 text-left">操作</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="(item, idx) in paginated"
              :key="idx"
              class="border-t border-gray-700 hover:bg-gray-700"
            >
              <td class="px-4 py-2">{{ item.車牌 }}</td>
              <td class="px-4 py-2">{{ formatTime(item.時間) }}</td>
              <td class="px-4 py-2">{{ item.完整路名 }}</td>

              <td class="px-4 py-2">
                <div v-if="item.經緯度?.lat != null">
                  {{ item.經緯度.lat }}, {{ item.經緯度.lon }}
                </div>
                <div v-else class="text-gray-400">—</div>
              </td>

              <td class="px-4 py-2">
                <img
                  v-if="item.照片"
                  :src="item.照片"
                  class="w-16 h-16 object-cover rounded cursor-pointer hover:scale-105 transition"
                  @click="openPreview(item.照片)"
                />
                <span v-else class="text-gray-400">無</span>
              </td>

              <td class="px-4 py-2">
                <slot name="actions" :item="item">
                  <!-- 預設行為 -->
                  <a
                    v-if="gmapUrl(item.經緯度?.lat, item.經緯度?.lon)"
                    :href="gmapUrl(item.經緯度.lat, item.經緯度.lon)!"
                    target="_blank"
                    class="px-3 py-1 rounded bg-blue-500 hover:bg-blue-400 text-white text-sm"
                  >
                    地圖
                  </a>
                </slot>
              </td>
            </tr>

            <tr v-if="paginated.length === 0">
              <td colspan="6" class="text-center py-6 text-gray-400">無資料</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分頁 -->
      <div class="flex justify-center gap-2 mt-4">
        <button @click="goToPage(1)" class="px-3 py-1 border rounded">‹‹</button>
        <button @click="goToPage(currentPage - 1)" class="px-3 py-1 border rounded">上一頁</button>

        <span class="px-3 py-1"> {{ currentPage }} / {{ totalPages }} </span>

        <button @click="goToPage(currentPage + 1)" class="px-3 py-1 border rounded">下一頁</button>
        <button @click="goToPage(totalPages)" class="px-3 py-1 border rounded">››</button>
      </div>
    </div>
  </div>
  <Teleport to="body">
    <div
      v-if="previewVisible"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/80"
      @click="closePreview"
    >
      <div class="relative max-w-5xl max-h-[90vh] p-4">
        <img
          :src="previewImage"
          class="max-w-full max-h-[85vh] rounded-xl shadow-2xl"
          @click.stop
        />

        <button
          class="absolute top-2 right-2 bg-white text-black px-3 py-1 rounded-full"
          @click="closePreview"
        >
          ✕
        </button>
      </div>
    </div>
  </Teleport>
</template>
