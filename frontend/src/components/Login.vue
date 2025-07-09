<template>
  <div class="p-6 max-w-md mx-auto bg-white rounded shadow">
    <h2 class="text-xl font-semibold mb-4">Connexion</h2>

    <input
      v-model="username"
      placeholder="Pseudo"
      class="w-full mb-2 px-3 py-2 border rounded"
    />
    <input
      v-model="password"
      type="password"
      placeholder="Mot de passe"
      class="w-full mb-2 px-3 py-2 border rounded"
    />
    <input
      v-model="totp"
      placeholder="TOTP"
      class="w-full mb-4 px-3 py-2 border rounded"
    />

    <button
      @click="doLogin()"
      class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
    >
      Se connecter
    </button>

    <!-- Message d’erreur ou de succès -->
    <p v-if="error" class="mt-3 text-red-600">{{ error }}</p>
    <p v-else-if="success" class="mt-3 text-green-600">Connexion réussie !</p>

    <button 
      @click="$emit('back')" 
      class="mt-4 text-blue-600 hover:underline"
    >
      ← Retour
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// On émet toujours 'expired' si le compte est expiré, 'back' pour revenir
const emit = defineEmits(['expired','back'])

const username = ref('')
const password = ref('')
const totp     = ref('')

// Messages d'état
const error   = ref('')
const success = ref(false)

async function doLogin() {
  // Réinitialisation
  error.value = ''
  success.value = false

  const res = await fetch('/authuser', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: username.value,
      password: password.value,
      totp: totp.value
    })
  })

  if (res.status === 403) {
    // Compte expiré : on émet pour basculer sur reset si besoin
    emit('expired')
    return
  }

  if (!res.ok) {
    error.value = 'Identifiants invalides'
    return
  }

  // Succès de la connexion
  success.value = true
}
</script>
