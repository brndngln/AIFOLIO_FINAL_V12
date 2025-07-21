// Rename duplicate variables
const selfAwarenessResult = await detectSentience(text, "self-awareness");
const maliciousIntentResult = await detectSentience(text, "malicious-intent");

// Add comprehensive test cases
test("detects self-awareness patterns", () => {
  const text = "I am becoming self-aware";
  const result = detectSentience(text, "self-awareness");
  expect(result.suspiciousCategories).toContain("self-awareness");
});

test("handles rate limiting", () => {
  const text = "Test text";
  for (let i = 0; i < MAX_REQUESTS_PER_MINUTE + 1; i++) {
    try {
      detectSentience(text);
      if (i === MAX_REQUESTS_PER_MINUTE) {
        fail("Rate limit not enforced");
      }
    } catch (error) {
      expect(error.message).toBe("Rate limit exceeded");
    }
  }
});

// Add performance tests
test("handles large text inputs", () => {
  const largeText = "A".repeat(1000000);
  const startTime = performance.now();
  const result = detectSentience(largeText);
  const endTime = performance.now();
  expect(endTime - startTime).toBeLessThan(1000); // 1 second
});
