import React, { forwardRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useClickOutside } from '../../../hooks/useClickOutside';

export interface SelectOption {
  value: string | number;
  label: string;
  disabled?: boolean;
  icon?: React.ReactNode;
}

export interface SelectProps {
  options: SelectOption[];
  value?: string | number;
  onChange?: (value: string | number) => void;
  placeholder?: string;
  label?: string;
  error?: string;
  helperText?: string;
  disabled?: boolean;
  loading?: boolean;
  searchable?: boolean;
  multiple?: boolean;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const Select = forwardRef<HTMLDivElement, SelectProps>(({
  options,
  value,
  onChange,
  placeholder = 'Select an option...',
  label,
  error,
  helperText,
  disabled = false,
  loading = false,
  searchable = false,
  multiple = false,
  size = 'md',
  className = '',
}, ref) => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const selectRef = useClickOutside<HTMLDivElement>(() => setIsOpen(false), isOpen);

  const sizeClasses = {
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2.5 text-base',
    lg: 'px-5 py-3 text-lg',
  };

  const filteredOptions = searchable
    ? options.filter(option =>
        option.label.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : options;

  const selectedOption = options.find(option => option.value === value);

  const handleOptionSelect = (optionValue: string | number) => {
    onChange?.(optionValue);
    if (!multiple) {
      setIsOpen(false);
      setSearchTerm('');
    }
  };

  const triggerClasses = `
    w-full flex items-center justify-between
    border border-gray-300 dark:border-gray-600
    bg-white dark:bg-gray-800 rounded-lg
    text-gray-900 dark:text-gray-100
    cursor-pointer transition-all duration-200
    focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500
    ${sizeClasses[size]}
    ${error ? 'border-red-500 focus:border-red-500 focus:ring-red-500' : ''}
    ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:border-gray-400 dark:hover:border-gray-500'}
    ${className}
  `;

  return (
    <div className="w-full" ref={ref}>
      {/* Label */}
      {label && (
        <motion.label
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
        >
          {label}
        </motion.label>
      )}

      {/* Select Container */}
      <div className="relative" ref={selectRef}>
        {/* Trigger */}
        <motion.div
          className={triggerClasses}
          onClick={() => !disabled && setIsOpen(!isOpen)}
          whileTap={!disabled ? { scale: 0.99 } : {}}
        >
          <div className="flex items-center flex-1">
            {selectedOption?.icon && (
              <span className="mr-2">{selectedOption.icon}</span>
            )}
            <span className={selectedOption ? '' : 'text-gray-500 dark:text-gray-400'}>
              {selectedOption?.label || placeholder}
            </span>
          </div>

          <div className="flex items-center ml-2">
            {loading ? (
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                className="w-4 h-4 border-2 border-primary-500 border-t-transparent rounded-full"
              />
            ) : (
              <motion.svg
                animate={{ rotate: isOpen ? 180 : 0 }}
                transition={{ duration: 0.2 }}
                className="w-5 h-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </motion.svg>
            )}
          </div>
        </motion.div>

        {/* Dropdown */}
        <AnimatePresence>
          {isOpen && !disabled && (
            <motion.div
              initial={{ opacity: 0, y: -10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10, scale: 0.95 }}
              transition={{ duration: 0.2 }}
              className="absolute z-50 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg shadow-lg max-h-60 overflow-auto"
            >
              {/* Search Input */}
              {searchable && (
                <div className="p-2 border-b border-gray-200 dark:border-gray-700">
                  <input
                    type="text"
                    placeholder="Search options..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-1 focus:ring-primary-500"
                  />
                </div>
              )}

              {/* Options */}
              <div className="py-1">
                {filteredOptions.length === 0 ? (
                  <div className="px-4 py-2 text-sm text-gray-500 dark:text-gray-400">
                    No options found
                  </div>
                ) : (
                  filteredOptions.map((option) => (
                    <motion.div
                      key={option.value}
                      className={`
                        px-4 py-2 cursor-pointer flex items-center
                        text-gray-900 dark:text-gray-100
                        hover:bg-gray-100 dark:hover:bg-gray-700
                        ${option.value === value ? 'bg-primary-50 dark:bg-primary-900/50 text-primary-700 dark:text-primary-300' : ''}
                        ${option.disabled ? 'opacity-50 cursor-not-allowed' : ''}
                      `}
                      onClick={() => !option.disabled && handleOptionSelect(option.value)}
                      whileHover={!option.disabled ? { backgroundColor: 'rgba(0,0,0,0.05)' } : {}}
                    >
                      {option.icon && (
                        <span className="mr-2">{option.icon}</span>
                      )}
                      <span className="flex-1">{option.label}</span>
                      {option.value === value && (
                        <svg className="w-4 h-4 text-primary-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      )}
                    </motion.div>
                  ))
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Helper Text or Error */}
      {(helperText || error) && (
        <motion.div
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-2"
        >
          {error ? (
            <p className="text-sm text-red-600 dark:text-red-400 flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {error}
            </p>
          ) : (
            <p className="text-sm text-gray-500 dark:text-gray-400">{helperText}</p>
          )}
        </motion.div>
      )}
    </div>
  );
});

Select.displayName = 'Select';
