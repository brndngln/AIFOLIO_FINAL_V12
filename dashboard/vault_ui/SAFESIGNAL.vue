<template>
  <div class="vault-ui safesignal">
    <h1>🛡️ SAFESIGNAL™</h1>
    <p>AI Crisis Toolkit Generator</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: "SAFESIGNAL" };
</script>
<style scoped>
.vault-ui.safesignal {
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
