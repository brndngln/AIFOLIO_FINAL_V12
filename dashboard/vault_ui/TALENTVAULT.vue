<template>
  <div class="vault-ui talentvault">
    <h2>TALENTVAULT™ — Hobby Uncoverer & Talent Explorer</h2>
    <form @submit.prevent="generate">
      <input
        v-model="user_profile"
        placeholder="Describe yourself (e.g. I love puzzles and music)"
        required
      />
      <button type="submit">Discover Talents</button>
    </form>
    <div v-if="pdfUrl">
      <a :href="pdfUrl" target="_blank">Download PDF</a>
    </div>
  </div>
</template>

<script>
import { generateTalentMap } from "@/vaults/talentvault_explorer/logic.js";

export default {
  data() {
    return {
      user_profile: "",
      pdfUrl: null,
    };
  },
  methods: {
    async generate() {
      const pdf = await generateTalentMap({ user_profile: this.user_profile });
      this.pdfUrl = URL.createObjectURL(pdf.output("blob"));
    },
  },
};
</script>

<style scoped>
.vault-ui.talentvault {
  background: linear-gradient(120deg, #181c2f 80%, #00ffe7 120%);
  border-radius: 2.5rem;
  box-shadow:
    0 8px 40px 0 #00ffe7a0,
    0 1.5px 5px #000a;
  padding: 2rem 2.5rem;
  margin: 2rem auto;
  max-width: 600px;
  color: #fff;
  font-family: "elite_sans", sans-serif;
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
</style>
