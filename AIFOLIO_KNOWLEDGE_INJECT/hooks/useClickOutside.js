import { useEffect } from 'react';

/**
 * Hook to detect clicks outside of a target element
 * Useful for closing modals, dropdowns, and panels
 */
export const useClickOutside = (ref, handler, enabled = true) => {
  useEffect(() => {
    if (!enabled) return;

    const listener = (event) => {
      const element = ref?.current;

      // Do nothing if clicking ref's element or descendent elements
      if (!element || element.contains(event.target)) {
        return;
      }

      handler(event);
    };

    document.addEventListener('mousedown', listener);
    document.addEventListener('touchstart', listener);

    return () => {
      document.removeEventListener('mousedown', listener);
      document.removeEventListener('touchstart', listener);
    };
  }, [ref, handler, enabled]);
};
