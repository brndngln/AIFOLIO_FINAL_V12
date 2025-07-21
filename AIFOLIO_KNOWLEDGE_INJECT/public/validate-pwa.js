// AIFOLIO PWA Validation Script
// Comprehensive PWA setup validation and testing

class PWAValidator {
    constructor() {
        this.results = {
            manifest: {},
            serviceWorker: {},
            icons: {},
            meta: {},
            installability: {},
            overall: { score: 0, status: 'unknown' }
        };

        this.requiredIcons = [
            'icon-192x192.png',
            'icon-512x512.png'
        ];

        this.optionalIcons = [
            'icon-72x72.png',
            'icon-96x96.png',
            'icon-128x128.png',
            'icon-144x144.png',
            'icon-152x152.png',
            'icon-384x384.png',
            'favicon-32x32.png',
            'apple-touch-icon.png'
        ];
    }

    async validateAll() {
        console.log('🔍 AIFOLIO PWA: Starting comprehensive validation...');

        await this.validateManifest();
        await this.validateServiceWorker();
        await this.validateIcons();
        await this.validateMetaTags();
        await this.validateInstallability();

        this.calculateOverallScore();
        this.displayResults();

        return this.results;
    }

    async validateManifest() {
        console.log('📄 Validating manifest.json...');

        try {
            const response = await fetch('/manifest.json');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const manifest = await response.json();

            // Required fields
            const required = ['name', 'short_name', 'start_url', 'display', 'icons'];
            const missing = required.filter(field => !manifest[field]);

            this.results.manifest = {
                exists: true,
                valid: missing.length === 0,
                missing: missing,
                data: manifest,
                score: missing.length === 0 ? 100 : Math.max(0, 100 - (missing.length * 20))
            };

            // Validate icons in manifest
            if (manifest.icons && Array.isArray(manifest.icons)) {
                const hasRequired = this.requiredIcons.every(size =>
                    manifest.icons.some(icon => icon.src.includes(size))
                );
                this.results.manifest.hasRequiredIcons = hasRequired;
            }

        } catch (error) {
            console.error('❌ Manifest validation failed:', error);
            this.results.manifest = {
                exists: false,
                valid: false,
                error: error.message,
                score: 0
            };
        }
    }

    async validateServiceWorker() {
        console.log('⚙️ Validating service worker...');

        if ('serviceWorker' in navigator) {
            try {
                const registration = await navigator.serviceWorker.getRegistration();

                this.results.serviceWorker = {
                    supported: true,
                    registered: !!registration,
                    active: registration ? !!registration.active : false,
                    scope: registration ? registration.scope : null,
                    score: registration && registration.active ? 100 : 50
                };

                if (registration && registration.active) {
                    console.log('✅ Service Worker active:', registration.scope);
                } else {
                    console.warn('⚠️ Service Worker not active');
                }

            } catch (error) {
                console.error('❌ Service Worker validation failed:', error);
                this.results.serviceWorker = {
                    supported: true,
                    registered: false,
                    error: error.message,
                    score: 0
                };
            }
        } else {
            this.results.serviceWorker = {
                supported: false,
                score: 0
            };
        }
    }

    async validateIcons() {
        console.log('🎨 Validating PWA icons...');

        const iconResults = {
            required: {},
            optional: {},
            score: 0
        };

        // Check required icons
        for (const icon of this.requiredIcons) {
            try {
                const response = await fetch(`/icons/${icon}`, { method: 'HEAD' });
                iconResults.required[icon] = {
                    exists: response.ok,
                    status: response.status
                };
            } catch (error) {
                iconResults.required[icon] = {
                    exists: false,
                    error: error.message
                };
            }
        }

        // Check optional icons
        for (const icon of this.optionalIcons) {
            try {
                const response = await fetch(`/icons/${icon}`, { method: 'HEAD' });
                iconResults.optional[icon] = {
                    exists: response.ok,
                    status: response.status
                };
            } catch (error) {
                iconResults.optional[icon] = {
                    exists: false,
                    error: error.message
                };
            }
        }

        // Calculate score
        const requiredCount = Object.values(iconResults.required).filter(r => r.exists).length;
        const optionalCount = Object.values(iconResults.optional).filter(r => r.exists).length;

        iconResults.score = (requiredCount / this.requiredIcons.length) * 60 +
                           (optionalCount / this.optionalIcons.length) * 40;

        this.results.icons = iconResults;
    }

    validateMetaTags() {
        console.log('🏷️ Validating PWA meta tags...');

        const requiredMeta = [
            'theme-color',
            'apple-mobile-web-app-capable',
            'apple-mobile-web-app-status-bar-style'
        ];

        const metaResults = {
            viewport: !!document.querySelector('meta[name="viewport"]'),
            themeColor: !!document.querySelector('meta[name="theme-color"]'),
            appleMeta: {},
            manifestLink: !!document.querySelector('link[rel="manifest"]'),
            score: 0
        };

        // Check Apple-specific meta tags
        requiredMeta.forEach(name => {
            metaResults.appleMeta[name] = !!document.querySelector(`meta[name="${name}"]`);
        });

        // Calculate score
        const metaCount = Object.values(metaResults.appleMeta).filter(Boolean).length;
        metaResults.score = (metaResults.viewport ? 25 : 0) +
                           (metaResults.themeColor ? 25 : 0) +
                           (metaResults.manifestLink ? 25 : 0) +
                           (metaCount / requiredMeta.length) * 25;

        this.results.meta = metaResults;
    }

