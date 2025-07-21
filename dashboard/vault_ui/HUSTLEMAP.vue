<template>
  <div class="vault-ui hustlemap">
    <h1>🗺️ HUSTLEMAP™</h1>
    <p>Small Business Blueprint Generator</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: "HUSTLEMAP" };
</script>
<style scoped>
.vault-ui.hustlemap {
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
