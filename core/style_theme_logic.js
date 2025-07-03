// Apple-tier smooth transitions, luxury design, 4K visuals, responsive typography
export const styleTheme = {
  transitions: {
    default: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
    hover: 'box-shadow 0.3s cubic-bezier(0.4,0,0.2,1)',
    vaultCard: 'transform 0.5s cubic-bezier(0.4,0,0.2,1)'
  },
  visuals: {
    resolution: '4K',
    theme: 'cinematic',
    palette: ['#181c2b', '#00fff7', '#232845', '#fff', '#b9a3e3'],
    font: 'var(--luxury-font, Inter, Helvetica, Arial, sans-serif)'
  },
  typography: {
    responsive: true,
    base: '1.15rem',
    heading: '2.25rem',
    weight: '600',
    luxury: true
  }
};
export default styleTheme;
