<template>
  <div class="empire-control-panel">
    <h2>Billionaire Empire Control Panel</h2>
    <div class="founder-command">
      <input v-model="founderCommand" placeholder="Enter strategic vision or command..." @keyup.enter="executeFounderCommand"/>
      <button @click="executeFounderCommand">Execute</button>
    </div>
    <div class="voice-ar-controls">
      <button @click="triggerVoiceActivation">🎤 Voice Spawn</button>
      <button @click="triggerARPreview">🕶️ AR Preview</button>
    </div>
    <div v-for="biz in businesses" :key="biz.id" class="biz-card">
      <h3>{{ biz.config.name || biz.id }}</h3>
      <ul>
        <li>Profit: {{ biz.analytics?.profit }}</li>
        <li>Growth: {{ biz.successMatrix?.traffic }}</li>
        <li>Risk: {{ biz.riskFirewall }}</li>
        <li>Virality: {{ biz.virality }}</li>
        <li>Status: {{ biz.status }}</li>
        <li>ROI: {{ biz.analytics?.roi }}</li>
        <li>AR Preview: <span v-if="biz.arPreview">Enabled</span><span v-else>—</span></li>
      </ul>
      <div v-if="biz.arPreview">
        <img :src="biz.arPreview.previewUrl" alt="AR Preview" style="max-width:200px;border-radius:1rem;box-shadow:0 0 16px #00fff7a0;"/>
      </div>
    </div>
  </div>
</template>
<script>
import BusinessSpawner from '../core/business_spawner.js';
import Analytics3 from '../core/analytics_3.js';
import { showARPreview } from './ar_preview.js';
import { activateByVoice } from './voice_activation.js';

export default {
  name: 'EmpireControlPanel',
  data() {
    return {
      businesses: [],
      founderCommand: ''
    };
  },
  mounted() {
    // Demo: spawn 3 businesses
    this.businesses = [
      BusinessSpawner.spawnBusiness({ name: 'Luxury NFT Vault', revenue: 1000000, cost: 10000 }),
      BusinessSpawner.spawnBusiness({ name: 'AI SaaS Builder', revenue: 3000000, cost: 200000 }),
      BusinessSpawner.spawnBusiness({ name: 'Viral Content Engine', revenue: 500000, cost: 5000 })
    ];
    BusinessSpawner.optimizeAll();
    this.updateAnalytics();
  },
  methods: {
    updateAnalytics() {
      this.businesses = BusinessSpawner.getAllBusinesses().map(biz => {
        biz.analytics = Analytics3.track(biz);
        return biz;
      });
    },
    triggerVoiceActivation() {
      const result = activateByVoice('spawn business');
      if(result.triggered) {
        const newBiz = BusinessSpawner.spawnBusiness({ name: `Voice Spawned Biz ${Date.now()}` });
        BusinessSpawner.optimizeAll();
        this.updateAnalytics();
      }
    },
    triggerARPreview() {
      // Enable AR preview for all businesses for demo
      this.businesses = this.businesses.map(biz => {
        biz.arPreview = showARPreview({ businessId: biz.id, previewUrl: `/products/${biz.id}_ar.png` });
        return biz;
      });
    },
    executeFounderCommand() {
      if(this.founderCommand.trim()) {
        // For demo: spawn a new business with the command as the name
        const newBiz = BusinessSpawner.spawnBusiness({ name: this.founderCommand.trim() });
        BusinessSpawner.optimizeAll();
        this.updateAnalytics();
        this.founderCommand = '';
      }
    }
  }
};
</script>
<style scoped>
.empire-control-panel { background: #181c2b; color: #fff; border-radius: 2rem; box-shadow: 0 0 32px #00fff7a0; padding: 2rem; }
.biz-card { background: #232845; margin: 1rem 0; border-radius: 1.5rem; padding: 1.2rem; box-shadow: 0 2px 16px #00fff780; transition: box-shadow 0.3s; }
.biz-card:hover { box-shadow: 0 4px 32px #00fff7cc; }
.founder-command { margin-bottom: 1.5rem; display: flex; gap: 0.5rem; }
.founder-command input { flex: 1; border-radius: 1rem; padding: 0.5rem 1rem; border: none; font-size: 1.1rem; }
.founder-command button { border-radius: 1rem; background: #00fff7; color: #232845; font-weight: bold; padding: 0.5rem 1.2rem; box-shadow: 0 2px 8px #00fff7a0; transition: background 0.2s; }
.founder-command button:hover { background: #00b3a6; color: #fff; }
.voice-ar-controls { margin-bottom: 1.5rem; display: flex; gap: 1rem; }
.voice-ar-controls button { border-radius: 1rem; background: #232845; color: #00fff7; font-weight: bold; padding: 0.5rem 1.2rem; box-shadow: 0 2px 8px #00fff7a0; transition: background 0.2s; border: none; }
.voice-ar-controls button:hover { background: #00fff7; color: #232845; }
</style>
