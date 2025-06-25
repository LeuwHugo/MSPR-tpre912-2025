<template>
  <div>
    <!-- Home -->
    <Home
      v-if="view === 'home'"
      @navigate="view = $event"
    />

    <!-- Create account -->
    <Create
      v-else-if="view === 'create'"
      @generated="onGenerated"
      @back="view = 'home'"
    />

    <!-- Show created credentials -->
    <div
      v-else-if="view === 'createResult'"
      class="container"
    >
      <h2 class="text-xl font-semibold mb-4">Identifiants générés</h2>
      <div>
        <h3>Mot de passe</h3>
        <code class="block bg-gray-100 p-2 rounded my-2">{{ password }}</code>
      </div>
      <div v-if="qr2fa">
        <h3>QR Code 2FA</h3>
        <img
          :src="`data:image/png;base64,${qr2fa}`"
          alt="QR 2FA"
          class="mt-2"
        />
      </div>
      <button @click="view = 'login'" class="btn mt-4">
        Aller à la connexion
      </button>
    </div>

    <!-- Login -->
    <Login
      v-else-if="view === 'login'"
      @expired="view = 'request'"
      @login="view = 'home'"
      @back="view = 'home'"
    />

    <!-- Request reset -->
    <RequestReset
      v-else-if="view === 'request'"
      @requested="onRequested"
      @back="view = 'home'"
    />

    <!-- Reset (generate new password) -->
    <Reset
      v-else-if="view === 'reset'"
      :token="resetToken"
      @reset="onReset"
      @back="view = 'home'"
    />

    <!-- Reset result -->
    <ResetResult
      v-else-if="view === 'resetResult'"
      :password="password"
      :qr="qrPwd"
      @to-login="view = 'login'"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Home from './components/Home.vue'
import Create from './components/Create.vue'
import Login from './components/Login.vue'
import RequestReset from './components/RequestReset.vue'
import Reset from './components/Reset.vue'
import ResetResult from './components/ResetResult.vue'

// Gestion de la vue courante
const view = ref('home')

// Stockage des données partagées
const password = ref('')
const qr2fa = ref('')
const qrPwd = ref('')
const resetToken = ref('')

// Quand Create.vue émet { password, qr2fa }
function onGenerated({ password: pwd, qr2fa: q }) {
  password.value = pwd
  qr2fa.value = q
  view.value = 'createResult'
}

// Quand RequestReset.vue émet (on ne change pas de vue ici)
function onRequested({ reset_link }) {
  // tu peux afficher un toast ou stocker le lien si tu veux
  console.log('Lien de reset :', reset_link)
}

// Quand Reset.vue émet { password, password_qr }
function onReset({ password: pwd, password_qr }) {
  password.value = pwd
  qrPwd.value = password_qr
  view.value = 'resetResult'
}

// Si tu récupères view & token depuis la query string au chargement
const params = new URLSearchParams(location.search)
const initialView = params.get('view')
const token = params.get('token')
if (initialView === 'reset' && token) {
  view.value = 'reset'
  resetToken.value = token
}
</script>

<style>
.btn {
  background: #005fcc;
  color: #fff;
  padding: 0.6rem 1.2rem;
  border-radius: 4px;
  cursor: pointer;
  border: none;
}
.btn:hover {
  background: #004bb5;
}
</style>
