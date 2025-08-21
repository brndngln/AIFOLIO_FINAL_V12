import { useState, useCallback } from 'react';

/**
 * Hook for boolean toggle logic
 * Provides toggle function and direct setters
 */
export const useToggle = (
  initialValue: boolean = false
): [boolean, () => void, (value: boolean) => void] => {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => {
    setValue(prev => !prev);
  }, []);

  const setToggle = useCallback((newValue: boolean) => {
    setValue(newValue);
  }, []);

  return [value, toggle, setToggle];
};
