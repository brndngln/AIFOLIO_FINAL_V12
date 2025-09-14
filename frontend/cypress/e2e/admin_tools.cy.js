describe("Admin Tools Panel", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("shows all admin tool tabs", () => {
    cy.contains("Admin Tools").should("exist");
    cy.contains("Audit Log").should("exist");
    cy.contains("Export History").should("exist");
    cy.contains("User Management").should("exist");
    cy.contains("Sessions").should("exist");
    cy.contains("SAFE AI Settings").should("exist");
  });

  it("can switch between tabs", () => {
    cy.contains("Export History").click();
    cy.contains("Export/Download History").should("exist");
    cy.contains("User Management").click();
    cy.contains("User/Partner Management").should("exist");
    cy.contains("Sessions").click();
    cy.contains("Active Sessions").should("exist");
    cy.contains("SAFE AI Settings").click();
    cy.contains("SAFE AI Compliance Settings").should("exist");
  });

  it("downloads audit log as CSV and JSON", () => {
    cy.contains("Audit Log").click();
    cy.contains("Download CSV").should("exist");
    cy.contains("Download JSON").should("exist");
  });

  it("downloads export history as CSV and JSON", () => {
    cy.contains("Export History").click();
    cy.contains("Download CSV").should("exist");
    cy.contains("Download JSON").should("exist");
  });

  it("can add and delete a user", () => {
    cy.contains("User Management").click();
    cy.get('input[aria-label="Username"]').type("testuser");
    cy.get('input[aria-label="Email"]').type("user@example.com");
    cy.get('input[aria-label="Organization"]').type("TestOrg");
    cy.get('button[type="submit"]').click();
    cy.contains("testuser").should("exist");
    cy.get('button[aria-label="Delete testuser"]').click();
    cy.contains("testuser").should("not.exist");
  });

  it("can change user role", () => {
    cy.contains("User Management").click();
    cy.get('select[aria-label^="Role for"]').first().select("admin");
    cy.get('select[aria-label^="Role for"]')
      .first()
      .should("have.value", "admin");
  });
});
