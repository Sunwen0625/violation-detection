<template>
  <div class="space-y-16 px-6 py-10 text-gray-200">
    <!-- 🔹 1. Hero -->
    <section class="text-center space-y-4">
      <h1 class="text-4xl font-bold text-white">違規停車檢舉系統</h1>

      <p class="text-gray-400 max-w-2xl mx-auto">
        結合 AI 影像辨識與即時通報，協助使用者快速完成違規停車檢舉，
        提升交通管理效率，改善生活環境。
      </p>

      <div class="flex justify-center gap-4 mt-4">
        <RouterLink
          to="/login"
          class="px-6 py-3 rounded-xl bg-blue-500 hover:bg-blue-400 transition text-white font-semibold"
        >
          開始檢舉
        </RouterLink>

        <RouterLink
          to="/login"
          class="px-6 py-3 rounded-xl bg-gray-700 hover:bg-gray-600 transition"
        >
          查看紀錄
        </RouterLink>
      </div>
    </section>

    <!-- 🔹 2. 功能介紹 -->
    <section>
      <h2 class="text-2xl font-bold text-white mb-6 text-center">系統功能</h2>

      <div class="grid md:grid-cols-3 gap-6">
        <div class="bg-[#2a2a2a] p-6 rounded-xl shadow">
          <h3 class="text-lg font-semibold text-white mb-2">🚗 違規檢舉</h3>
          <p class="text-gray-400 text-sm">
            上傳照片或使用影像辨識，自動判斷是否為違規停車並建立案件。
          </p>
        </div>

        <div class="bg-[#2a2a2a] p-6 rounded-xl shadow">
          <h3 class="text-lg font-semibold text-white mb-2">📄 檢舉歷史</h3>
          <p class="text-gray-400 text-sm">查看過去所有檢舉紀錄，包含時間、地點與相關證據。</p>
        </div>

        <div class="bg-[#2a2a2a] p-6 rounded-xl shadow">
          <h3 class="text-lg font-semibold text-white mb-2">📍 地圖查看</h3>
          <p class="text-gray-400 text-sm">在地圖上查看違規位置，快速掌握違規熱點。</p>
        </div>
      </div>
    </section>

    <!-- 🔹 3. 操作流程 -->
    <section>
      <h2 class="text-2xl font-bold text-white mb-6 text-center">使用流程</h2>

      <div class="grid md:grid-cols-4 gap-6 text-center">
        <div>
          <div class="text-blue-400 text-2xl font-bold">1</div>
          <p class="mt-2 text-gray-300">登入帳號</p>
        </div>

        <div>
          <div class="text-blue-400 text-2xl font-bold">2</div>
          <p class="mt-2 text-gray-300">拍攝或上傳照片</p>
        </div>

        <div>
          <div class="text-blue-400 text-2xl font-bold">3</div>
          <p class="mt-2 text-gray-300">系統自動判斷</p>
        </div>

        <div>
          <div class="text-blue-400 text-2xl font-bold">4</div>
          <p class="mt-2 text-gray-300">送出檢舉</p>
        </div>
      </div>
    </section>

    <!-- 🔹 4. 系統價值 -->
    <section class="text-center max-w-3xl mx-auto space-y-4">
      <h2 class="text-2xl font-bold text-white">為什麼使用這個系統？</h2>

      <p class="text-gray-400">
        傳統違規停車處理方式高度依賴人力，本系統透過 AI 自動辨識與資料整合，
        提供快速、準確且便利的檢舉流程，降低人工負擔並提升效率。
      </p>

      <p class="text-gray-400">
        同時透過資料累積與視覺化分析，有助於發現違規熱點， 改善交通與居住環境。
      </p>
    </section>
  </div>
</template>
