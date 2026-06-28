<script lang="ts" setup>
import { computed } from 'vue'

interface Props {
  name: string
  avatar?: string
}

const props = defineProps<Props>()

// 如果沒有頭像，顯示預設（例如用名字首字）
const initial = computed(() => props.name.charAt(0).toUpperCase())
</script>

<template>
  <div class="flex items-center gap-3 mx-5 cursor-pointer">
    <!-- 頭像 -->
    <div
      class="w-10 h-10 rounded-full overflow-hidden border-2 border-white bg-gray-400 flex items-center justify-center text-white font-bold"
    >
      <img v-if="avatar" :src="avatar" alt="avatar" class="w-full h-full object-cover" />
      <span v-else>{{ initial }}</span>
    </div>

    <!-- 名字 -->
    <span class="text-white font-semibold">
      {{ name }}
    </span>
  </div>
</template>
