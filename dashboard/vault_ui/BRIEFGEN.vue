<template>
  <div class="vault-ui briefgen">
    <h1>📣 BRIEFGEN™</h1>
    <p>AI PR & Press Kit Generator</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: "BRIEFGEN" };
</script>
<style scoped>
.vault-ui.briefgen {
  background: rgba(24, 28, 47, 0.85);
  border-radius: 18px;
  box-shadow: 0 0 24px #00ffd0;
  color: #fff;
  padding: 2rem;
}
h1 {
  text-shadow: 0 0 8px #00ffd0;
}
</style>
