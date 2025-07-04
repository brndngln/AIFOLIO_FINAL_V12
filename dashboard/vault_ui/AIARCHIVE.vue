<template>
  <div class="vault-ui aiarchive">
    <h1>🗃️ AIARCHIVE™</h1>
    <p>Automated Ebook + Resource Pack Creator</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: 'AIARCHIVE' };
</script>
<style scoped>
.vault-ui.aiarchive { background: rgba(20,20,20,0.8); border-radius: 18px; box-shadow: 0 0 24px #00ffd0; color: #fff; padding: 2rem; }
h1 { text-shadow: 0 0 8px #00ffd0; }
</style>
