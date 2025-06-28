<template>
  <div class="vault-ui traffiq">
    <h1>🚦 TRAFFIQ™</h1>
    <p>Ad Traffic & Funnel Routing Engine</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: 'TRAFFIQ' };
</script>
<style scoped>
.vault-ui.traffiq { background: rgba(24,28,47,0.85); border-radius: 18px; box-shadow: 0 0 24px #00ffd0; color: #fff; padding: 2rem; }
h1 { text-shadow: 0 0 8px #00ffd0; }
</style>
