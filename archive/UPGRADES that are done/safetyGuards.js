// Fixed object syntax
return {
  isSuspicious:
    sentienceScore >= this.patternThreshold || suspiciousContexts.length > 0,
  matches,
  suspiciousCategories,
  suspiciousContexts,
  text,
  sentienceScore,
  totalScore,
  contextScores: Object.fromEntries(contextScores),
};

// Add rate limiting
const MAX_REQUESTS_PER_MINUTE = 100;
let requestCount = 0;
let lastResetTime = Date.now();

const checkRateLimit = () => {
  const currentTime = Date.now();
  if (currentTime - lastResetTime > 60000) {
    requestCount = 0;
    lastResetTime = currentTime;
  }
  if (requestCount >= MAX_REQUESTS_PER_MINUTE) {
    throw new Error("Rate limit exceeded");
  }
  requestCount++;
};

// Add memory monitoring
const checkMemoryUsage = () => {
  const memoryUsage = process.memoryUsage();
  if (memoryUsage.heapUsed > 100 * 1024 * 1024) {
    // 100MB
    console.warn("High memory usage detected");
  }
};
