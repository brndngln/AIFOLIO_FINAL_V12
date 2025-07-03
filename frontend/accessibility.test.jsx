import React from 'react';
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import HiddenMuseHaven from './muse_haven/HiddenMuseHaven.jsx';

expect.extend(toHaveNoViolations);

test('HiddenMuseHaven is accessible', async () => {
  const { container } = render(<HiddenMuseHaven />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
