<template>
  <div class="admin-audit-dashboard p-6 bg-gray-50 min-h-screen">
    <h1 class="text-2xl font-bold mb-6">Audit Log Dashboard</h1>
    <div v-if="logs.length === 0" class="text-gray-500">No audit logs yet.</div>
    <table v-else class="min-w-full bg-white rounded shadow">
      <thead>
        <tr>
          <th class="px-4 py-2">Timestamp</th>
          <th class="px-4 py-2">Action</th>
          <th class="px-4 py-2">Actor</th>
          <th class="px-4 py-2">Status</th>
          <th class="px-4 py-2">Device</th>
          <th class="px-4 py-2">IP</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in logs" :key="log.timestamp">
          <td class="px-4 py-2">{{ log.timestamp }}</td>
          <td class="px-4 py-2">{{ log.action_type }}</td>
          <td class="px-4 py-2">{{ log.actor }}</td>
          <td class="px-4 py-2">{{ log.status }}</td>
          <td class="px-4 py-2">{{ log.device_id }}</td>
          <td class="px-4 py-2">{{ log.ip }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
const logs = ref([]);
onMounted(async () => {
  const res = await axios.get("/api/audit/logs");
  logs.value = res.data;
});
</script>

<style scoped>
.admin-audit-dashboard {
  @apply max-w-5xl mx-auto;
}
</style>
