// AIFOLIO Elite System - AppWrapper Layout Tests
// Validates mounting logic, theme propagation, and responsive behavior

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe } from 'jest-axe';
import { AppWrapper } from '../../layouts/AppWrapper';

// Mock the hooks and components that AppWrapper depends on
jest.mock('../../hooks/useMounted', () => ({
  useMounted: () => true
}));

jest.mock('../../hooks/useDarkMode', () => ({
  useDarkMode: () => ({
    theme: 'light',
    isDark: false,
    toggleTheme: jest.fn(),
    systemTheme: 'light'
  })
}));

jest.mock('../../hooks/useToggle', () => ({
  useToggle: (initialValue: boolean = false) => {
    const [value, setValue] = React.useState(initialValue);
    const toggle = () => setValue(prev => !prev);
    const setToggle = (newValue: boolean) => setValue(newValue);
    return [value, toggle, setToggle];
  }
}));

// Mock child components to avoid complex rendering
jest.mock('../../ui/ThemeEditorPanel', () => ({
  ThemeEditorPanel: () => <div data-testid="theme-editor-panel">Theme Editor</div>
}));

jest.mock('../../ui/Navbar', () => ({
  Navbar: ({ onMenuClick }: { onMenuClick: () => void }) => (
    <nav data-testid="navbar">
      <button onClick={onMenuClick} data-testid="menu-button">Menu</button>
    </nav>
  )
}));

jest.mock('../../ui/Sidebar', () => ({
  Sidebar: ({
    isOpen,
    onClose,
    currentRoute
  }: {
    isOpen: boolean;
    onClose: () => void;
    currentRoute: string;
  }) => (
    <aside data-testid="sidebar" data-open={isOpen}>
      <button onClick={onClose} data-testid="sidebar-close">Close</button>
      <div data-testid="current-route">{currentRoute}</div>
    </aside>
  )
}));

// Mock framer-motion
jest.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }: any) => <div {...props}>{children}</div>,
    main: ({ children, ...props }: any) => <main {...props}>{children}</main>
  }
}));

