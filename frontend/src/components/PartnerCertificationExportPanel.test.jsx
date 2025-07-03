import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import PartnerCertificationExportPanel from "./PartnerCertificationExportPanel";

// Mock localStorage
beforeEach(() => {
  window.localStorage.clear();
  window.localStorage.setItem("token", "header.eyJleHAiOjQ3MzIzMzg0MDB9.signature"); // valid far future exp
});

describe("PartnerCertificationExportPanel", () => {
  it("renders JWT badge and DPA link", () => {
    render(<PartnerCertificationExportPanel />);
    expect(screen.getByText(/JWT/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Data Processing Agreement/i })).toBeInTheDocument();
  });

  it("shows toast on template save", () => {
    render(<PartnerCertificationExportPanel />);
    window.prompt = jest.fn(() => "TestTemplate");
    fireEvent.click(screen.getByRole("button", { name: /Save current field selection as template/i }));
    expect(screen.getByText(/Template saved/i)).toBeInTheDocument();
  });

  it("opens and copies audit log details", async () => {
    render(<PartnerCertificationExportPanel />);
    const auditRow = screen.getAllByRole("listitem")[0];
    fireEvent.click(auditRow);
    expect(await screen.findByText(/Audit Log Details/i)).toBeInTheDocument();
    const copyBtn = screen.getByRole("button", { name: /Copy to Clipboard/i });
    Object.assign(navigator, { clipboard: { writeText: jest.fn() } });
    fireEvent.click(copyBtn);
    expect(await screen.findByText(/Copied to clipboard/i)).toBeInTheDocument();
  });

  it("shows schedule recurrence options", () => {
    render(<PartnerCertificationExportPanel />);
    fireEvent.click(screen.getByRole("button", { name: /Add Schedule/i }));
    expect(screen.getByLabelText(/Recurrence/i)).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText(/Recurrence/i), { target: { value: "weekly" } });
    expect(screen.getByPlaceholderText(/Day of Week/i)).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText(/Recurrence/i), { target: { value: "monthly" } });
    expect(screen.getByPlaceholderText(/Day of Month/i)).toBeInTheDocument();
  });

  it("shows bulk action buttons and disables during loading", async () => {
    render(<PartnerCertificationExportPanel />);
    // Select all partners
    const selectAll = screen.getByLabelText(/Select all partners/i);
    fireEvent.click(selectAll);
    const bulkCsv = screen.getByRole("button", { name: /Bulk Export CSV/i });
    fireEvent.click(bulkCsv);
    expect(bulkCsv).toBeDisabled();
    await waitFor(() => expect(bulkCsv).not.toBeDisabled(), { timeout: 2000 });
  });

  it("renders with dark mode styles", () => {
    window.matchMedia = jest.fn().mockReturnValue({ matches: true, addEventListener: jest.fn(), removeEventListener: jest.fn() });
    render(<PartnerCertificationExportPanel />);
    expect(document.body.innerHTML).toMatch(/radial-gradient/);
  });

  it("renders accessibility labels and ARIA roles", () => {
    render(<PartnerCertificationExportPanel />);
    expect(screen.getByLabelText(/Partner Certification Export/i)).toBeInTheDocument();
    expect(screen.getByRole("dialog")).toBeInTheDocument();
  });
});
