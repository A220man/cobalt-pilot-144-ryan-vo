import yaml

with open('bio-research/skills/nextflow-development/scripts/config/pipelines/sarek.yaml', 'r') as f:
    config = yaml.safe_load(f)

print('validation:', config.get('validation'))
print('conditional_required:', config.get('validation', {}).get('conditional_required'))
print('type of conditional_required:', type(config.get('validation', {}).get('conditional_required')))
if config.get('validation', {}).get('conditional_required'):
    for k, v in config.get('validation', {}).get('conditional_required').items():
        print(f'  key: "{k}" (type: {type(k)}), value: {v}')

