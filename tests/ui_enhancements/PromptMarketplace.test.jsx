import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import PromptMarketplace from '../../dashboard/frontend/src/components/PromptMarketplace';

describe('PromptMarketplace', () => {
  it('renders marketplace table and filters', () => {
    render(<PromptMarketplace />);
    expect(screen.getByText('Prompt Marketplace')).toBeInTheDocument();
    expect(screen.getByText('Submit Prompt')).toBeInTheDocument();
    expect(screen.getByText('Elite prompt sets.')).toBeInTheDocument();
  });

  it('filters by status', () => {
    render(<PromptMarketplace />);
    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'approved' } });
    expect(screen.getByText('Approved')).toBeInTheDocument();
  });
});
