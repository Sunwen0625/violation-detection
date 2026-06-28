<script setup lang="ts">
import { toRef } from 'vue'
import ProfileView from '@/components/profile/ProfileView.vue'
import ProfileForm from '@/components/profile/ProfileForm.vue'
import { useProfile } from '@/composables/useProfile'

const props = defineProps<{
  user: {
    name: string
    email: string
    phone: string
    idNumber: string
    address: string
    avatar?: string
  }
  cars: {
    car_id: number
    license_plate: string
  }[]
}>()

const userRef = toRef(props, 'user')
const carsRef = toRef(props, 'cars')
const {
  isEditing,
  form,
  cars,
  avatar,
  handleAvatarUpload,
  toggleEdit,
  saveProfile,
  addLicense,
  removeLicense,
} = useProfile(userRef, carsRef)
</script>

<template>
  <div class="flex justify-center py-10">
    <div class="w-full max-w-3xl bg-[#2a2a2a] rounded-2xl p-8">
      <ProfileView
        v-if="!isEditing"
        :user="user"
        :cars="cars"
        :avatar="avatar"
        @edit="toggleEdit"
        @uploadAvatar="handleAvatarUpload"
      />

      <ProfileForm
        v-else
        :form="form"
        :cars="cars"
        @save="saveProfile"
        @cancel="toggleEdit"
        @addLicense="addLicense"
        @removeLicense="removeLicense"
      />
    </div>
  </div>
</template>
