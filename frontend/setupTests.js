// Global setup for Vitest + jsdom

// Mock window.matchMedia globally
if (typeof window !== "undefined") {
  window.matchMedia =
    window.matchMedia ||
    function () {
      return {
        matches: false,
        addEventListener: function () {},
        removeEventListener: function () {},
      };
    };
}

// Mock global fetch if not present
if (typeof global !== "undefined" && typeof global.fetch === "undefined") {
  global.fetch = () =>
    Promise.resolve({ ok: true, json: () => Promise.resolve([]) });
}

// Mock localStorage if not present
if (
  typeof window !== "undefined" &&
  typeof window.localStorage === "undefined"
) {
  let store = {};
  window.localStorage = {
    getItem: (key) => store[key] || null,
    setItem: (key, value) => {
      store[key] = value;
    },
    removeItem: (key) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
}

// Mock clipboard
if (
  typeof navigator !== "undefined" &&
  typeof navigator.clipboard === "undefined"
) {
  navigator.clipboard = { writeText: () => Promise.resolve() };
}
