<template>
  <div class="vault-ui nostalgia">
    <h1>📔 NOSTALGIA™</h1>
    <p>Memory Book & Tribute Generator</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: 'NOSTALGIA' };
</script>
<style scoped>
.vault-ui.nostalgia { background: rgba(24,28,47,0.85); border-radius: 18px; box-shadow: 0 0 24px #00ffd0; color: #fff; padding: 2rem; }
h1 { text-shadow: 0 0 8px #00ffd0; }
</style>
