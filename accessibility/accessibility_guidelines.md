# AIFOLIO Accessibility Guidelines

## WCAG 2.1 AA Compliance Standards

### 1. Perceivable
- Provide text alternatives for images
- Provide captions for videos
- Ensure sufficient color contrast (4.5:1 for normal text)
- Make content adaptable to different presentations

### 2. Operable
- Make all functionality keyboard accessible
- Give users enough time to read content
- Don't use content that causes seizures
- Help users navigate and find content

### 3. Understandable
- Make text readable and understandable
- Make content appear and operate predictably
- Help users avoid and correct mistakes

### 4. Robust
- Maximize compatibility with assistive technologies
- Use valid, semantic HTML
- Ensure content works across different browsers

## Implementation Checklist

### HTML Structure
- [ ] Use semantic HTML elements
- [ ] Provide proper heading hierarchy (h1-h6)
- [ ] Include alt attributes for images
- [ ] Use labels for form inputs
- [ ] Implement proper focus management

### CSS Design
- [ ] Ensure color contrast meets WCAG standards
- [ ] Design for 200% zoom without horizontal scrolling
- [ ] Use relative units (rem, em) for scalability
- [ ] Provide focus indicators for interactive elements

### JavaScript Interactions
- [ ] Implement keyboard navigation
- [ ] Manage focus for dynamic content
- [ ] Provide screen reader announcements
- [ ] Handle error states accessibly

### Testing Tools
- axe-core: Automated accessibility testing
- WAVE: Web accessibility evaluation
- Lighthouse: Performance and accessibility audits
- Screen readers: NVDA, JAWS, VoiceOver testing
