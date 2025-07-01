<template>
  <div class="empire-control-panel">
    <h2>Billionaire Empire Control Panel</h2>
    <div v-for="biz in businesses" :key="biz.id" class="biz-card">
      <h3>{{ biz.config.name || biz.id }}</h3>
      <ul>
        <li>Profit: {{ biz.analytics.profit }}</li>
        <li>Growth: {{ biz.successMatrix?.traffic }}</li>
        <li>Risk: {{ biz.riskFirewall }}</li>
        <li>Virality: {{ biz.virality }}</li>
        <li>Status: {{ biz.status }}</li>
      </ul>
    </div>
  </div>
</template>
<script>
import BusinessSpawner from '../core/business_spawner.js';
export default {
  name: 'EmpireControlPanel',
  data() {
    return {
      businesses: []
    };
  },
  mounted() {
    // Example: spawn 3 businesses for demo
    this.businesses = [
      BusinessSpawner.spawnBusiness({ name: 'Luxury NFT Vault', revenue: 1000000, cost: 10000 }),
      BusinessSpawner.spawnBusiness({ name: 'AI SaaS Builder', revenue: 3000000, cost: 200000 }),
      BusinessSpawner.spawnBusiness({ name: 'Viral Content Engine', revenue: 500000, cost: 5000 })
    ];
    BusinessSpawner.optimizeAll();
    this.businesses = BusinessSpawner.getAllBusinesses();
  }
};
</script>
<style scoped>
.empire-control-panel { background: #181c2b; color: #fff; border-radius: 2rem; box-shadow: 0 0 32px #00fff7a0; padding: 2rem; }
.biz-card { background: #232845; margin: 1rem 0; border-radius: 1.5rem; padding: 1.2rem; box-shadow: 0 2px 16px #00fff780; transition: box-shadow 0.3s; }
.biz-card:hover { box-shadow: 0 4px 32px #00fff7cc; }
</style>
