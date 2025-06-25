<template>
  <div class="p-6 max-w-md mx-auto bg-white rounded shadow">
    <h2 class="text-xl font-semibold mb-4">Mot de passe réinitialisé</h2>
    <div v-if="password">
      <h3 class="font-medium">Nouveau mot de passe</h3>
      <code class="block bg-gray-100 p-2 rounded my-2">{{ password }}</code>
    </div>
    <div v-if="qr">
      <h3 class="font-medium">QR mot de passe</h3>
      <img :src="`data:image/png;base64,${qr}`" alt="QR mot de passe" class="mt-2"/>
    </div>
    <button
      @click="$emit('to-login')"
      class="mt-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
    >
      Aller à la connexion
    </button>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
defineProps({
  password: String,
  qr:       String,
})
const emit = defineEmits(['to-login'])
</script>
