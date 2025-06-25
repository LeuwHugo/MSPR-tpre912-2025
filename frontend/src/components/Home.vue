<!-- src/components/Home.vue -->
<template>
  <div class="p-6 text-center">
    <h1 class="text-3xl font-bold mb-4">Bienvenue</h1>
    <div class="space-x-2">
      <button @click="$emit('navigate','create')" class="btn">Créer</button>
      <button @click="$emit('navigate','login')" class="btn">Connexion</button>
      <button @click="$emit('navigate','request')" class="btn">Mot de passe oublié</button>
    </div>
  </div>
</template>

<script setup>
// rien à ajouter pour l’instant
</script>

<style scoped>
.btn {
  @apply bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700;
}
</style>
