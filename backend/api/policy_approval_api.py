from fastapi import APIRouter, Body
from pathlib import Path
import json
from datetime import datetime

APPROVAL_PATH = Path(__file__).parent.parent.parent / 'logs' / 'policy_approvals.json'

router = APIRouter()

@router.post('/api/policy/submit_for_approval')
def submit_for_approval(data: dict = Body(...)):
    rec = data.get('recommendation')
    submitter = data.get('submitter')
    record = {
        'recommendation': rec,
        'submitter': submitter,
        'status': 'pending',
        'approvals': [],
        'rejections': [],
        'submitted_at': datetime.utcnow().isoformat()
    }
    if APPROVAL_PATH.exists():
        with open(APPROVAL_PATH, 'r') as f:
            approvals = json.load(f)
    else:
        approvals = []
    approvals.append(record)
    with open(APPROVAL_PATH, 'w') as f:
        json.dump(approvals, f, indent=2)
    return {'success': True, 'record': record}

@router.post('/api/policy/approve')
def approve_policy(data: dict = Body(...)):
    idx = data.get('idx')
    reviewer = data.get('reviewer')
    if APPROVAL_PATH.exists():
        with open(APPROVAL_PATH, 'r') as f:
            approvals = json.load(f)
    else:
        return {'success': False, 'error': 'No approvals'}
    if idx is not None and 0 <= idx < len(approvals):
        approvals[idx]['approvals'].append({'reviewer': reviewer, 'timestamp': datetime.utcnow().isoformat()})
        # If 2+ approvals, status becomes 'approved'
        if len(approvals[idx]['approvals']) >= 2:
            approvals[idx]['status'] = 'approved'
        with open(APPROVAL_PATH, 'w') as f:
            json.dump(approvals, f, indent=2)
        return {'success': True, 'record': approvals[idx]}
    return {'success': False, 'error': 'Invalid index'}

@router.post('/api/policy/reject')
def reject_policy(data: dict = Body(...)):
    idx = data.get('idx')
    reviewer = data.get('reviewer')
    reason = data.get('reason')
    if APPROVAL_PATH.exists():
        with open(APPROVAL_PATH, 'r') as f:
            approvals = json.load(f)
    else:
        return {'success': False, 'error': 'No approvals'}
    if idx is not None and 0 <= idx < len(approvals):
        approvals[idx]['rejections'].append({'reviewer': reviewer, 'reason': reason, 'timestamp': datetime.utcnow().isoformat()})
        # If 2+ rejections, status becomes 'rejected'
        if len(approvals[idx]['rejections']) >= 2:
            approvals[idx]['status'] = 'rejected'
        with open(APPROVAL_PATH, 'w') as f:
            json.dump(approvals, f, indent=2)
        return {'success': True, 'record': approvals[idx]}
    return {'success': False, 'error': 'Invalid index'}

@router.get('/api/policy/approvals')
def list_approvals():
    if APPROVAL_PATH.exists():
        with open(APPROVAL_PATH, 'r') as f:
            return json.load(f)
    return []
