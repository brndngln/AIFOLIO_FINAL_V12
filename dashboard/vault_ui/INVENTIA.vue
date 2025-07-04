<template>
  <div class="vault-ui inventia">
    <h1>💡 INVENTIA™</h1>
    <p>Product Innovation + Startup Idea Vault</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: 'INVENTIA' };
</script>
<style scoped>
.vault-ui.inventia { background: rgba(20,20,20,0.8); border-radius: 18px; box-shadow: 0 0 24px #00ffd0; color: #fff; padding: 2rem; }
h1 { text-shadow: 0 0 8px #00ffd0; }
</style>
