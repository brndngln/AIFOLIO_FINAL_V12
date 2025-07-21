<template>
  <div class="vault-selector">
    <div class="header">
      <img src="/assets/aifolio_elite.svg" class="elite-logo" />
      <span class="elite-label">AIFOLIO™ OMNIELITE</span>
      <span class="phase-badge">Phase: OMNIELITE</span>
    </div>
    <div class="vault-list">
      <div
        v-for="vault in vaults"
        :key="vault.id"
        class="vault-card"
        :class="{ active: vault.id === selectedVault }"
        @click="selectVault(vault.id)"
        @mouseenter="hoverVault = vault.id"
        @mouseleave="hoverVault = null"
      >
        <span class="vault-icon" v-html="vault.icon"></span>
        <span class="vault-label">{{ vault.label }}</span>
        <transition name="fade">
          <span v-if="hoverVault === vault.id" class="vault-desc">
            {{ getVaultDescription(vault.id) }}
          </span>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import vaultRegistry from "@/config/vault_registry.json";

export default {
  name: "VaultSelector",
  data() {
    return {
      vaults: vaultRegistry,
      selectedVault: vaultRegistry[0].id,
      hoverVault: null,
    };
  },
  methods: {
    selectVault(id) {
      this.selectedVault = id;
      this.$emit("vault-selected", id);
    },
    getVaultDescription(id) {
      const desc = {
        templiq_templates:
          "Generate templates, courses, planners, and export in multiple formats.",
        therapiq_therapy:
          "Personalized therapy frameworks, journaling, and emotional mapping.",
        ritualux_rituals:
          "Design spiritual rituals, ceremonies, and visual altar layouts.",
        talentvault_explorer:
          "Discover talents, hobbies, and create personalized growth maps.",
        rebelremedy_recipes:
          "Build wellness kits, herbal blends, and printable remedy guides.",
        contentdrop_network:
          "Autonomous content drops, scheduling, and subscription management.",
        templatevault_hub:
          "Mega-library, drag-and-drop builder, and licensing for templates.",
      };
      return desc[id] || "";
    },
  },
};
</script>

<style scoped>
.vault-selector {
  background: rgba(24, 24, 32, 0.97);
  border-radius: 2.5rem;
  box-shadow:
    0 8px 40px 0 #00ffe7a0,
    0 1.5px 5px #000a;
  padding: 2rem 2.5rem;
  margin: 2rem auto;
  max-width: 900px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.header {
  display: flex;
  align-items: center;
  gap: 1.2rem;
  margin-bottom: 2.5rem;
}
.elite-logo {
  height: 48px;
}
.elite-label {
  font-family: "elite_sans", sans-serif;
  font-size: 2.1rem;
  letter-spacing: 0.08em;
  color: #00ffe7;
  font-weight: 800;
  text-shadow: 0 0 12px #00ffe7a0;
}
.phase-badge {
  background: #222;
  color: #fff;
  border-radius: 1rem;
  padding: 0.2rem 1.1rem;
  font-size: 1rem;
  margin-left: auto;
  font-weight: 600;
  letter-spacing: 0.07em;
}
.vault-list {
  display: flex;
  flex-wrap: wrap;
  gap: 2.2rem;
  justify-content: center;
  width: 100%;
}
.vault-card {
  background: linear-gradient(120deg, #181c2f 80%, #00ffe7 120%);
  border-radius: 1.7rem;
  box-shadow: 0 2px 12px #00ffe744;
  padding: 1.7rem 2.2rem;
  min-width: 170px;
  min-height: 110px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition:
    box-shadow 0.16s,
    transform 0.13s;
  position: relative;
  font-family: "elite_sans", sans-serif;
}
.vault-card.active,
.vault-card:hover {
  box-shadow:
    0 4px 24px #00ffe7a0,
    0 1.5px 5px #000a;
  transform: translateY(-4px) scale(1.045);
  background: linear-gradient(120deg, #00ffe7 10%, #181c2f 100%);
}
.vault-icon {
  font-size: 2.5rem;
  margin-bottom: 0.8rem;
  text-shadow: 0 0 12px #00ffe7a0;
}
.vault-label {
  font-size: 1.13rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.04em;
}
.vault-desc {
  position: absolute;
  bottom: -2.5rem;
  left: 50%;
  transform: translateX(-50%);
  background: #222c;
  color: #fff;
  border-radius: 1rem;
  padding: 0.6rem 1.4rem;
  font-size: 0.98rem;
  white-space: nowrap;
  box-shadow: 0 2px 8px #00ffe7a0;
  pointer-events: none;
  z-index: 10;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.17s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
