import React from 'react';
import { ThemeEditorPanel } from '../ui/ThemeEditorPanel';
import { useMounted } from '../hooks/useMounted';

export const AppWrapper = ({ children }) => {
  const mounted = useMounted();

  return (
    <div className="min-h-screen transition-colors duration-300 bg-white dark:bg-gray-900">
      {/* Theme Editor Panel - Only render after mount */}
      {mounted && <ThemeEditorPanel />}

      {/* Main App Content */}
      <main className="relative">
        {children}
      </main>
    </div>
  );
};
