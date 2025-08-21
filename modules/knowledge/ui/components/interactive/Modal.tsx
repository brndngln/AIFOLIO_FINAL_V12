import React, { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useClickOutside } from '../../../hooks/useClickOutside';

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  closeOnOverlayClick?: boolean;
  closeOnEscape?: boolean;
  showCloseButton?: boolean;
  header?: React.ReactNode;
  footer?: React.ReactNode;
  className?: string;
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  size = 'md',
  closeOnOverlayClick = true,
  closeOnEscape = true,
  showCloseButton = true,
  header,
  footer,
  className = '',
}) => {
  const modalRef = useRef<HTMLDivElement>(null);

  // Close on click outside
  useClickOutside(
    modalRef,
    () => {
      if (closeOnOverlayClick) {
        onClose();
      }
    },
    isOpen
  );

  // Close on escape key
  useEffect(() => {
    if (!closeOnEscape || !isOpen) return;

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [closeOnEscape, isOpen, onClose]);

  // Prevent body scroll when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
    full: 'max-w-full mx-4',
  };

  const overlayVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1 },
  };

  const modalVariants = {
    hidden: {
      opacity: 0,
      scale: 0.8,
      y: 50,
    },
    visible: {
      opacity: 1,
      scale: 1,
      y: 0,
      transition: {
        type: "spring",
        stiffness: 300,
        damping: 30,
      },
    },
    exit: {
      opacity: 0,
      scale: 0.8,
      y: 50,
      transition: {
        duration: 0.2,
      },
    },
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          {/* Overlay */}
          <motion.div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm"
            variants={overlayVariants}
            initial="hidden"
            animate="visible"
            exit="hidden"
            transition={{ duration: 0.2 }}
          />

          {/* Modal Container */}
          <div className="flex min-h-full items-center justify-center p-4">
            <motion.div
              ref={modalRef}
              className={`
                relative w-full ${sizeClasses[size]}
                bg-white dark:bg-gray-800
                rounded-lg shadow-xl
                ${className}
              `}
              variants={modalVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
            >
              {/* Header */}
              {(title || header || showCloseButton) && (
                <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
                  <div className="flex-1">
                    {header || (
                      title && (
                        <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                          {title}
                        </h2>
                      )
                    )}
                  </div>
                  {showCloseButton && (
                    <motion.button
                      onClick={onClose}
                      className="ml-4 p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200"
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </motion.button>
                  )}
                </div>
              )}

              {/* Content */}
              <div className="p-6">
                {children}
              </div>

              {/* Footer */}
              {footer && (
                <div className="flex items-center justify-end space-x-3 p-6 border-t border-gray-200 dark:border-gray-700">
                  {footer}
                </div>
              )}
            </motion.div>
          </div>
        </div>
      )}
    </AnimatePresence>
  );
};

// Confirmation Modal Component
export interface ConfirmModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title?: string;
  message?: string;
  confirmText?: string;
  cancelText?: string;
  variant?: 'danger' | 'warning' | 'info';
  loading?: boolean;
}

export const ConfirmModal: React.FC<ConfirmModalProps> = ({
  isOpen,
  onClose,
  onConfirm,
  title = 'Confirm Action',
  message = 'Are you sure you want to proceed?',
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  variant = 'info',
  loading = false,
}) => {
  const variantStyles = {
    danger: 'text-red-600 dark:text-red-400',
    warning: 'text-yellow-600 dark:text-yellow-400',
    info: 'text-blue-600 dark:text-blue-400',
  };

  const buttonVariants = {
    danger: 'danger',
    warning: 'primary',
    info: 'primary',
  } as const;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      size="sm"
      header={
        <div className="flex items-center space-x-3">
          <div className={`p-2 rounded-full bg-gray-100 dark:bg-gray-700 ${variantStyles[variant]}`}>
            {variant === 'danger' && (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            )}
            {variant === 'warning' && (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            )}
            {variant === 'info' && (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            )}
          </div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
            {title}
          </h2>
        </div>
      }
      footer={
        <>
          <button
            onClick={onClose}
            disabled={loading}
            className="btn-secondary"
          >
            {cancelText}
          </button>
          <button
            onClick={onConfirm}
            disabled={loading}
            className={`btn-${buttonVariants[variant]}`}
          >
            {loading && (
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                className="w-4 h-4 border-2 border-current border-t-transparent rounded-full mr-2"
              />
            )}
            {confirmText}
          </button>
        </>
      }
    >
      <p className="text-gray-600 dark:text-gray-400">
        {message}
      </p>
    </Modal>
  );
};
