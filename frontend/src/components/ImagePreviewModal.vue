<script setup lang="ts">
defineProps<{
  visible: boolean
  imageUrl: string
}>()

const emit = defineEmits<{
  close: []
}>()
</script>

<template>
  <Teleport to="body">
    <div
      v-if="visible"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/80"
      @click="emit('close')"
    >
      <div class="relative max-w-5xl max-h-[90vh] p-4">
        <img :src="imageUrl" class="max-h-[85vh] max-w-full rounded-xl shadow-2xl" @click.stop />

        <button
          class="absolute right-2 top-2 rounded-full bg-white px-3 py-1 text-sm"
          @click="emit('close')"
        >
          ✕
        </button>
      </div>
    </div>
  </Teleport>
</template>