    async validateInstallability() {
        console.log('📱 Validating PWA installability...');

        const installResults = {
            beforeInstallPrompt: false,
            standalone: false,
            httpsOrLocalhost: false,
            score: 0
        };

        // Check if running in standalone mode
        installResults.standalone = window.matchMedia('(display-mode: standalone)').matches ||
                                   window.navigator.standalone === true;

        // Check HTTPS or localhost
        installResults.httpsOrLocalhost = location.protocol === 'https:' ||
                                         location.hostname === 'localhost' ||
                                         location.hostname === '127.0.0.1';

        // Check for beforeinstallprompt support
        installResults.beforeInstallPrompt = 'onbeforeinstallprompt' in window;

        // Calculate score
        installResults.score = (installResults.httpsOrLocalhost ? 40 : 0) +
                              (installResults.beforeInstallPrompt ? 30 : 0) +
                              (installResults.standalone ? 30 : 0);

        this.results.installability = installResults;
    }

    calculateOverallScore() {
        const weights = {
            manifest: 0.3,
            serviceWorker: 0.25,
            icons: 0.2,
            meta: 0.15,
            installability: 0.1
        };

        let totalScore = 0;
        Object.keys(weights).forEach(category => {
            if (this.results[category] && typeof this.results[category].score === 'number') {
                totalScore += this.results[category].score * weights[category];
            }
        });

        this.results.overall.score = Math.round(totalScore);

        if (totalScore >= 90) {
            this.results.overall.status = 'excellent';
        } else if (totalScore >= 75) {
            this.results.overall.status = 'good';
        } else if (totalScore >= 50) {
            this.results.overall.status = 'fair';
        } else {
            this.results.overall.status = 'poor';
        }
    }

    displayResults() {
        console.log('\n🎯 AIFOLIO PWA VALIDATION RESULTS');
        console.log('═'.repeat(50));

        console.log(`\n📊 Overall Score: ${this.results.overall.score}/100 (${this.results.overall.status.toUpperCase()})`);

        console.log('\n📄 Manifest:', this.results.manifest.valid ? '✅' : '❌');
        if (this.results.manifest.missing && this.results.manifest.missing.length > 0) {
            console.log('   Missing fields:', this.results.manifest.missing.join(', '));
        }

        console.log('\n⚙️ Service Worker:', this.results.serviceWorker.active ? '✅' : '❌');
        if (this.results.serviceWorker.scope) {
            console.log('   Scope:', this.results.serviceWorker.scope);
        }

        console.log('\n🎨 Icons:');
        Object.entries(this.results.icons.required).forEach(([icon, result]) => {
            console.log(`   ${icon}: ${result.exists ? '✅' : '❌'}`);
        });

        console.log('\n🏷️ Meta Tags:', this.results.meta.manifestLink ? '✅' : '❌');
        console.log('   Viewport:', this.results.meta.viewport ? '✅' : '❌');
        console.log('   Theme Color:', this.results.meta.themeColor ? '✅' : '❌');

        console.log('\n📱 Installability:', this.results.installability.httpsOrLocalhost ? '✅' : '❌');
        console.log('   HTTPS/Localhost:', this.results.installability.httpsOrLocalhost ? '✅' : '❌');
        console.log('   Install Prompt:', this.results.installability.beforeInstallPrompt ? '✅' : '❌');

        console.log('\n' + '═'.repeat(50));

        // Recommendations
        this.displayRecommendations();
    }

    displayRecommendations() {
        console.log('\n💡 RECOMMENDATIONS:');

        if (this.results.overall.score < 90) {
            if (!this.results.manifest.valid) {
                console.log('• Fix manifest.json validation errors');
            }

            if (!this.results.serviceWorker.active) {
                console.log('• Register and activate service worker');
            }

            const missingRequired = Object.entries(this.results.icons.required)
                .filter(([, result]) => !result.exists)
                .map(([icon]) => icon);

            if (missingRequired.length > 0) {
                console.log('• Add required icons:', missingRequired.join(', '));
            }

            if (!this.results.meta.manifestLink) {
                console.log('• Add manifest link to HTML head');
            }

            if (!this.results.installability.httpsOrLocalhost) {
                console.log('• Serve over HTTPS for production');
            }
        } else {
            console.log('🎉 PWA setup is excellent! Ready for production deployment.');
        }
    }
}

// Auto-run validation when script loads
if (typeof window !== 'undefined') {
    window.PWAValidator = PWAValidator;

    // Auto-validate after page load
    window.addEventListener('load', () => {
        setTimeout(async () => {
            const validator = new PWAValidator();
            await validator.validateAll();

            // Store results globally for debugging
            window.pwaValidationResults = validator.results;
        }, 1000);
    });
}

// Export for Node.js environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PWAValidator;
}

console.log('🔍 AIFOLIO PWA Validator loaded and ready');
