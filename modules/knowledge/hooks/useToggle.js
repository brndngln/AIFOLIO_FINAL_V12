import { useState, useCallback } from 'react';

/**
 * Hook for boolean toggle logic
 * Provides toggle function and direct setters
 */
export const useToggle = (initialValue = false) => {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => {
    setValue(prev => !prev);
  }, []);

  const setToggle = useCallback((newValue) => {
    setValue(newValue);
  }, []);

  return [value, toggle, setToggle];
};
