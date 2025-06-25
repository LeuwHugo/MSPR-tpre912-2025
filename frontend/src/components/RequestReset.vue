<template>
  <div class="p-6 max-w-md mx-auto bg-white rounded shadow">
    <h2 class="text-xl font-semibold mb-4">Mot de passe oublié</h2>
    <input
      v-model="username"
      placeholder="Pseudo"
      class="w-full mb-4 px-3 py-2 border rounded"
    />
    <button
      @click="request()"
      class="w-full bg-yellow-600 text-white py-2 rounded hover:bg-yellow-700"
    >
      Envoyer lien de réinitialisation
    </button>
    <p class="mt-3 text-green-600" v-if="link">{{ link }}</p>
    <p class="mt-3 text-red-600" v-if="error">{{ error }}</p>
    <button @click="$emit('back')" class="mt-4 text-blue-600 hover:underline">
      ← Retour
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const emit = defineEmits(['requested','back'])
const username = ref('')
const link = ref('')
const error = ref('')

async function request() {
  error.value = ''
  const res = await fetch('/request-reset', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ username: username.value })
  })
  if (!res.ok) {
    error.value = 'Erreur de demande'
    return
  }
  const { reset_link } = await res.json()
  link.value = reset_link
  emit('requested', { reset_link })
}
</script>
