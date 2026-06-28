import axios from 'axios'

export interface UserProfile {
  name: string
  email: string
  phone: string
  idNumber: string
  address: string
  avatar: string
}

export async function getUserByEmail(email: string): Promise<UserProfile> {
  const { data } = await axios.get(`http://127.0.0.1:8000/users/by-email/${email}`)
  return data
}

export async function updateUserByEmail(
  email: string,
  payload: {
    name: string
    email: string
    phone_number: string
    address: string
    idNumber: string
    avatar: string
  },
) {
  const { data } = await axios.put(`http://127.0.0.1:8000/users/by-email/${email}`, {
    name: payload.name,
    email: payload.email,
    phone_number: payload.phone_number,
    address: payload.address,
    id_number: payload.idNumber,
    avatar: payload.avatar,
  })

  return data
}
