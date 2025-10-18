# Component Documentation Template

## Component Name

Brief description of what this component does.

### Usage

```tsx
import { ComponentName } from './ComponentName';

<ComponentName prop1="value1" prop2="value2" />
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| prop1 | string | - | Description of prop1 |
| prop2 | boolean | false | Description of prop2 |

### Examples

#### Basic Usage
```tsx
<ComponentName />
```

#### With Props
```tsx
<ComponentName prop1="custom value" prop2={true} />
```

### Accessibility

- Describe accessibility features
- Keyboard navigation support
- Screen reader compatibility

### Testing

```tsx
import { render, screen } from '@testing-library/react';
import { ComponentName } from './ComponentName';

test('renders component correctly', () => {
  render(<ComponentName />);
  expect(screen.getByRole('button')).toBeInTheDocument();
});
```
