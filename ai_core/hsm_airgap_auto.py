import os
import shutil
import getpass


from typing import Optional

def export_share_to_hsm(share: str, hsm_dir: Optional[str] = None) -> str:
    """
    Export a key share to a simulated HSM (directory or hardware token mount).
    Args:
        share: The key share string to export.
        hsm_dir: Optional HSM directory path. If None, uses default.
    Returns:
        The filename of the exported key share.
    """
    if hsm_dir is None:
        hsm_dir = f"/tmp/hsm_{getpass.getuser()}"  # Simulated HSM mount
    os.makedirs(hsm_dir, exist_ok=True)
    fname = os.path.join(hsm_dir, f"emma_share_{os.urandom(4).hex()}.key")
    with open(fname, "w") as f:
        f.write(share)
    print(f"[HSM] Exported share to {fname}")
    return fname


def airgap_transfer(file_path: str, dest_dir: Optional[str] = None) -> str:
    """
    Transfer a file to a simulated air-gapped destination.
    Args:
        file_path: Path to the file to transfer.
        dest_dir: Optional destination directory. If None, uses default.
    Returns:
        The destination path of the copied file.
    """
    if dest_dir is None:
        dest_dir = f"/tmp/airgap_{getpass.getuser()}"
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, os.path.basename(file_path))
    shutil.copy2(file_path, dest)
    print(f"[AIRGAP] Copied {file_path} to {dest}")
    return dest
