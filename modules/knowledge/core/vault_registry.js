// OMNIELITE AIFOLIO Vault Registry - Elite SAFE AI, High-Ticket, Modular
// This registry dynamically discovers, registers, and exposes all vaults for elite business workflows
// All logic is static, deterministic, owner-controlled, and fully auditable

const fs = require("fs");
const path = require("path");
const licenseManager = require("./license_manager");

const VAULTS_DIR = path.resolve(__dirname, "../vaults");

/**
 * Discover all vaults in the vaults directory and register their metadata.
 * Each vault must export a metadata.json file and static bundle logic.
 */
function discoverVaults() {
  const vaults = [];
  fs.readdirSync(VAULTS_DIR, { withFileTypes: true }).forEach((dirent) => {
    if (dirent.isDirectory()) {
      const vaultPath = path.join(VAULTS_DIR, dirent.name);
      const metaFile = path.join(vaultPath, "metadata.json");
      if (fs.existsSync(metaFile)) {
        const metadata = JSON.parse(fs.readFileSync(metaFile, "utf-8"));
        vaults.push({
          ...metadata,
          id: dirent.name,
          path: vaultPath,
          hasBundleGenerator: fs.existsSync(
            path.join(vaultPath, "bundle_generator.js"),
          ),
          hasLicense: metadata.licenseEnabled === true,
        });
      }
    }
  });
  return vaults;
}

/**
 * Get all registered vaults with full metadata and capabilities
 */
function getAllVaults() {
  return discoverVaults();
}

/**
 * Get a specific vault by ID
 */
function getVaultById(vaultId) {
  return getAllVaults().find((v) => v.id === vaultId);
}

/**
 * Generate a deterministic license key for a vault bundle (if enabled)
 */
function generateVaultLicenseKey(vaultId, userId) {
  const vault = getVaultById(vaultId);
  if (vault && vault.hasLicense) {
    return licenseManager.generateLicenseKey(userId, vaultId);
  }
  throw new Error("Vault does not support licensing or not found.");
}

/**
 * Validate a deterministic license key for a vault bundle (if enabled)
 */
function validateVaultLicenseKey(vaultId, key, userId) {
  const vault = getVaultById(vaultId);
  if (vault && vault.hasLicense) {
    return licenseManager.validateLicenseKey(key, userId, vaultId);
  }
  return false;
}

module.exports = {
  getAllVaults,
  getVaultById,
  generateVaultLicenseKey,
  validateVaultLicenseKey,
};
