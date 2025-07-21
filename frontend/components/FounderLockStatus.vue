<template>
  <div class="founder-lock-status p-4 bg-white rounded shadow">
    <h2 class="text-xl font-bold mb-2">Founder Lock Status</h2>
    <div class="mb-2">
      <span class="font-semibold">Founder:</span> {{ lock.founder }}
    </div>
    <div class="mb-2">
      <span class="font-semibold">Device ID:</span> {{ lock.device_id }}
    </div>
    <div class="mb-2">
      <span class="font-semibold">Biometric Required:</span>
      {{ lock.biometric_required ? "Yes" : "No" }}
    </div>
    <div class="mb-2">
      <span class="font-semibold">Emergency Backup:</span>
      {{ lock.emergency_backup }}
    </div>
    <div class="mb-2">
      <span class="font-semibold">Signed At:</span> {{ lock.signed_at }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
const lock = ref({});
onMounted(async () => {
  const res = await axios.get("/api/founder/lock");
  lock.value = res.data;
});
</script>

<style scoped>
.founder-lock-status {
  @apply max-w-md mx-auto;
}
</style>
