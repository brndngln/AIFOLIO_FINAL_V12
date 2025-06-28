// OMNIELITE Embedded QR Generator
import QRCode from 'qrcode';

export function generateQR(text) {
  return QRCode.toDataURL(text);
}
