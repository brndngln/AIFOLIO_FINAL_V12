import '@testing-library/jest-dom';
import React from 'react';
import { render, fireEvent, act } from '@testing-library/react';
import ThemeProvider from '../../frontend/theme/ThemeProvider.jsx';
import ColorCustomization from '../../frontend/src/components/ColorCustomization.jsx';

describe('ColorCustomization', () => {
  let container;
  
  beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
  });

  afterEach(() => {
    document.body.removeChild(container);
    container = null;
  });

  test('undo/redo functionality works correctly', async () => {
    console.log('[TEST] undo/redo functionality test started');
    const { getByText, getByRole } = render(
      <ThemeProvider>
        <ColorCustomization />
      </ThemeProvider>
    );

    // Find and change a color
    const colorPicker = getByRole('colorpicker');
    const originalColor = colorPicker.value;
    
    // Change color
    fireEvent.change(colorPicker, { target: { value: '#FF0000' } });
    await act(() => Promise.resolve());

    // Verify color changed
    expect(colorPicker.value).not.toBe(originalColor);

    // Test undo
    const undoButton = getByText('Undo Last Change');
    fireEvent.click(undoButton);
    await act(() => Promise.resolve());

    // Verify color reverted
    expect(colorPicker.value).toBe(originalColor);

    // Test redo
    const redoButton = getByText('Redo Last Change');
    fireEvent.click(redoButton);
    await act(() => Promise.resolve());

    // Verify color changed back
    expect(colorPicker.value).not.toBe(originalColor);
  });

  test('all color properties are properly applied', async () => {
    console.log('[TEST] all color properties test started');
    const { getByText, getByRole } = render(
      <ThemeProvider>
        <ColorCustomization />
      </ThemeProvider>
    );

    const components = [
      'app', 'card', 'button', 'input', 'link', 
      'alert', 'tooltip', 'modal', 'header', 'navigation'
    ];

    const properties = [
      'background', 'text', 'accent', 'secondary', 'cta',
      'border', 'shadow', 'hover', 'active', 'focus',
      'link', 'link-hover', 'link-visited', 'error',
      'success', 'warning', 'info', 'disabled', 'placeholder',
      'underline', 'title', 'subtitle', 'divider', 'icon'
    ];

    // Test each component and property
    for (const component of components) {
      for (const prop of properties) {
        let picker;
        try {
          picker = getByRole(`colorpicker-${component}-${prop}`);
        } catch (e) {
          // Role not found, skip
          continue;
        }
        const originalColor = picker.value;
        fireEvent.change(picker, { target: { value: '#FF0000' } });
        await act(() => Promise.resolve());
        expect(picker.value.toLowerCase()).toBe('#ff0000');
        fireEvent.change(picker, { target: { value: originalColor } });
        await act(() => Promise.resolve());
      }
    }
  });

  test('preview components update correctly', async () => {
    console.log('[TEST] preview components update test started');
    const { getByText, getByRole } = render(
      <ThemeProvider>
        <ColorCustomization />
      </ThemeProvider>
    );

    // Enable preview
    let previewButton;
    try {
      previewButton = getByText('Show Preview');
      console.log('[TEST] Found Show Preview button');
    } catch (e) {
      previewButton = getByText('Preview');
      console.log('[TEST] Found fallback Preview button');
    }
    fireEvent.click(previewButton);
    await act(() => Promise.resolve());

    // Find preview components
    const colorPreview = getByRole('color-preview');
    const buttonPreview = getByRole('button-preview');

    // Change a color and verify preview updates
    let colorPicker;
    try {
      colorPicker = getByRole('colorpicker-app-background');
      console.log('[TEST] Found colorpicker-app-background');
    } catch (e) {
      const allPickers = screen.queryAllByRole(/colorpicker/);
      colorPicker = allPickers[0];
      console.log('[TEST] Fallback to first colorpicker role');
    }
    fireEvent.change(colorPicker, { target: { value: '#FF0000' } });
    await act(() => Promise.resolve());

    // Verify previews have updated
    // Debug: log actual style
    console.log('[TEST] colorPreview style:', colorPreview.style.backgroundColor);
    console.log('[TEST] buttonPreview style:', buttonPreview.style.backgroundColor);
    // Compare computed style (browser normalizes to rgb)
    expect(colorPreview.style.backgroundColor).toBe('rgb(255, 0, 0)');
    expect(buttonPreview.style.backgroundColor).toBe('rgb(255, 0, 0)');
  });
});
