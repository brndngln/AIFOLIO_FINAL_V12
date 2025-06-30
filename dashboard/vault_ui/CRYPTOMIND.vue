<template>
  <div class="vault-ui cryptomind">
    <h1>🪙 CRYPTOMIND™</h1>
    <p>Crypto Education + DeFi Toolkit Generator</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: 'CRYPTOMIND' };
</script>
<style scoped>
.vault-ui.cryptomind { background: rgba(20,20,20,0.8); border-radius: 18px; box-shadow: 0 0 24px #00ffd0; color: #fff; padding: 2rem; }
h1 { text-shadow: 0 0 8px #00ffd0; }
</style>
