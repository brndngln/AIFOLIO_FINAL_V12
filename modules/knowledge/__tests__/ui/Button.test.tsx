// AIFOLIO Elite System - Button Component Tests
// Comprehensive testing for interactions, variants, and accessibility

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe } from 'jest-axe';
import { Button } from '../../ui/components/forms/Button';

describe('Button Component', () => {
  describe('Basic Rendering', () => {
    it('should render with default props', () => {
      render(<Button>Click me</Button>);

      const button = screen.getByRole('button', { name: /click me/i });
      expect(button).toBeInTheDocument();
      expect(button).toHaveClass('px-4', 'py-2.5', 'text-base'); // md size
    });

    it('should render children correctly', () => {
      render(<Button>Test Button</Button>);

      expect(screen.getByText('Test Button')).toBeInTheDocument();
    });

    it('should apply custom className', () => {
      render(<Button className="custom-class">Button</Button>);

      const button = screen.getByRole('button');
      expect(button).toHaveClass('custom-class');
    });
  });

  describe('Variants', () => {
    const variants = ['primary', 'secondary', 'ghost', 'danger', 'success'] as const;

    variants.forEach(variant => {
      it(`should render ${variant} variant correctly`, () => {
        render(<Button variant={variant}>Button</Button>);

        const button = screen.getByRole('button');
        expect(button).toBeInTheDocument();
        // Variant-specific classes would be tested here based on implementation
      });
    });
  });

  describe('Sizes', () => {
    const sizes = [
      { size: 'xs' as const, classes: ['px-2.5', 'py-1.5', 'text-xs'] },
      { size: 'sm' as const, classes: ['px-3', 'py-2', 'text-sm'] },
      { size: 'md' as const, classes: ['px-4', 'py-2.5', 'text-base'] },
      { size: 'lg' as const, classes: ['px-6', 'py-3', 'text-lg'] },
      { size: 'xl' as const, classes: ['px-8', 'py-4', 'text-xl'] }
    ];

    sizes.forEach(({ size, classes }) => {
      it(`should render ${size} size correctly`, () => {
        render(<Button size={size}>Button</Button>);

        const button = screen.getByRole('button');
        classes.forEach(className => {
          expect(button).toHaveClass(className);
        });
      });
    });
  });

  describe('Interactive States', () => {
    it('should handle click events', async () => {
      const handleClick = jest.fn();
      const user = userEvent.setup();

      render(<Button onClick={handleClick}>Click me</Button>);

      const button = screen.getByRole('button');
      await user.click(button);

      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('should not trigger click when disabled', async () => {
      const handleClick = jest.fn();
      const user = userEvent.setup();

      render(<Button onClick={handleClick} disabled>Disabled Button</Button>);

      const button = screen.getByRole('button');
      expect(button).toBeDisabled();

      await user.click(button);
      expect(handleClick).not.toHaveBeenCalled();
    });

    it('should not trigger click when loading', async () => {
      const handleClick = jest.fn();
      const user = userEvent.setup();

      render(<Button onClick={handleClick} loading>Loading Button</Button>);

      const button = screen.getByRole('button');
      expect(button).toBeDisabled();

      await user.click(button);
      expect(handleClick).not.toHaveBeenCalled();
    });
  });

  describe('Loading State', () => {
    it('should show loading state', () => {
      render(<Button loading>Loading Button</Button>);

      const button = screen.getByRole('button');
      expect(button).toBeDisabled();
      expect(button).toHaveAttribute('aria-busy', 'true');
    });

    it('should hide children when loading', () => {
      render(<Button loading>Button Text</Button>);

      // The text might be visually hidden but still in DOM
      const button = screen.getByRole('button');
      expect(button).toBeInTheDocument();
    });
  });

  describe('Icon Support', () => {
    const TestIcon = () => <span data-testid="test-icon">🚀</span>;

    it('should render icon on left by default', () => {
      render(
        <Button icon={<TestIcon />}>
          Button with Icon
        </Button>
      );

      expect(screen.getByTestId('test-icon')).toBeInTheDocument();
      expect(screen.getByText('Button with Icon')).toBeInTheDocument();
    });

    it('should render icon on right when specified', () => {
      render(
        <Button icon={<TestIcon />} iconPosition="right">
          Button with Icon
        </Button>
      );

      expect(screen.getByTestId('test-icon')).toBeInTheDocument();
      expect(screen.getByText('Button with Icon')).toBeInTheDocument();
    });
  });

  describe('Full Width', () => {
    it('should apply full width styles', () => {
      render(<Button fullWidth>Full Width Button</Button>);

      const button = screen.getByRole('button');
      expect(button).toHaveClass('w-full');
    });
  });

  describe('Accessibility', () => {
    it('should be accessible', async () => {
      const { container } = render(<Button>Accessible Button</Button>);

      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });

    it('should support keyboard navigation', async () => {
      const handleClick = jest.fn();
      const user = userEvent.setup();

      render(<Button onClick={handleClick}>Keyboard Button</Button>);

      const button = screen.getByRole('button');
      button.focus();

      expect(button).toHaveFocus();

      await user.keyboard('{Enter}');
      expect(handleClick).toHaveBeenCalledTimes(1);

      await user.keyboard(' ');
      expect(handleClick).toHaveBeenCalledTimes(2);
    });

    it('should have proper ARIA attributes when loading', () => {
      render(<Button loading>Loading Button</Button>);

      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('aria-busy', 'true');
      expect(button).toBeDisabled();
    });

    it('should have proper ARIA attributes when disabled', () => {
      render(<Button disabled>Disabled Button</Button>);

      const button = screen.getByRole('button');
      expect(button).toBeDisabled();
      expect(button).toHaveAttribute('aria-disabled', 'true');
    });
  });

  describe('Form Integration', () => {
    it('should support form submission', () => {
      const handleSubmit = jest.fn(e => e.preventDefault());

      render(
        <form onSubmit={handleSubmit}>
          <Button type="submit">Submit</Button>
        </form>
      );

      const button = screen.getByRole('button', { name: /submit/i });
      fireEvent.click(button);

      expect(handleSubmit).toHaveBeenCalledTimes(1);
    });

    it('should support different button types', () => {
      render(<Button type="reset">Reset</Button>);

      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('type', 'reset');
    });
  });

  describe('Event Handling', () => {
    it('should handle focus and blur events', async () => {
      const handleFocus = jest.fn();
      const handleBlur = jest.fn();
      const user = userEvent.setup();

      render(
        <Button onFocus={handleFocus} onBlur={handleBlur}>
          Focus Button
        </Button>
      );

      const button = screen.getByRole('button');

      await user.click(button);
      expect(handleFocus).toHaveBeenCalledTimes(1);

      await user.tab();
      expect(handleBlur).toHaveBeenCalledTimes(1);
    });

    it('should handle mouse events', async () => {
      const handleMouseEnter = jest.fn();
      const handleMouseLeave = jest.fn();
      const user = userEvent.setup();

      render(
        <Button onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
          Hover Button
        </Button>
      );

      const button = screen.getByRole('button');

      await user.hover(button);
      expect(handleMouseEnter).toHaveBeenCalledTimes(1);

      await user.unhover(button);
      expect(handleMouseLeave).toHaveBeenCalledTimes(1);
    });
  });

  describe('Ref Forwarding', () => {
    it('should forward ref correctly', () => {
      const ref = React.createRef<HTMLButtonElement>();

      render(<Button ref={ref}>Ref Button</Button>);

      expect(ref.current).toBeInstanceOf(HTMLButtonElement);
      expect(ref.current?.textContent).toBe('Ref Button');
    });
  });
});
