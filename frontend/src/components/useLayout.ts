import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

export function useLayout() {
  const auth = useAuthStore()

  // 🔹 是否顯示 sidebar
  const showSidebar = computed(() => {
    return !auth.isGuest
  })

  // 🔹 layout class（控制 grid / flex）
  const layoutClass = computed(() => {
    return showSidebar.value ? 'grid grid-cols-[240px_1fr]' : 'flex'
  })

  return {
    showSidebar,
    layoutClass,
  }
}
