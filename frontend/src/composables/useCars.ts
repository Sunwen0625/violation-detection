import { ref } from 'vue'

export interface Car {
  car_id: number
  license_plate: string
}

export function useCars(userId: number) {
  const cars = ref<Car[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchCars = async () => {
    loading.value = true
    try {
      const res = await fetch(`/api/cars/${userId}`)
      if (!res.ok) throw new Error('載入失敗')
      cars.value = await res.json()
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const addCar = async (plate: string) => {
    try {
      const res = await fetch(`/api/cars/${userId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ license_plate: plate }),
      })

      if (!res.ok) throw new Error('新增失敗')

      const newCar = await res.json()
      cars.value.push(newCar)
    } catch (err: any) {
      error.value = err.message
    }
  }

  const deleteCar = async (carId: number) => {
    try {
      const res = await fetch(`/api/cars/${userId}/${carId}`, {
        method: 'DELETE',
      })

      if (!res.ok) throw new Error('刪除失敗')

      cars.value = cars.value.filter((c) => c.car_id !== carId)
    } catch (err: any) {
      error.value = err.message
    }
  }

  return {
    cars,
    loading,
    error,
    fetchCars,
    addCar,
    deleteCar,
  }
}
