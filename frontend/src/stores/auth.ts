import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export type Role = 'guest' | 'user' | 'admin'

interface User {
  name: string
  avatar?: string
}

export const useAuthStore = defineStore('auth', () => {
  // 🔹 state
  const role = ref<Role>('guest')
  const user = ref<User | null>(null)

  // 🔹 getters（可讀性提升）
  const isGuest = computed(() => role.value === 'guest')
  const isUser = computed(() => role.value === 'user')
  const isAdmin = computed(() => role.value === 'admin')

  // 🔹 actions
  function loginAsUser(userData: User) {
    role.value = 'user'
    user.value = userData
  }

  function loginAsAdmin(userData: User) {
    role.value = 'admin'
    user.value = userData
  }

  function updateAvatar(avatar: string) {
    if (!user.value) return
    user.value.avatar = avatar
  }

  function logout() {
    role.value = 'guest'
    user.value = null
  }

  function setRoleDebug(newRole: Role) {
    role.value = newRole

    // 模擬不同身份資料
    if (newRole === 'guest') {
      user.value = null
    } else if (newRole === 'user') {
      user.value = { name: '測試使用者' }
    } else if (newRole === 'admin') {
      user.value = { name: '管理員' }
    }
  }

  return {
    role,
    user,
    isGuest,
    isUser,
    isAdmin,
    loginAsUser,
    loginAsAdmin,
    updateAvatar,
    logout,
    setRoleDebug, // 新增的調試方法
  }
})
