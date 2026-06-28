<script lang="ts" setup>
import { RouterLink } from 'vue-router'

interface Props {
  to: string
  color?: 'blue' | 'orange'
}

const props = withDefaults(defineProps<Props>(), {
  color: 'blue',
})

const colorClass = {
  blue: 'bg-blue-500 hover:bg-blue-400',
  orange: 'bg-orange-500 hover:bg-orange-400',
}
</script>

<template>
  <RouterLink
    :to="to"
    :class="[
      'flex items-center gap-1.5 px-5 py-2 rounded-xl font-semibold text-white',
      'hover:-translate-y-0.5 transition-all duration-300',
      colorClass[color],
    ]"
  >
    <slot />
  </RouterLink>
</template>
