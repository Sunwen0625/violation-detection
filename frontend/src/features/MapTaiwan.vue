<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed, watch } from 'vue'
import { LMap, LTileLayer, LControlZoom } from '@vue-leaflet/vue-leaflet'
import L from 'leaflet'
import 'leaflet.markercluster'

/** props：資料來源與設定 */
const props = withDefaults(
  defineProps<{
    points?: Array<{
      經緯度: { lat: number; lon: number }
      車牌: string
      照片: string
      時間: string
      完整路名: string
    }>
    url?: string
    circleRadius?: number // 放大時每點的外圈半徑（公尺）
    maxClusterZoom?: number // 幾倍開始不再群聚（展開 Marker）
  }>(),
  {
    url: '/data/cases.json',
    circleRadius: 120,
    maxClusterZoom: 12, // 與地圖 maxZoom 同步就能「最大倍率時展開」
  },
)

/** 地圖基本參數（台灣邊界、縮放） */
const center = ref<[number, number]>([23.7, 121])
const taiwanBounds: L.LatLngBoundsExpression = [
  [21.5, 119.3],
  [25.5, 122.5],
]
const minZoom = 6
const maxZoom = 12
const zoom = ref(7)

/** 修正預設 Marker 圖示（Vite 常見坑） */
const DefaultIcon = L.Icon.Default.prototype as any
DefaultIcon.options.iconUrl = new URL(
  'leaflet/dist/images/marker-icon.png',
  import.meta.url,
).toString()
DefaultIcon.options.iconRetinaUrl = new URL(
  'leaflet/dist/images/marker-icon-2x.png',
  import.meta.url,
).toString()
DefaultIcon.options.shadowUrl = new URL(
  'leaflet/dist/images/marker-shadow.png',
  import.meta.url,
).toString()

/** 載入資料（兩種方式：直接傳 points 或從 url 抓） */
const raw = ref<any[]>([])
onMounted(async () => {
  if (props.points?.length) {
    raw.value = props.points
  } else if (props.url) {
    try {
      const res = await fetch(props.url)
      if (res.ok) raw.value = await res.json()
    } catch (e) {
      console.warn('載入資料失敗', e)
    }
  }
})

/** 正規化資料 */
type P = {
  id: number
  lat: number
  lng: number
  plate: string
  photo: string
  time: string
  road: string
}
const data = computed<P[]>(() =>
  raw.value
    .map((d, i) => ({
      id: i + 1,
      lat: d?.經緯度?.lat,
      lng: d?.經緯度?.lon,
      plate: d?.車牌,
      photo: d?.照片,
      time: d?.時間,
      road: d?.完整路名,
    }))
    .filter((p) => Number.isFinite(p.lat) && Number.isFinite(p.lng)),
)

/** 叢集群組、圈圈群組與 map 引用 */
let map: L.Map | null = null
let cluster: L.MarkerClusterGroup | null = null
let circlesLayer: L.LayerGroup | null = null

function buildPopupHtml(p: P) {
  const time = new Date(p.time).toLocaleString()
  const link = p.photo
    ? `<div style="margin-top:6px;"><a href="${p.photo}" target="_blank" rel="noreferrer">查看照片</a></div>`
    : ''
  return `
    <div style="font-size:14px;line-height:1.4">
      <div><strong>車牌：</strong>${p.plate}</div>
      <div><strong>時間：</strong>${time}</div>
      <div><strong>路名：</strong>${p.road}</div>
      ${link}
    </div>
  `
}

/** 當地圖 ready，把叢集層建起來 */
function onReady(m: L.Map) {
  map = m

  // 1) 建立叢集層
  cluster = L.markerClusterGroup({
    maxClusterRadius: 60, // 群聚半徑（像素）：越小越快拆開
    showCoverageOnHover: false, // 滑鼠移到群聚不要畫覆蓋範圍
    spiderfyOnEveryZoom: true, // 每一級縮放都能蜘蛛化
    disableClusteringAtZoom: props.maxClusterZoom, // >= 12 就不再群聚
  })

  // 2) 將資料轉成 marker 加入叢集
  data.value.forEach((p) => {
    const marker = L.marker([p.lat, p.lng])
    marker.bindPopup(buildPopupHtml(p))
    cluster!.addLayer(marker)
  })

  map.addLayer(cluster)

  // 3) 放大時顯示圈圈（圈起周圍）；縮小時拿掉，避免太擠
  circlesLayer = L.layerGroup().addTo(map)
  drawCircles()
  map.on('zoomend', drawCircles)
}

/** 依縮放繪製/清空圈圈 */
function drawCircles() {
  if (!map || !circlesLayer) return
  circlesLayer.clearLayers()

  const z = map.getZoom()
  if (z < maxZoom) {
    // 未達最大縮放 -> 不畫圈（用群聚視覺即可）
    return
  }

  // 最大縮放：為每個點畫一圈
  data.value.forEach((p) => {
    const c = L.circle([p.lat, p.lng], {
      radius: props.circleRadius,
      color: '#ff6b6b',
      weight: 1.5,
      opacity: 0.7,
      fillColor: '#ff6b6b',
      fillOpacity: 0.1,
    })
    circlesLayer!.addLayer(c)
  })
}

/** 當資料變動時，重建叢集與圈圈 */
watch(data, () => {
  if (!map) return
  if (cluster) {
    map.removeLayer(cluster)
    cluster.clearLayers()
  }
  cluster = L.markerClusterGroup({
    maxClusterRadius: 60,
    showCoverageOnHover: false,
    spiderfyOnEveryZoom: true,
    disableClusteringAtZoom: props.maxClusterZoom,
  })
  data.value.forEach((p) => {
    const m = L.marker([p.lat, p.lng]).bindPopup(buildPopupHtml(p))
    cluster!.addLayer(m)
  })
  map.addLayer(cluster)
  drawCircles()
})

onBeforeUnmount(() => {
  if (!map) return
  map.off('zoomend', drawCircles)
  if (cluster) map.removeLayer(cluster)
  if (circlesLayer) map.removeLayer(circlesLayer)
})
</script>

<template>
  <div class="w-full block rounded-xl overflow-hidden shadow-lg">
    <LMap
      v-model:zoom="zoom"
      :center="center"
      :min-zoom="minZoom"
      :max-zoom="maxZoom"
      :max-bounds="taiwanBounds"
      :max-bounds-viscosity="1.0"
      style="height: 70vh; width: 100%"
      @ready="onReady"
    >
      <LTileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        :no-wrap="true"
        :attribution="'© OpenStreetMap contributors'"
      />
      <LControlZoom position="topright" />
    </LMap>
  </div>
</template>
