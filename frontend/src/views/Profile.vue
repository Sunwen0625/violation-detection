<script setup lang="ts">
import { watch, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import UserProfilePage from '@/components/profile/UserProfile.vue'
import AdminProfile from '@/components/ui/AdminProfile.vue'
import { getUserByEmail, type UserProfile } from '@/api/user'

const auth = useAuthStore()

type Car = {
  car_id: number
  license_plate: string
}

const cars = ref<Car[]>([])
const user = ref<UserProfile>({
  name: '',
  email: '',
  phone: '',
  idNumber: '',
  address: '',
  avatar: '',
})

async function fetchUser() {
  try {
    const data = await getUserByEmail('123@example.com')
    console.log('API 回傳:', data)
    user.value = data
  } catch (error) {
    console.error('載入使用者失敗', error)
  }
}
async function fetchCars() {
  try {
    const res = await fetch(`/api/cars/1`) // 先寫死
    const data = await res.json()
    if (Array.isArray(data)) {
      cars.value = data
    } else {
      console.error('cars API 格式錯誤', data)
      cars.value = []
    }
  } catch (e) {
    console.error('載入車牌失敗', e)
  }
}

watch(
  () => auth.isUser,
  async (isUser) => {
    if (isUser) {
      await fetchUser()
      await fetchCars()
    }
  },
  { immediate: true },
)
</script>
<template>
  <!-- 一般使用者 -->
  <UserProfilePage v-if="auth.isUser" :user="user" :cars="cars" :avatar="user.avatar" />

  <!-- 管理員 -->
  <AdminProfile
    v-else-if="auth.isAdmin"
    :user="{
      name: auth.user?.name || '',
      adminId: 'ADM-001',
    }"
  />

  <!-- 訪客 -->
  <div v-else class="text-gray-400">請先登入</div>
</template>
