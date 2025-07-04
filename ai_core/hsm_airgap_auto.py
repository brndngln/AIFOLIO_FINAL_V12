import os
import shutil
import getpass

def export_share_to_hsm(share, hsm_dir=None):
    """Export a key share to a simulated HSM (directory or hardware token mount)."""
    if hsm_dir is None:
        hsm_dir = f"/tmp/hsm_{getpass.getuser()}"  # Simulated HSM mount
    os.makedirs(hsm_dir, exist_ok=True)
    fname = os.path.join(hsm_dir, f"emma_share_{os.urandom(4).hex()}.key")
    with open(fname, 'w') as f:
        f.write(share)
    print(f"[HSM] Exported share to {fname}")
    return fname

def airgap_transfer(file_path, dest_dir=None):
    """Transfer a file to a simulated air-gapped destination."""
    if dest_dir is None:
        dest_dir = f"/tmp/airgap_{getpass.getuser()}"
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, os.path.basename(file_path))
    shutil.copy2(file_path, dest)
    print(f"[AIRGAP] Copied {file_path} to {dest}")
    return dest
