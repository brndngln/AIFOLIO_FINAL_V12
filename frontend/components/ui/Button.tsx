import React from 'react';
import { motion } from 'framer-motion';

interface ButtonProps {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({ 
  variant = 'primary', 
  children 
}) => {
  return (
    <motion.button
      className={`px-4 py-2 rounded-lg font-medium ${
        variant === 'primary' 
          ? 'bg-blue-600 text-white' 
          : 'bg-gray-100 text-gray-900'
      }`}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      {children}
    </motion.button>
  );
};
