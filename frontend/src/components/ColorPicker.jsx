import React, { useState } from 'react';
import { useTheme } from '../theme/ThemeProvider';

function ColorPicker({ component, property, defaultValue }) {
  const { setTheme } = useTheme();
  const [color, setColor] = useState(localStorage.getItem(`color-${component}-${property}`) || defaultValue);

  const handleChange = (e) => {
    const newColor = e.target.value;
    setColor(newColor);
    localStorage.setItem(`color-${component}-${property}`, newColor);
    
    // Update theme object with new color
    setTheme(prev => ({
      ...prev,
      customColors: {
        ...prev.customColors,
        [component]: {
          ...(prev.customColors?.[component] || {}),
          [property]: newColor
        }
      }
    }));
  };

  return (
    <div className="flex items-center space-x-2">
      <label className="text-sm">{property.replace(/([A-Z])/g, ' $1').trim()}:</label>
      <input
        type="color"
        value={color}
        onChange={handleChange}
        className="w-10 h-10 rounded cursor-pointer"
      />
      <input
        type="text"
        value={color}
        onChange={handleChange}
        className="w-24 border rounded px-2"
      />
    </div>
  );
}

export default ColorPicker;
