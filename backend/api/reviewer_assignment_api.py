<<<<<<< HEAD
from fastapi import APIRouter, Body
from pathlib import Path
import json
from datetime import datetime
import random
=======
from fastapi import APIRouter
from pathlib import Path
>>>>>>> omni_repair_backup_20250704_1335

APPROVAL_PATH = Path(__file__).parent.parent.parent / 'logs' / 'policy_approvals.json'
REVIEWERS_PATH = Path(__file__).parent.parent.parent / 'config' / 'reviewers.json'

router = APIRouter()

from backend.compliance.reviewer_assignment import assign_all_open_violations, reviewer_leaderboard

@router.post('/api/reviewer/assign_all')
def assign_all():
    """
    Assign reviewers to all open violations (auto, by expertise, load, accuracy)
    """
    return assign_all_open_violations()

@router.get('/api/reviewer/leaderboard')
def leaderboard():
    """
    Reviewer leaderboard with stats and badges
    """
    return reviewer_leaderboard()
