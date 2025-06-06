// Theme configuration file
export const theme = {
  // Color palette
  colors: {
    // Primary Colors
    primary: {
      main: '#2563eb',
      light: '#3b82f6',
      dark: '#1d4ed8',
      contrastText: '#ffffff'
    },
    secondary: {
      main: '#10b981',
      light: '#2dd4bf',
      dark: '#059669',
      contrastText: '#ffffff'
    },
    
    // Background Colors
    background: {
      main: '#0f172a',
      light: '#1e293b',
      dark: '#0c1420',
      surface: '#1e293b',
      surfaceVariant: '#334155'
    },
    
    // Text Colors
    text: {
      primary: '#f8fafc',
      secondary: '#94a3b8',
      disabled: '#64748b',
      hint: '#64748b',
      link: '#3b82f6'
    },
    
    // Status Colors
    success: {
      main: '#10b981',
      light: '#2dd4bf',
      dark: '#059669',
      contrastText: '#ffffff'
    },
    error: {
      main: '#ef4444',
      light: '#f87171',
      dark: '#dc2626',
      contrastText: '#ffffff'
    },
    warning: {
      main: '#f59e0b',
      light: '#fbbf24',
      dark: '#d97706',
      contrastText: '#ffffff'
    },
    info: {
      main: '#3b82f6',
      light: '#60a5fa',
      dark: '#1d4ed8',
      contrastText: '#ffffff'
    },
    
    // Additional Status Colors
    neutral: {
      main: '#64748b',
      light: '#94a3b8',
      dark: '#475569',
      contrastText: '#ffffff'
    },
    danger: {
      main: '#dc2626',
      light: '#f87171',
      dark: '#b91c1c',
      contrastText: '#ffffff'
    },
    caution: {
      main: '#fbbf24',
      light: '#fcd34d',
      dark: '#d97706',
      contrastText: '#000000'
    },
    positive: {
      main: '#10b981',
      light: '#2dd4bf',
      dark: '#059669',
      contrastText: '#ffffff'
    },
    negative: {
      main: '#ef4444',
      light: '#f87171',
      dark: '#dc2626',
      contrastText: '#ffffff'
    },
    
    // Metric Colors
    metrics: {
      up: '#10b981',
      down: '#ef4444',
      stable: '#64748b',
      critical: '#dc2626',
      good: '#10b981',
      warning: '#fbbf24',
      excellent: '#10b981',
      poor: '#ef4444'
    }
  },
  
  // Typography
  typography: {
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      lineHeight: 1.2,
      letterSpacing: '-0.025em'
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      lineHeight: 1.3,
      letterSpacing: '-0.015em'
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
      lineHeight: 1.4,
      letterSpacing: '-0.01em'
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 600,
      lineHeight: 1.5,
      letterSpacing: '-0.01em'
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 600,
      lineHeight: 1.5,
      letterSpacing: '-0.01em'
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 600,
      lineHeight: 1.5,
      letterSpacing: '-0.01em'
    },
    body: {
      fontSize: '1rem',
      fontWeight: 400,
      lineHeight: 1.5,
      letterSpacing: '0.01em'
    },
    bodySmall: {
      fontSize: '0.875rem',
      fontWeight: 400,
      lineHeight: 1.5,
      letterSpacing: '0.01em'
    },
    caption: {
      fontSize: '0.75rem',
      fontWeight: 400,
      lineHeight: 1.5,
      letterSpacing: '0.02em'
    }
  },
  
  // Spacing
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    xxl: '3rem',
    xxxl: '4rem'
  },
  
  // Border Radius
  borderRadius: {
    xs: '0.125rem',
    sm: '0.25rem',
    md: '0.5rem',
    lg: '0.75rem',
    xl: '1rem',
    full: '9999px'
  },
  
  // Shadows
  shadows: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 25px rgba(0, 0, 0, 0.1)',
    xxl: '0 25px 50px rgba(0, 0, 0, 0.1)',
    inner: 'inset 0 2px 4px rgba(0, 0, 0, 0.05)',
    none: 'none'
  },
  
  // Components
  components: {
    button: {
      primary: {
        backgroundColor: '#2563eb',
        color: '#ffffff',
        hover: {
          backgroundColor: '#1d4ed8'
        },
        active: {
          backgroundColor: '#1e40af'
        }
      },
      secondary: {
        backgroundColor: '#10b981',
        color: '#ffffff',
        hover: {
          backgroundColor: '#059669'
        },
        active: {
          backgroundColor: '#06835f'
        }
      },
      text: {
        color: '#1e293b',
        backgroundColor: 'transparent',
        hover: {
          color: '#2563eb'
        }
      },
      outlined: {
        borderColor: '#64748b',
        color: '#f8fafc',
        backgroundColor: 'transparent',
        hover: {
          borderColor: '#94a3b8'
        }
      }
    },
    card: {
      backgroundColor: '#1e293b',
      shadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      borderRadius: '0.5rem',
      variants: {
        outlined: {
          borderColor: '#64748b',
          borderWidth: '1px'
        },
        elevated: {
          shadow: '0 10px 15px rgba(0, 0, 0, 0.1)'
        }
      }
    },
    input: {
      backgroundColor: '#334155',
      color: '#f8fafc',
      borderColor: '#64748b',
      focus: {
        borderColor: '#2563eb',
        shadow: '0 0 0 3px rgba(37, 99, 235, 0.1)'
      }
    },
    icon: {
      size: {
        xs: '0.75rem',
        sm: '1rem',
        md: '1.25rem',
        lg: '1.5rem',
        xl: '2rem'
      },
      colors: {
        primary: '#2563eb',
        secondary: '#10b981',
        disabled: '#64748b'
      }
    }
  },
  
  // Layout
  layout: {
    container: {
      maxWidth: '1200px',
      padding: '1rem'
    },
    grid: {
      gap: '1rem',
      columns: '1fr',
      variants: {
        two: 'repeat(2, 1fr)',
        three: 'repeat(3, 1fr)',
        four: 'repeat(4, 1fr)'
      }
    }
  },
  
  // Transitions
  transitions: {
    default: 'all 0.2s ease-in-out',
    fast: 'all 0.1s ease-in-out',
    slow: 'all 0.3s ease-in-out'
  },
  
  // Z-index
  zIndex: {
    hide: -1,
    auto: 'auto',
    base: 0,
    dropdown: 1000,
    sticky: 1100,
    fixed: 1200,
    modal: 1300,
    popover: 1400,
    skipLink: 1500
  }
};

