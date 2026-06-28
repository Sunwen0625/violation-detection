import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface CaseItem {
  經緯度: { lat: number | null; lon: number | null }
  車牌: string
  照片: string
  時間: string
  完整路名: string
}

export const useAppealStore = defineStore('appeal', () => {
  const appeals = ref<CaseItem[]>([])

  // 🔹 發起申訴
  const submitAppeal = (caseItem: CaseItem) => {
    // 避免重複申訴
    const exists = appeals.value.find((c) => c.時間 === caseItem.時間 && c.車牌 === caseItem.車牌)
    if (!exists) {
      appeals.value.push(caseItem)
    }
  }

  // 🔹 管理員同意（刪除案件）
  const approveAppeal = (caseItem: CaseItem) => {
    appeals.value = appeals.value.filter((c) => c !== caseItem)
  }

  // 🔹 管理員拒絕（不再可申訴）
  const rejectAppeal = (caseItem: CaseItem) => {
    appeals.value = appeals.value.filter((c) => c !== caseItem)
  }

  return {
    appeals,
    submitAppeal,
    approveAppeal,
    rejectAppeal,
  }
})
