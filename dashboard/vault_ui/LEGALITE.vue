<template>
  <div class="vault-ui legalite">
    <h1>⚖️ LEGALITE™</h1>
    <p>AI Legal Template & Contract Generator</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: "LEGALITE" };
</script>
<style scoped>
.vault-ui.legalite {
  background: rgba(20, 20, 20, 0.8);
  border-radius: 18px;
  box-shadow: 0 0 24px #00ffd0;
  color: #fff;
  padding: 2rem;
}
h1 {
  text-shadow: 0 0 8px #00ffd0;
}
</style>
