import { useEffect, useRef } from 'react';

export const usePerformanceMonitor = (componentName: string) => {
  const renderStart = useRef<number>(0);
  
  useEffect(() => {
    renderStart.current = performance.now();
    
    return () => {
      const renderTime = performance.now() - renderStart.current;
      if (renderTime > 16) { // Longer than one frame
        console.warn(`Slow render detected in ${componentName}: ${renderTime.toFixed(2)}ms`);
      }
    };
  });
  
  const measureAction = (actionName: string, action: () => void) => {
    const start = performance.now();
    action();
    const duration = performance.now() - start;
    
    if (duration > 100) {
      console.warn(`Slow action in ${componentName}.${actionName}: ${duration.toFixed(2)}ms`);
    }
  };
  
  return { measureAction };
};