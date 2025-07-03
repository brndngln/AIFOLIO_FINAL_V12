<template>
  <div class="vault-ui templatehub">
    <h2>TEMPLATEHUB™ — AI Template Vault + Licensing Hub</h2>
    <form @submit.prevent="generate">
      <input v-model="niche" placeholder="Enter niche (e.g. Business, Design)" required />
      <input v-model="userId" placeholder="Enter your User ID" required />
      <button type="submit">Generate Template Bundle</button>
    </form>
    <div v-if="result">
      <a :href="result.pdfUrl" target="_blank">Download PDF</a>
      <div class="license-key">License Key: <span>{{ result.licenseKey }}</span></div>
    </div>
  </div>
</template>

<script>
import { generateTemplateBundle } from '@/vaults/templatevault_hub/logic.js'

export default {
  data() {
    return {
      niche: '',
      userId: '',
      result: null
    }
  },
  methods: {
    async generate() {
      const { pdf, licenseKey } = await generateTemplateBundle({ niche: this.niche, userId: this.userId })
      this.result = {
        pdfUrl: URL.createObjectURL(pdf.output('blob')),
        licenseKey
      }
    }
  }
}
</script>

<style scoped>
.vault-ui.templatehub {
  background: linear-gradient(120deg, #181c2f 80%, #00ffe7 120%);
  border-radius: 2.5rem;
  box-shadow: 0 8px 40px 0 #00ffe7a0, 0 1.5px 5px #000a;
  padding: 2rem 2.5rem;
  margin: 2rem auto;
  max-width: 600px;
  color: #fff;
  font-family: 'elite_sans', sans-serif;
}
input {
  padding: 0.7rem 1.2rem;
  border-radius: 1rem;
  border: none;
  margin-right: 1rem;
  font-size: 1.1rem;
}
button {
  background: #00ffe7;
  color: #181c2f;
  border: none;
  border-radius: 1rem;
  padding: 0.7rem 1.5rem;
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  box-shadow: 0 2px 8px #00ffe7a0;
}
.license-key {
  margin-top: 1.2rem;
  font-size: 1.09rem;
  background: #222c;
  border-radius: 1rem;
  padding: 0.7rem 1.2rem;
  color: #00ffe7;
  font-family: monospace;
  box-shadow: 0 2px 8px #00ffe7a0;
}
</style>
