// OMNIELITE PDF Builder: Elite formatting, style auto-tuning, and image support
import jsPDF from 'jspdf';
import { getVaultTheme } from './style_tuner.js';

export function buildPDF({ content, vaultId, style }) {
  const doc = new jsPDF();
  const theme = getVaultTheme(vaultId, style);
  doc.setFont(theme.font || 'helvetica');
  doc.setTextColor(theme.textColor || '#111');
  doc.setFillColor(theme.bgColor || '#fff');
  doc.text(content.title, 20, 20, { maxWidth: 170 });
  doc.text(content.body, 20, 40, { maxWidth: 170 });
  // Add branding/cover if present
  if (content.coverImg) doc.addImage(content.coverImg, 'PNG', 140, 10, 50, 50);
  // Apply elite style (rounded corners, watermark, etc.)
  // ...
  return doc;
}
