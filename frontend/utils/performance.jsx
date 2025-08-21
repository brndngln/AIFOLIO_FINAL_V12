"""Performance monitoring utilities for AIFOLIO UI."""

import { useEffect, useRef, useState } from 'react';

// Performance metrics hook
export const usePerformanceMetrics = () => {
  const [metrics, setMetrics] = useState({
    renderTime: 0,
    memoryUsage: 0,
    fps: 0
  });
  
  useEffect(() => {
    const observer = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      entries.forEach((entry) => {
        if (entry.entryType === 'measure') {
          setMetrics(prev => ({
            ...prev,
            renderTime: entry.duration
          }));
        }
      });
    });
    
    observer.observe({ entryTypes: ['measure'] });
    
    return () => observer.disconnect();
  }, []);
  
  return metrics;
};

// Lazy loading hook
export const useLazyLoading = (threshold = 0.1) => {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { threshold }
    );
    
    if (ref.current) {
      observer.observe(ref.current);
    }
    
    return () => observer.disconnect();
  }, [threshold]);
  
  return [ref, isVisible];
};

// Virtual scrolling hook
export const useVirtualScrolling = (items, itemHeight, containerHeight) => {
  const [scrollTop, setScrollTop] = useState(0);
  
  const startIndex = Math.floor(scrollTop / itemHeight);
  const endIndex = Math.min(
    startIndex + Math.ceil(containerHeight / itemHeight) + 1,
    items.length
  );
  
  const visibleItems = items.slice(startIndex, endIndex);
  
  return {
    visibleItems,
    startIndex,
    totalHeight: items.length * itemHeight,
    offsetY: startIndex * itemHeight,
    onScroll: (e) => setScrollTop(e.target.scrollTop)
  };
};

// Image optimization component
export const OptimizedImage = ({ 
  src, 
  alt, 
  width, 
  height, 
  loading = 'lazy',
  ...props 
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [error, setError] = useState(false);
  
  return (
    <div className="relative overflow-hidden">
      {!isLoaded && !error && (
        <div className="absolute inset-0 bg-gray-200 animate-pulse" />
      )}
      <img
        src={src}
        alt={alt}
        width={width}
        height={height}
        loading={loading}
        onLoad={() => setIsLoaded(true)}
        onError={() => setError(true)}
        className={`transition-opacity duration-300 ${
          isLoaded ? 'opacity-100' : 'opacity-0'
        }`}
        {...props}
      />
      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-100 text-gray-500">
          Failed to load image
        </div>
      )}
    </div>
  );
};
