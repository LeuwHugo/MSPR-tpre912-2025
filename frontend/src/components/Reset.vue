<template>
  <div class="p-6 max-w-md mx-auto bg-white rounded shadow">
    <h2 class="text-xl font-semibold mb-4">Réinitialisation</h2>
    <p class="mb-4">Un nouveau mot de passe va être généré.</p>
    <button
      @click="reset()"
      class="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700"
    >
      Générer nouveau mot de passe
    </button>
    <button @click="$emit('back')" class="mt-4 text-blue-600 hover:underline">
      ← Retour
    </button>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
const props = defineProps({ token: String })
const emit  = defineEmits(['reset','back'])

async function reset() {
  const res = await fetch('/reset-password', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ username: props.token })
  })
  if (!res.ok) return
  const data = await res.json()
  emit('reset', data)
}
</script>