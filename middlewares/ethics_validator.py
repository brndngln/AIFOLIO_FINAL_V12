"""
Middleware: Ethics Validator
Wraps all logic processors and filters outputs through the OMNIELITE Ethics Engine before rendering.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ethics_engine import OmnieliteEthicsEngine, EthicsViolation

def ethics_validator(action, context):
    try:
        OmnieliteEthicsEngine.enforce(action, context)
        return True
<<<<<<< HEAD
    except EthicsViolation as e:
=======
    except EthicsViolation:
>>>>>>> omni_repair_backup_20250704_1335
        # Output is blocked, EMMA will handle
        return False
