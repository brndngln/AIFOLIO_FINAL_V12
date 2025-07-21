// OMNIELITE Drop Archive System: ZIP Export
import JSZip from "jszip";

export async function archiveDrops(drops) {
  const zip = new JSZip();
  drops.forEach((drop) => {
    zip.file(drop.filename, drop.content);
  });
  return await zip.generateAsync({ type: "blob" });
}
