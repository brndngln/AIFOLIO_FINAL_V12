from fastapi import APIRouter, Body
from pathlib import Path
import json
from datetime import datetime
import random

APPROVAL_PATH = Path(__file__).parent.parent.parent / 'logs' / 'policy_approvals.json'
REVIEWERS_PATH = Path(__file__).parent.parent.parent / 'config' / 'reviewers.json'

router = APIRouter()

@router.post('/api/reviewer/assign')
def assign_reviewers(data: dict = Body(...)):
    idx = data.get('idx')
    num_reviewers = data.get('num_reviewers', 2)
    if REVIEWERS_PATH.exists():
        with open(REVIEWERS_PATH, 'r') as f:
            reviewers = json.load(f)
    else:
        return {'success': False, 'error': 'No reviewers configured'}
    if APPROVAL_PATH.exists():
        with open(APPROVAL_PATH, 'r') as f:
            approvals = json.load(f)
    else:
        return {'success': False, 'error': 'No approvals'}
    if idx is not None and 0 <= idx < len(approvals):
        assigned = random.sample(reviewers, min(num_reviewers, len(reviewers)))
        approvals[idx]['assigned_reviewers'] = assigned
        approvals[idx]['assignment_time'] = datetime.utcnow().isoformat()
        with open(APPROVAL_PATH, 'w') as f:
            json.dump(approvals, f, indent=2)
        return {'success': True, 'assigned': assigned, 'record': approvals[idx]}
    return {'success': False, 'error': 'Invalid index'}

@router.get('/api/reviewer/list')
def list_reviewers():
    if REVIEWERS_PATH.exists():
        with open(REVIEWERS_PATH, 'r') as f:
            return json.load(f)
    return []
