import { useState, useEffect } from 'react';

/**
 * Hook to check if component is mounted
 * Prevents hydration mismatches in SSR environments
 * Returns true only after component has mounted on client
 */
export const useMounted = () => {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return mounted;
};
