<template>
  <div class="vault-ui mythmaker">
    <h1>🐉 MYTHMAKER™</h1>
    <p>Fantasy World & RPG Asset Vault</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: 'MYTHMAKER' };
</script>
<style scoped>
.vault-ui.mythmaker { background: rgba(24,28,47,0.85); border-radius: 18px; box-shadow: 0 0 24px #00ffd0; color: #fff; padding: 2rem; }
h1 { text-shadow: 0 0 8px #00ffd0; }
</style>
