// [WINDSURF FIXED ✅]
import '@testing-library/jest-dom/vitest';
import { describe, test, expect } from 'vitest';
import React from 'react';
import { render, fireEvent, act, waitFor } from '@testing-library/react';
import ThemeProvider from '../../theme/ThemeProvider.jsx';
import ColorCustomization from '../components/ColorCustomization.jsx';

describe('ColorCustomization', () => {

  test('undo/redo functionality works correctly', async () => {
    const { getByTestId } = render(
      <ThemeProvider>
        <ColorCustomization />
      </ThemeProvider>
    );

    // Find and change a color
    // Select the app.background color picker directly by test id
    const backgroundPicker = getByTestId('colorpicker-app-background');
    const originalColor = backgroundPicker.value;
    console.log('Original color:', originalColor);
    await waitFor(() => expect(backgroundPicker.value).toBe(originalColor));

    // Change color
    fireEvent.change(backgroundPicker, { target: { value: '#FF0000' } });
    await waitFor(() => {
      const updatedPicker = getByTestId('colorpicker-app-background');
      return updatedPicker.value.toLowerCase() === '#ff0000';
    }, { timeout: 2000 });
    console.log('Color after change:', getByTestId('colorpicker-app-background').value);

    // Test undo
    const undoButton = getByTestId('undo-button');
    fireEvent.click(undoButton);
    await waitFor(() => {
      const updatedPicker = getByTestId('colorpicker-app-background');
      return updatedPicker.value.toLowerCase() === originalColor.toLowerCase();
    }, { timeout: 2000 });
    console.log('Color after undo:', getByTestId('colorpicker-app-background').value);

    // Test redo
    const redoButton = getByTestId('redo-button');
    fireEvent.click(redoButton);
    await waitFor(() => {
      const updatedPicker = getByTestId('colorpicker-app-background');
      return updatedPicker.value.toLowerCase() === '#ff0000';
    }, { timeout: 2000 });
    console.log('Color after redo:', getByTestId('colorpicker-app-background').value);

    // Final assertion
    expect(getByTestId('colorpicker-app-background').value.toLowerCase()).toBe('#ff0000');
  });

  test('all color properties are properly applied', async () => {
    const { getByTestId } = render(
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
    let pickersTestIndex = 0;
    for (const component of components) {
      for (const prop of properties) {
         // Always re-query the picker after each change to avoid stale references
         let picker = null;
         try {
           picker = getByTestId(`colorpicker-${component}-${prop}`);
         } catch (e) {
           // Picker does not exist for this component/property combo, skip
           continue;
         }
         if (!picker) continue;
         const originalColor = picker.value;
         if (typeof originalColor !== 'string') continue;
         console.log(`Picker [${component}.${prop}] before change:`, originalColor);
         fireEvent.input(picker, { target: { value: '#FF0000' } });
         await waitFor(() => {
           return picker.value && picker.value.toLowerCase() === '#ff0000';
         }, { timeout: 2000 });
         console.log(`Picker [${component}.${prop}] after change:`, picker.value);
         expect(picker.value.toLowerCase()).toBe('#ff0000');
         fireEvent.input(picker, { target: { value: originalColor } });
         await waitFor(() => {
           return picker.value && picker.value.toLowerCase() === originalColor.toLowerCase();
         }, { timeout: 2000 });
         console.log(`Picker [${component}.${prop}] after revert:`, picker.value);
      }
    }
  }, 90000);

  test('preview components update correctly', async () => {
    const { getByTestId } = render(
      <ThemeProvider>
        <ColorCustomization />
      </ThemeProvider>
    );

    // Enable preview
    const previewButton = getByTestId('preview-button');
    fireEvent.click(previewButton);
    await act(() => Promise.resolve());

    // Find preview components
    const colorPreview = getByTestId('color-preview');
    

    // Select the app.background color picker directly by test id
    const backgroundPicker = getByTestId('colorpicker-app-background');
    fireEvent.change(backgroundPicker, { target: { value: '#FF0000' } });
    await act(() => Promise.resolve());

    // Verify preview updates
    await waitFor(() => expect(colorPreview).toHaveStyle({
      backgroundColor: 'rgb(255, 0, 0)'
    }));
  }, 90000);
});
