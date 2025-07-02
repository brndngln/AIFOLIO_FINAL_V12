<template>
  <div class="elite-admin-dashboard p-6 bg-gray-100 min-h-screen">
    <h1 class="text-3xl font-bold mb-6">Elite Empire Admin Dashboard</h1>
    <div class="mb-4">
      <button class="btn-primary" @click="refresh">Refresh</button>
      <button class="btn-secondary ml-2" @click="freezeSystem">Emergency Freeze</button>
    </div>
    <div class="mb-6">
      <h2 class="text-xl font-semibold mb-2">System Events</h2>
      <table class="min-w-full bg-white rounded shadow">
        <thead>
          <tr>
            <th class="px-4 py-2">Timestamp</th>
            <th class="px-4 py-2">Type</th>
            <th class="px-4 py-2">Actor</th>
            <th class="px-4 py-2">Status</th>
            <th class="px-4 py-2">Integration</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="event in events" :key="event.timestamp">
            <td class="px-4 py-2">{{ event.timestamp }}</td>
            <td class="px-4 py-2">{{ event.type }}</td>
            <td class="px-4 py-2">{{ event.actor }}</td>
            <td class="px-4 py-2">{{ event.status }}</td>
            <td class="px-4 py-2">{{ event.integration }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="mb-6">
      <h2 class="text-xl font-semibold mb-2">Billionaire Mind Activations</h2>
      <ul>
        <li v-for="mind in billionaireMinds" :key="mind.name">
          <span class="font-semibold">{{ mind.name }}</span> — {{ mind.archetype }} ({{ mind.scaling_logic }})
        </li>
      </ul>
    </div>
    <div class="mb-6">
      <h2 class="text-xl font-semibold mb-2">Compliance & Sentience Alerts</h2>
      <ul>
        <li v-for="alert in complianceAlerts" :key="alert.timestamp">
          <span class="text-red-600">[{{ alert.timestamp }}]</span> {{ alert.message }}
        </li>
      </ul>
    </div>
    <div class="mb-6">
      <h2 class="text-xl font-semibold mb-2">Founder Controls</h2>
      <button class="btn-danger" @click="overrideSystem">Founder Override</button>
      <button class="btn-warning ml-2" @click="rollbackSystem">Rollback</button>
      <button class="btn-info ml-2" @click="testNotification">Test Notification</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
const events = ref([])
const billionaireMinds = ref([])
const complianceAlerts = ref([])

async function refresh() {
  const res = await axios.get('/api/elite/events')
  events.value = res.data
  const mindsRes = await axios.get('/api/elite/billionaire_minds')
  billionaireMinds.value = mindsRes.data
  const alertsRes = await axios.get('/api/elite/compliance_alerts')
  complianceAlerts.value = alertsRes.data
}
function freezeSystem() { axios.post('/api/elite/freeze') }
function overrideSystem() { axios.post('/api/elite/override') }
function rollbackSystem() { axios.post('/api/elite/rollback') }
function testNotification() { axios.post('/api/elite/test_notification') }
onMounted(refresh)
</script>

<style scoped>
.elite-admin-dashboard { @apply max-w-6xl mx-auto; }
.btn-primary { @apply bg-blue-700 text-white px-4 py-2 rounded; }
.btn-secondary { @apply bg-gray-400 text-white px-4 py-2 rounded; }
.btn-danger { @apply bg-red-600 text-white px-4 py-2 rounded; }
.btn-warning { @apply bg-yellow-500 text-white px-4 py-2 rounded; }
.btn-info { @apply bg-blue-400 text-white px-4 py-2 rounded; }
</style>
