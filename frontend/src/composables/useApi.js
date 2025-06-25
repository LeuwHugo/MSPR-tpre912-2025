// src/composables/useApi.js
import { reactive } from 'vue'

export function useApi() {
  const state = reactive({ message: '' })

  async function post(path, body) {
    const res = await fetch(path, {
      method:'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(body)
    })
    if (!res.ok) throw res
    return res.json()
  }

  return { state, post }
}
