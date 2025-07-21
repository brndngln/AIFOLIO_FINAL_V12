<template>
  <div class="vault-ui wisdomvault">
    <h1>💡 WISDOMVAULT™</h1>
    <p>AI Life Wisdom + Reflection Vault</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: "WISDOMVAULT" };
</script>
<style scoped>
.vault-ui.wisdomvault {
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
