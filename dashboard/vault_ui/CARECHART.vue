<template>
  <div class="vault-ui carechart">
    <h1>💖 CARECHART™</h1>
    <p>Health Tracker & Wellness Journal Builder</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: "CARECHART" };
</script>
<style scoped>
.vault-ui.carechart {
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