// Dark/Light theme variants
export const themes = {
  colors: {
    // Primary Colors
    primary: {
      main: '#2563eb',
      light: '#3b82f6',
      dark: '#1d4ed8'
    },
    secondary: {
      main: '#10b981',
      light: '#2dd4bf',
      dark: '#059669'
    },
    
    // Background Colors
    background: {
      main: '#0f172a',
      light: '#1e293b',
      dark: '#0c1420'
    },
    
    // Text Colors
    text: {
      primary: '#f8fafc',
      secondary: '#94a3b8',
      disabled: '#64748b'
    },
    
    // Status Colors
    success: {
      main: '#10b981',
      light: '#2dd4bf',
      dark: '#059669'
    },
    error: {
      main: '#ef4444',
      light: '#f87171',
      dark: '#dc2626'
    },
    warning: {
      main: '#f59e0b',
      light: '#fbbf24',
      dark: '#d97706'
    },
    info: {
      main: '#3b82f6',
      light: '#60a5fa',
      dark: '#1d4ed8'
    }
  },
  
  // Typography
  typography: {
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      lineHeight: 1.2
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      lineHeight: 1.3
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
      lineHeight: 1.4
    },
    body: {
      fontSize: '1rem',
      fontWeight: 400,
      lineHeight: 1.5
    }
  },
  
  // Spacing
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    xxl: '3rem'
  },
  
  // Border Radius
  borderRadius: {
    sm: '0.25rem',
    md: '0.5rem',
    lg: '0.75rem',
    xl: '1rem'
  },
  
  // Shadows
  shadows: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 25px rgba(0, 0, 0, 0.1)'
  },
  
  // Components
  components: {
    button: {
      primary: {
        backgroundColor: '#2563eb',
        color: '#ffffff',
        hover: {
          backgroundColor: '#1d4ed8'
        }
      },
      secondary: {
        backgroundColor: '#10b981',
        color: '#ffffff',
        hover: {
          backgroundColor: '#059669'
        }
      }
    },
    card: {
      backgroundColor: '#1e293b',
  dark: {
    ...baseTheme,
    colors: {
      ...baseTheme.colors,
      background: {
        main: '#0f172a',
        light: '#1e293b',
        dark: '#0c1420',
        surface: '#1e293b',
        surfaceVariant: '#334155'
      },
      text: {
        primary: '#f8fafc',
        secondary: '#94a3b8',
        disabled: '#64748b',
        hint: '#64748b',
        link: '#3b82f6'
      },
      primary: {
        main: '#3b82f6',
        light: '#60a5fa',
        dark: '#1d4ed8',
        contrastText: '#ffffff'
      },
      secondary: {
        main: '#2dd4bf',
        light: '#3dd3c8',
        dark: '#059669',
        contrastText: '#ffffff'
      }
    },
    components: {
      ...baseTheme.components,
      input: {
        backgroundColor: '#334155',
        color: '#f8fafc',
        borderColor: '#64748b',
        focus: {
          borderColor: '#3b82f6',
          shadow: '0 0 0 3px rgba(59, 130, 246, 0.1)'
        }
      }
    }
  },
  
  // Light theme
  light: {
    ...baseTheme,
    colors: {
      ...baseTheme.colors,
      background: {
        main: '#ffffff',
        light: '#f3f4f6',
        dark: '#f8fafc',
        surface: '#ffffff',
        surfaceVariant: '#f3f4f6'
      },
      text: {
        primary: '#1e293b',
        secondary: '#475569',
        disabled: '#94a3b8',
        hint: '#94a3b8',
        link: '#3b82f6'
      },
      primary: {
        main: '#3b82f6',
        light: '#60a5fa',
        dark: '#1d4ed8',
        contrastText: '#ffffff'
      },
      secondary: {
        main: '#2dd4bf',
        light: '#3dd3c8',
        dark: '#059669',
        contrastText: '#ffffff'
      }
    },
    components: {
      ...baseTheme.components,
      input: {
        backgroundColor: '#ffffff',
        color: '#1e293b',
        borderColor: '#e2e8f0',
        focus: {
          borderColor: '#3b82f6',
          shadow: '0 0 0 3px rgba(59, 130, 246, 0.1)'
        }
      }
    }
  },
  
  // Custom themes
  'dark-blue': {
    ...baseTheme,
    colors: {
      ...baseTheme.colors,
      background: {
        main: '#0f172a',
        light: '#1e293b',
        dark: '#0c1420',
        surface: '#1e293b',
        surfaceVariant: '#2563eb'
      },
      text: {
        primary: '#f8fafc',
        secondary: '#94a3b8',
        disabled: '#64748b',
        hint: '#64748b',
        link: '#2563eb'
      },
      primary: {
        main: '#2563eb',
        light: '#3b82f6',
        dark: '#1d4ed8',
        contrastText: '#ffffff'
      },
      secondary: {
        main: '#10b981',
        light: '#2dd4bf',
        dark: '#059669',
        contrastText: '#ffffff'
      }
    },
    components: {
      ...baseTheme.components,
      input: {
        backgroundColor: '#1e293b',
        color: '#f8fafc',
        borderColor: '#2563eb',
        focus: {
          borderColor: '#1d4ed8',
          shadow: '0 0 0 3px rgba(37, 99, 235, 0.1)'
        }
      }
    }
  },
  
  'light-blue': {
    ...baseTheme,
    colors: {
      ...baseTheme.colors,
      background: {
        main: '#f0f9ff',
        light: '#e0f2fe',
        dark: '#cffafe',
        surface: '#f0f9ff',
        surfaceVariant: '#e0f2fe'
      },
      text: {
        primary: '#0891b2',
        secondary: '#38bdf8',
        disabled: '#60a5fa',
        hint: '#60a5fa',
        link: '#0ea5e9'
      },
      primary: {
        main: '#0ea5e9',
        light: '#38bdf8',
        dark: '#0891b2',
        contrastText: '#ffffff'
      },
      secondary: {
        main: '#2dd4bf',
        light: '#3dd3c8',
        dark: '#059669',
        contrastText: '#ffffff'
      }
    },
    components: {
      ...baseTheme.components,
      input: {
        backgroundColor: '#f0f9ff',
        color: '#0891b2',
        borderColor: '#38bdf8',
        focus: {
          borderColor: '#0ea5e9',
          shadow: '0 0 0 3px rgba(14, 165, 233, 0.1)'
        }
      }
    }
  }
};

// Default theme
export default themes.dark;
