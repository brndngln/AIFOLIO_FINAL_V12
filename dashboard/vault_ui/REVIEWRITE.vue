<template>
  <div class="vault-ui reviewrite">
    <h1>📝 REVIEWRITE™</h1>
    <p>Affiliate Product Review Generator</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: 'REVIEWRITE' };
</script>
<style scoped>
.vault-ui.reviewrite { background: rgba(24,28,47,0.85); border-radius: 18px; box-shadow: 0 0 24px #00ffd0; color: #fff; padding: 2rem; }
h1 { text-shadow: 0 0 8px #00ffd0; }
</style>
