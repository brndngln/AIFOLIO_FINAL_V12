import json
import datetime
import os

TUNER_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/style_voice_tuner_log.jsonl'))
os.makedirs(os.path.dirname(TUNER_LOG), exist_ok=True)

# Example preset enforcement
STYLE_PRESETS = {
    'friendly': {'greeting': 'Hi there!', 'closing': 'Best regards,'},
    'formal': {'greeting': 'Dear Customer,', 'closing': 'Sincerely,'},
    'energetic': {'greeting': 'Hey!', 'closing': 'Let’s go!'}
}

def tune_output_style(text, preset='friendly'):
    preset_data = STYLE_PRESETS.get(preset, STYLE_PRESETS['friendly'])
    # Enforce preset greeting/closing
    lines = text.split('\n')
    if lines:
        lines[0] = preset_data['greeting']
        if len(lines) > 1:
            lines[-1] = preset_data['closing']
    tuned = '\n'.join(lines)
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'original': text,
        'preset': preset,
        'tuned': tuned
    }
    with open(TUNER_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return tuned

if __name__ == "__main__":
    print(tune_output_style('Hello!\nThank you for your purchase.\nRegards,', 'formal'))
