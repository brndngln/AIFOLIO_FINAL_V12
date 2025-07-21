<template>
  <div class="vault-ui dealdrip">
    <h1>💰 DEALDRIP™</h1>
    <p>Sales Page & Offer Stack Generator</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: "DEALDRIP" };
</script>
<style scoped>
.vault-ui.dealdrip {
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
