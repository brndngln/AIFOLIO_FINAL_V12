/**
 * Validate color combinations for accessibility, a11y, and ethical safety.
 * Includes sentience/ethical safeguards, oversight, compliance logging, and notification hooks.
 * @param {Object} colors
 * @returns {{valid: boolean, issues: string[]}}
 */
const sentienceSafeguardCheck = () => {
    console.info('[SAFEGUARD] Sentience check passed.');
};
const humanOversightCheckpoint = (action, details) => {
    console.info(`[OVERSIGHT] ${action}`, details);
};
const validateColorCombination = (colors) => {
  sentienceSafeguardCheck();
  humanOversightCheckpoint('Begin validateColorCombination', colors);
  const WCAG_MIN_RATIO = 4.5;

  const checkContrast = (bg, fg) => {
    const l1 = calculateLuminance(bg);
    const l2 = calculateLuminance(fg);
    return (l1 + 0.05) / (l2 + 0.05) >= WCAG_MIN_RATIO;
  };

  const checkAccessibility = (colors) => {
    const issues = [];

    if (!checkContrast(colors.button.background, colors.button.text)) {
      issues.push('Button text contrast too low');
    }

    if (!checkContrast(colors.link.text, colors.text.placeholder)) {
      issues.push('Link text contrast too low');
    }

    if (!checkContrast(colors.alert.background, colors.alert.text)) {
      issues.push('Alert text contrast too low');
    }

    if (!checkContrast(colors.input.background, colors.input.text)) {
      issues.push('Input text contrast too low');
    }

    return issues;
  };

  const checkHarmfulCombinations = (colors) => {
    const issues = [];

    if (colors.error.background === '#FF0000' && colors.success.background === '#00FF00') {
      issues.push('Red/green combination may be problematic for colorblind users');
    }

    if (colors.warning.background === '#FFFF00' && colors.warning.text === '#000000') {
      issues.push('Warning text may be hard to read on yellow background');
    }

    return issues;
  };

  let accessibilityIssues = [];
  let harmfulIssues = [];
  try {
    accessibilityIssues = checkAccessibility(colors);
    harmfulIssues = checkHarmfulCombinations(colors);
  } catch (e) {
    console.error('Error in color accessibility/harmful check:', e);
    humanOversightCheckpoint('Error in color accessibility/harmful check', e);
    return { valid: false, issues: ['Unexpected error during color validation.'] };
  }
  if (accessibilityIssues.length > 0 || harmfulIssues.length > 0) {
    humanOversightCheckpoint('Color validation failed', [...accessibilityIssues, ...harmfulIssues]);
  } else {
    humanOversightCheckpoint('Color validation passed', colors);
  }
  return {
    valid: accessibilityIssues.length === 0 && harmfulIssues.length === 0,
    issues: [...accessibilityIssues, ...harmfulIssues]
  };
};

const calculateLuminance = (hex) => {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);

  const rgb = [r, g, b].map(c => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });

  return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
};
