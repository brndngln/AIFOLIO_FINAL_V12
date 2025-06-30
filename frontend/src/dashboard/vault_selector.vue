<template>
  <div class="vault-selector-grid">
    <div v-for="vault in vaults" :key="vault.id" class="vault-card" @click="$emit('select', vault)">
      <div class="icon">{{ vault.icon }}</div>
      <div class="label">{{ vault.label }}</div>
    </div>
  </div>
</template>
<script>
import vaultRegistry from '../../../config/vault_registry.json';
export default {
  name: 'VaultSelector',
  data() {
    return { vaults: vaultRegistry };
  }
};
</script>
<style scoped>
.vault-selector-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 2rem;
  background: rgba(10,10,20,0.85);
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 0 0 40px #00ffd0, 0 0 0 2px #222 inset;
}
.vault-card {
  cursor: pointer;
  background: rgba(30,30,40,0.9);
  border-radius: 16px;
  box-shadow: 0 0 16px #00ffd0;
  color: #fff;
  padding: 1.5rem 1rem;
  text-align: center;
  transition: transform 0.13s, box-shadow 0.13s;
  position: relative;
}
.vault-card:hover {
  transform: scale(1.06);
  box-shadow: 0 0 32px #00ffd0, 0 0 0 3px #fff inset;
  z-index: 2;
}
.icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 12px #00ffd0;
}
.label {
  font-weight: bold;
  font-size: 1.2rem;
  letter-spacing: 0.04em;
}
</style>
