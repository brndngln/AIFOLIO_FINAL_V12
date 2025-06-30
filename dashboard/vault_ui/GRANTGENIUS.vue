<template>
  <div class="vault-ui grantgenius">
    <h1>🏆 GRANTGENIUS™</h1>
    <p>Grant Writing & Budget Generator</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: 'GRANTGENIUS' };
</script>
<style scoped>
.vault-ui.grantgenius { background: rgba(20,20,20,0.8); border-radius: 18px; box-shadow: 0 0 24px #00ffd0; color: #fff; padding: 2rem; }
h1 { text-shadow: 0 0 8px #00ffd0; }
</style>
