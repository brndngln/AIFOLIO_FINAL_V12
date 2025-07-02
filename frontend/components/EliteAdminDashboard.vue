<template>
  <div class="elite-admin-dashboard p-6 bg-gradient-to-br from-gray-100 to-blue-50 min-h-screen">
    <h1 class="text-4xl font-extrabold mb-8 text-center text-blue-900">{{$t('eliteEmpireAdminDashboard')}}</h1>
    <div class="flex flex-wrap gap-4 mb-8 justify-center">
      <button class="btn-primary" @click="refresh">{{$t('refresh')}}</button>
      <button class="btn-secondary" @click="freezeSystem">{{$t('emergencyFreeze')}}</button>
      <button class="btn-danger" @click="overrideSystem">{{$t('founderOverride')}}</button>
      <button class="btn-warning" @click="rollbackSystem">{{$t('rollback')}}</button>
      <button class="btn-info" @click="testNotification">{{$t('testNotification')}}</button>
    </div>
    <div class="mb-10">
      <h2 class="text-2xl font-semibold mb-4">{{$t('systemEvents')}}</h2>
      <input v-model="eventSearch" class="input-search mb-4" :placeholder="$t('searchEvents')" />
      <table class="min-w-full bg-white rounded shadow-lg luxury-table">
        <thead>
          <tr>
            <th class="px-4 py-2">{{$t('timestamp')}}</th>
            <th class="px-4 py-2">{{$t('type')}}</th>
            <th class="px-4 py-2">{{$t('actor')}}</th>
            <th class="px-4 py-2">{{$t('status')}}</th>
            <th class="px-4 py-2">{{$t('integration')}}</th>
            <th class="px-4 py-2">{{$t('channels')}}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="event in filteredEvents" :key="event.timestamp">
            <td class="px-4 py-2">{{ event.timestamp }}</td>
            <td class="px-4 py-2">{{ event.type }}</td>
            <td class="px-4 py-2">
              <span v-if="event.actor === 'founder'" class="founder-badge">{{$t('founder')}}</span>
              {{ event.actor }}
            </td>
            <td class="px-4 py-2">
              <span v-if="event.status === 'high_priority'" class="status-high">{{$t('highPriority')}}</span>
              {{ event.status }}
            </td>
            <td class="px-4 py-2">{{ event.integration }}</td>
            <td class="px-4 py-2">
              <span v-if="event.channels" class="channels-badges">
                <span v-for="ch in event.channels" :key="ch" class="channel-badge">{{ ch }}</span>
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="mb-10">
      <h2 class="text-2xl font-semibold mb-4">{{$t('billionaireMindActivations')}}</h2>
      <input v-model="mindSearch" class="input-search mb-4" :placeholder="$t('searchMinds')" />
      <ul>
        <li v-for="mind in filteredMinds" :key="mind.name">
          <span class="font-semibold">{{ mind.name }}</span> — {{ mind.archetype }} ({{ mind.scaling_logic }})
        </li>
      </ul>
    </div>
    <div class="mb-10">
      <h2 class="text-2xl font-semibold mb-4">{{$t('complianceAndSentienceAlerts')}}</h2>
      <input v-model="alertSearch" class="input-search mb-4" :placeholder="$t('searchAlerts')" />
      <ul>
        <li v-for="alert in filteredAlerts" :key="alert.timestamp">
          <span class="text-red-600">[{{ alert.timestamp }}]</span> {{ alert.message }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
const events = ref([])
const billionaireMinds = ref([])
const complianceAlerts = ref([])
const eventSearch = ref('')
const mindSearch = ref('')
const alertSearch = ref('')

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

const filteredEvents = computed(() => events.value.filter(e =>
  Object.values(e).join(' ').toLowerCase().includes(eventSearch.value.toLowerCase())
))
const filteredMinds = computed(() => billionaireMinds.value.filter(m =>
  Object.values(m).join(' ').toLowerCase().includes(mindSearch.value.toLowerCase())
))
const filteredAlerts = computed(() => complianceAlerts.value.filter(a =>
  Object.values(a).join(' ').toLowerCase().includes(alertSearch.value.toLowerCase())
))

onMounted(refresh)
</script>

<style scoped>
.elite-admin-dashboard { @apply max-w-6xl mx-auto; }
.luxury-table { @apply shadow-2xl border border-blue-200; }
.input-search { @apply border border-blue-300 rounded px-3 py-2 mb-2 w-full max-w-md; }
.founder-badge { @apply bg-gradient-to-r from-yellow-300 to-yellow-500 text-black px-2 py-1 rounded font-bold ml-1; }
.status-high { @apply bg-red-600 text-white px-2 py-1 rounded font-semibold ml-1; }
.channels-badges { @apply flex gap-1; }
.channel-badge { @apply bg-blue-200 text-blue-900 px-2 py-1 rounded text-xs font-semibold; }
</style>
