// AIFOLIO Elite System - useToggle Hook Tests
// Validates toggle state logic with comprehensive scenarios

import { renderHook, act } from '@testing-library/react';
import { useToggle } from '../../hooks/useToggle';

describe('useToggle Hook', () => {
  describe('Default Behavior', () => {
    it('should initialize with false by default', () => {
      const { result } = renderHook(() => useToggle());
      const [value] = result.current;

      expect(value).toBe(false);
    });

    it('should initialize with provided initial value', () => {
      const { result } = renderHook(() => useToggle(true));
      const [value] = result.current;

      expect(value).toBe(true);
    });
  });

  describe('Toggle Functionality', () => {
    it('should toggle from false to true', () => {
      const { result } = renderHook(() => useToggle(false));

      act(() => {
        const [, toggle] = result.current;
        toggle();
      });

      const [value] = result.current;
      expect(value).toBe(true);
    });

    it('should toggle from true to false', () => {
      const { result } = renderHook(() => useToggle(true));

      act(() => {
        const [, toggle] = result.current;
        toggle();
      });

      const [value] = result.current;
      expect(value).toBe(false);
    });

    it('should toggle multiple times correctly', () => {
      const { result } = renderHook(() => useToggle(false));

      // Initial state
      expect(result.current[0]).toBe(false);

      // First toggle
      act(() => {
        result.current[1]();
      });
      expect(result.current[0]).toBe(true);

      // Second toggle
      act(() => {
        result.current[1]();
      });
      expect(result.current[0]).toBe(false);

      // Third toggle
      act(() => {
        result.current[1]();
      });
      expect(result.current[0]).toBe(true);
    });
  });

  describe('Direct Setter Functionality', () => {
    it('should set value to true using setter', () => {
      const { result } = renderHook(() => useToggle(false));

      act(() => {
        const [, , setToggle] = result.current;
        setToggle(true);
      });

      const [value] = result.current;
      expect(value).toBe(true);
    });

    it('should set value to false using setter', () => {
      const { result } = renderHook(() => useToggle(true));

      act(() => {
        const [, , setToggle] = result.current;
        setToggle(false);
      });

      const [value] = result.current;
      expect(value).toBe(false);
    });

    it('should override current state with setter', () => {
      const { result } = renderHook(() => useToggle(true));

      // Set to false
      act(() => {
        const [, , setToggle] = result.current;
        setToggle(false);
      });
      expect(result.current[0]).toBe(false);

      // Set to true
      act(() => {
        const [, , setToggle] = result.current;
        setToggle(true);
      });
      expect(result.current[0]).toBe(true);
    });
  });

  describe('Return Value Structure', () => {
    it('should return array with correct structure', () => {
      const { result } = renderHook(() => useToggle());
      const [value, toggle, setToggle] = result.current;

      expect(typeof value).toBe('boolean');
      expect(typeof toggle).toBe('function');
      expect(typeof setToggle).toBe('function');
      expect(result.current).toHaveLength(3);
    });

    it('should maintain function references across renders', () => {
      const { result, rerender } = renderHook(() => useToggle());

      const [, initialToggle, initialSetToggle] = result.current;

      rerender();

      const [, rerenderToggle, rerenderSetToggle] = result.current;

      expect(initialToggle).toBe(rerenderToggle);
      expect(initialSetToggle).toBe(rerenderSetToggle);
    });
  });

  describe('Edge Cases', () => {
    it('should handle rapid successive toggles', () => {
      const { result } = renderHook(() => useToggle(false));

      act(() => {
        // Rapid toggles
        result.current[1](); // true
        result.current[1](); // false
        result.current[1](); // true
        result.current[1](); // false
      });

      expect(result.current[0]).toBe(false);
    });

    it('should handle mixed toggle and setter operations', () => {
      const { result } = renderHook(() => useToggle(false));

      act(() => {
        result.current[1](); // toggle to true
        result.current[2](false); // set to false
        result.current[1](); // toggle to true
      });

      expect(result.current[0]).toBe(true);
    });
  });
});