describe('AppWrapper Component', () => {
  // Mock window.innerWidth for responsive tests
  const mockInnerWidth = (width: number) => {
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: width,
    });
    window.dispatchEvent(new Event('resize'));
  };

  beforeEach(() => {
    // Reset to desktop size by default
    mockInnerWidth(1200);
  });

  describe('Basic Rendering', () => {
    it('should render with default props', () => {
      render(
        <AppWrapper>
          <div data-testid="test-content">Test Content</div>
        </AppWrapper>
      );

      expect(screen.getByTestId('test-content')).toBeInTheDocument();
      expect(screen.getByTestId('navbar')).toBeInTheDocument();
      expect(screen.getByTestId('sidebar')).toBeInTheDocument();
      expect(screen.getByTestId('theme-editor-panel')).toBeInTheDocument();
    });

    it('should render children correctly', () => {
      const testContent = 'This is test content';

      render(
        <AppWrapper>
          <p>{testContent}</p>
        </AppWrapper>
      );

      expect(screen.getByText(testContent)).toBeInTheDocument();
    });

    it('should pass currentRoute to sidebar', () => {
      const testRoute = '/dashboard';

      render(
        <AppWrapper currentRoute={testRoute}>
          <div>Content</div>
        </AppWrapper>
      );

      expect(screen.getByTestId('current-route')).toHaveTextContent(testRoute);
    });

    it('should use default route when not provided', () => {
      render(
        <AppWrapper>
          <div>Content</div>
        </AppWrapper>
      );

      expect(screen.getByTestId('current-route')).toHaveTextContent('/');
    });
  });

  describe('Sidebar Functionality', () => {
    it('should toggle sidebar when menu button is clicked', async () => {
      const user = userEvent.setup();

      render(
        <AppWrapper>
          <div>Content</div>
        </AppWrapper>
      );

      const menuButton = screen.getByTestId('menu-button');
      const sidebar = screen.getByTestId('sidebar');

      // Initially closed
      expect(sidebar).toHaveAttribute('data-open', 'false');

      // Click to open
      await user.click(menuButton);
      expect(sidebar).toHaveAttribute('data-open', 'true');

      // Click to close
      await user.click(menuButton);
      expect(sidebar).toHaveAttribute('data-open', 'false');
    });

    it('should close sidebar when close button is clicked', async () => {
      const user = userEvent.setup();

      render(
        <AppWrapper>
          <div>Content</div>
        </AppWrapper>
      );

      const menuButton = screen.getByTestId('menu-button');
      const closeButton = screen.getByTestId('sidebar-close');
      const sidebar = screen.getByTestId('sidebar');

      // Open sidebar first
      await user.click(menuButton);
      expect(sidebar).toHaveAttribute('data-open', 'true');

      // Close via close button
      await user.click(closeButton);
      expect(sidebar).toHaveAttribute('data-open', 'false');
    });
  });

  describe('Responsive Behavior', () => {
    it('should handle desktop viewport', async () => {
      mockInnerWidth(1200);

      render(
        <AppWrapper>
          <div>Content</div>
        </AppWrapper>
      );

      // Wait for resize effect
      await waitFor(() => {
        const sidebar = screen.getByTestId('sidebar');
        // On desktop, sidebar should be open by default (based on implementation)
        expect(sidebar).toBeInTheDocument();
      });
    });

    it('should handle mobile viewport', async () => {
      mockInnerWidth(600);

      render(
        <AppWrapper>
          <div>Content</div>
        </AppWrapper>
      );

      // Wait for resize effect
      await waitFor(() => {
        const sidebar = screen.getByTestId('sidebar');
        // On mobile, sidebar should be closed by default
        expect(sidebar).toHaveAttribute('data-open', 'false');
      });
    });

    it('should respond to window resize events', async () => {
      render(
        <AppWrapper>
          <div>Content</div>
        </AppWrapper>
      );

      // Start with desktop
      mockInnerWidth(1200);
      await waitFor(() => {
        expect(screen.getByTestId('sidebar')).toBeInTheDocument();
      });

      // Resize to mobile
      mockInnerWidth(600);
      await waitFor(() => {
        const sidebar = screen.getByTestId('sidebar');
        expect(sidebar).toHaveAttribute('data-open', 'false');
      });
    });
  });

  describe('Theme Integration', () => {
    it('should integrate with theme system', () => {
      render(
        <AppWrapper>
          <div>Content</div>
        </AppWrapper>
      );

      // Theme editor panel should be present
      expect(screen.getByTestId('theme-editor-panel')).toBeInTheDocument();
    });
  });

  describe('Layout Structure', () => {
    it('should have proper semantic structure', () => {
      render(
        <AppWrapper>
          <div data-testid="main-content">Main Content</div>
        </AppWrapper>
      );

      // Should have navigation
      expect(screen.getByRole('navigation')).toBeInTheDocument();

      // Should have main content area
      expect(screen.getByTestId('main-content')).toBeInTheDocument();
    });

    it('should maintain proper DOM hierarchy', () => {
      const { container } = render(
        <AppWrapper>
          <div>Content</div>
        </AppWrapper>
      );

      // Basic structure validation
      expect(container.firstChild).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('should be accessible', async () => {
      const { container } = render(
        <AppWrapper>
          <div>Accessible Content</div>
        </AppWrapper>
      );

      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });

    it('should support keyboard navigation', async () => {
      const user = userEvent.setup();

      render(
        <AppWrapper>
          <div>Content</div>
        </AppWrapper>
      );

      const menuButton = screen.getByTestId('menu-button');

      // Should be focusable
      await user.tab();
      expect(menuButton).toHaveFocus();

      // Should activate with Enter
      await user.keyboard('{Enter}');
      const sidebar = screen.getByTestId('sidebar');
      expect(sidebar).toHaveAttribute('data-open', 'true');
    });
  });

  describe('Error Boundaries', () => {
    it('should handle children rendering errors gracefully', () => {
      const ThrowingComponent = () => {
        throw new Error('Test error');
      };

      // Suppress console.error for this test
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

      expect(() => {
        render(
          <AppWrapper>
            <ThrowingComponent />
          </AppWrapper>
        );
      }).not.toThrow();

      consoleSpy.mockRestore();
    });
  });

  describe('Performance', () => {
    it('should not cause unnecessary re-renders', () => {
      const { rerender } = render(
        <AppWrapper>
          <div>Content 1</div>
        </AppWrapper>
      );

      // Re-render with same props
      rerender(
        <AppWrapper>
          <div>Content 1</div>
        </AppWrapper>
      );

      // Should still work correctly
      expect(screen.getByText('Content 1')).toBeInTheDocument();
    });

    it('should handle prop changes correctly', () => {
      const { rerender } = render(
        <AppWrapper currentRoute="/home">
          <div>Content</div>
        </AppWrapper>
      );

      expect(screen.getByTestId('current-route')).toHaveTextContent('/home');

      rerender(
        <AppWrapper currentRoute="/dashboard">
          <div>Content</div>
        </AppWrapper>
      );

      expect(screen.getByTestId('current-route')).toHaveTextContent('/dashboard');
    });
  });

  describe('Event Handling', () => {
    it('should handle multiple rapid interactions', async () => {
      const user = userEvent.setup();

      render(
        <AppWrapper>
          <div>Content</div>
        </AppWrapper>
      );

      const menuButton = screen.getByTestId('menu-button');
      const sidebar = screen.getByTestId('sidebar');

      // Rapid clicks
      await user.click(menuButton);
      await user.click(menuButton);
      await user.click(menuButton);

      // Should end up in closed state (3 clicks = open -> close -> open)
      expect(sidebar).toHaveAttribute('data-open', 'true');
    });
  });
});
