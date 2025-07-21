describe("Owner Control Center End-to-End", () => {
  it("should allow owner to toggle integrations, trigger lockdown, export logs, and run compliance audit", () => {
    cy.visit("/");
    cy.get('button[aria-label="Owner Control Center"]').click();
    cy.contains("Slack").parent().find('input[type="checkbox"]').check();
    cy.contains("Discord").parent().find('input[type="checkbox"]').check();
    cy.contains("Email").parent().find('input[type="checkbox"]').check();
    cy.contains("Rotate API Keys").click();
    cy.contains("Compliance Audit").click();
    cy.contains("Export Audit Log").click();
    cy.contains("Export Compliance Log").click();
    cy.contains("Emergency Lockdown").click();
    cy.contains("Confirm");
  });
});
