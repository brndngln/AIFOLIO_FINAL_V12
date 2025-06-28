<template>
  <div class="vault-ui eventcraft">
    <h1>🎉 EVENTCRAFT™</h1>
    <p>Event & Wedding Planner Vault</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: 'EVENTCRAFT' };
</script>
<style scoped>
.vault-ui.eventcraft { background: rgba(24,28,47,0.85); border-radius: 18px; box-shadow: 0 0 24px #00ffd0; color: #fff; padding: 2rem; }
h1 { text-shadow: 0 0 8px #00ffd0; }
</style>
