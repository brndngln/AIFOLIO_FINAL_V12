<template>
  <div
    class="founder-login flex flex-col items-center justify-center min-h-screen bg-gray-50"
  >
    <h1 class="text-3xl font-bold mb-6">Founder Login</h1>
    <form @submit.prevent="submit" class="w-full max-w-sm">
      <div class="mb-4">
        <label class="block text-gray-700">Device ID</label>
        <input v-model="device_id" class="input" readonly />
      </div>
      <div class="mb-4">
        <label class="block text-gray-700">Biometric (Touch ID/Face ID)</label>
        <button type="button" @click="biometricAuth" class="btn">
          Verify Biometric
        </button>
        <span v-if="biometricVerified" class="text-green-600 ml-2"
          >Verified</span
        >
      </div>
      <div class="mb-4">
        <label class="block text-gray-700">OTP</label>
        <input v-model="otp" class="input" placeholder="Enter OTP" />
      </div>
      <div class="mb-4">
        <label class="block text-gray-700">Founder Key Signature</label>
        <input
          v-model="signature"
          class="input"
          placeholder="Paste digital signature"
        />
      </div>
      <button type="submit" class="btn-primary w-full">Login</button>
    </form>
    <div v-if="error" class="text-red-600 mt-4">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
const device_id = ref("");
const otp = ref("");
const signature = ref("");
const biometricVerified = ref(false);
const error = ref("");

// Simulate device fingerprinting
if (window && window.navigator) {
  device_id.value =
    window.navigator.userAgent + "-" + window.navigator.platform;
}

function biometricAuth() {
  // Stub: Use WebAuthn/TouchID/FaceID API in production
  biometricVerified.value = true;
}

async function submit() {
  error.value = "";
  if (!biometricVerified.value) {
    error.value = "Biometric verification required.";
    return;
  }
  try {
    const res = await axios.post("/api/founder/login", {
      device_id: device_id.value,
      otp: otp.value,
      signature: signature.value,
      public_key: "YOUR_PUBLIC_KEY",
      challenge: "LOGIN_CHALLENGE",
      otp_secret: "YOUR_OTP_SECRET",
    });
    if (res.data.status === "success") {
      window.location.href = "/admin";
    } else {
      error.value = "Login failed.";
    }
  } catch (e) {
    error.value = e.response?.data?.detail || "Login failed.";
  }
}
</script>

<style scoped>
.input {
  @apply border rounded px-3 py-2 w-full;
}
.btn {
  @apply bg-blue-100 text-blue-700 px-4 py-2 rounded;
}
.btn-primary {
  @apply bg-blue-600 text-white px-4 py-2 rounded;
}
</style>
