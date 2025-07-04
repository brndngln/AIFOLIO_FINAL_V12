<template>
  <div class="vault-ui policygen">
    <h1>📜 POLICYGEN™</h1>
    <p>SOP + Company Policy Vault</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: 'POLICYGEN' };
</script>
<style scoped>
.vault-ui.policygen { background: rgba(20,20,20,0.8); border-radius: 18px; box-shadow: 0 0 24px #00ffd0; color: #fff; padding: 2rem; }
h1 { text-shadow: 0 0 8px #00ffd0; }
</style>
