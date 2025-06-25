<template>
  <div class="p-6 max-w-md mx-auto bg-white rounded shadow">
    <h2 class="text-xl font-semibold mb-4">Créer un compte</h2>
    <input
      v-model="username"
      placeholder="Pseudo"
      class="w-full mb-2 px-3 py-2 border rounded"
    />
    <button
      @click="generate()"
      class="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700"
    >
      Générer mes identifiants
    </button>

    <div v-if="password" class="mt-4">
      <h3 class="font-medium">Mot de passe</h3>
      <code class="block bg-gray-100 p-2 rounded my-2">{{ password }}</code>
    </div>
    <div v-if="qr2fa" class="mt-4">
      <h3 class="font-medium">QR Code 2FA</h3>
      <img :src="`data:image/png;base64,${qr2fa}`" alt="QR 2FA" class="mt-2" />
    </div>

    <button @click="$emit('back')" class="mt-6 text-blue-600 hover:underline">
      ← Retour
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const emit = defineEmits(['generated','back'])
const username = ref('')
const password = ref('')
const qr2fa = ref('')

async function generate() {
  const r1 = await fetch('/genpwd', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ username: username.value })
  })
  const { password: pwd } = await r1.json()
  password.value = pwd

  const r2 = await fetch('/gen2fa', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ username: username.value })
  })
  const { secret_qr } = await r2.json()
  qr2fa.value = secret_qr

  emit('generated', { password: pwd, qr2fa: secret_qr })
}
</script>
