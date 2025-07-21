<template>
  <div class="vault-ui ai-mentor">
    <h1>👨‍🎓 AI-MENTOR™</h1>
    <p>Youth Motivation + Study Guide Vault</p>
    <slot></slot>
  </div>
</template>
<script>
export default { name: "AI_MENTOR" };
</script>
<style scoped>
.vault-ui.ai-mentor {
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
