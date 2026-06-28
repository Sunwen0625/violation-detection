import type { RouteLocationRaw } from 'vue-router'

export interface MenuItem {
  name: string
  path?: RouteLocationRaw
  children?: MenuItem[]
}

export const sidebarConfig: Record<string, MenuItem[]> = {
  // 🔹 訪客
  guest: [
    { name: '首頁', path: '/' },
    { name: '關於我們', path: '/about' },
  ],

  // 🔹 一般使用者
  user: [
    { name: '首頁', path: '/' },

    {
      name: '基本資料',
      path: '/profile',
    },

    { name: '檢舉歷史', path: '/records' },
    { name: '違規紀錄', path: '/report' },

    { name: '行車紀錄器檢舉', path: '/dashcam' },
  ],

  // 🔹 管理者
  admin: [
    {
      name: '個人資料',
      path: '/profile',
    },
    { name: '申訴重審', path: '/appeals' },
    { name: '違規停車位置', path: '/map' },
  ],
}
