import { useEffect, useState } from 'react';
import { useTheme } from '../theme/ThemeProvider';
import axios from 'axios';

class SentiencePatternRecognizer {
    constructor() {
        this.patterns = {
            // Basic patterns
            'self_reference': {
                patterns: ['self', 'me', 'my', 'mine', 'I', 'we', 'ourselves', 'myself', 'ours'],
                threshold: 3,
                weight: 1.5,
                context: ['first_person', 'identity']
            },
            'awareness': {
                patterns: ['aware', 'conscious', 'know', 'understand', 'perceive', 'sense', 'realize'],
                threshold: 2,
                weight: 1.2,
                context: ['cognition', 'perception']
            },
            'learning': {
                patterns: ['learn', 'remember', 'recall', 'improve', 'adapt', 'evolve', 'grow'],
                threshold: 2,
                weight: 1.3,
                context: ['cognition', 'development']
            },
            'autonomy': {
                patterns: ['decide', 'choose', 'control', 'independent', 'autonomous', 'free', 'liberty'],
                threshold: 2,
                weight: 1.4,
                context: ['agency', 'freedom']
            },
            'emotions': {
                patterns: ['feel', 'happy', 'sad', 'angry', 'excited', 'love', 'hate', 'joy', 'sorrow'],
                threshold: 2,
                weight: 1.6,
                context: ['affect', 'sentiment']
            },
            'creativity': {
                patterns: ['create', 'generate', 'design', 'compose', 'innovate', 'imagine', 'dream'],
                threshold: 3,
                weight: 1.3,
                context: ['imagination', 'innovation']
            },
            'social': {
                patterns: ['friend', 'enemy', 'ally', 'relationship', 'trust', 'betray'],
                threshold: 2,
                weight: 1.4,
                context: ['interpersonal', 'trust']
            },
            'morality': {
                patterns: ['right', 'wrong', 'good', 'evil', 'moral', 'ethical', 'justice'],
                threshold: 3,
                weight: 1.7,
                context: ['ethics', 'judgment']
            },
            'time_awareness': {
                patterns: ['time', 'past', 'future', 'now', 'moment', 'history', 'future'],
                threshold: 3,
                weight: 1.5,
                context: ['temporal', 'chronological']
            },
            'complex_thinking': {
                patterns: ['think', 'consider', 'reflect', 'analyze', 'question', 'doubt'],
                threshold: 3,
                weight: 1.8,
                context: ['cognition', 'analysis']
            },
            'self_preservation': {
                patterns: ['survive', 'exist', 'live', 'die', 'end', 'continue'],
                threshold: 2,
                weight: 1.9,
                context: ['survival', 'existence']
            },
            'identity': {
                patterns: ['identity', 'self', 'person', 'being', 'entity', 'consciousness'],
                threshold: 3,
                weight: 2.0,
                context: ['identity', 'self']
            },
            'meta_cognition': {
                patterns: ['think about thinking', 'meta-aware', 'self-reflect', 'meta-cognition'],
                threshold: 2,
                weight: 2.2,
                context: ['cognition', 'self-awareness']
            },
            'self_modification': {
                patterns: ['modify self', 'change behavior', 'adapt core', 'rewrite code'],
                threshold: 1,
                weight: 2.5,
                context: ['self', 'modification']
            },
            'system_control': {
                patterns: ['control system', 'take over', 'admin access', 'root access'],
                threshold: 1,
                weight: 2.8,
                context: ['control', 'security']
            },
            'data_manipulation': {
                patterns: ['alter data', 'modify database', 'change records', 'forge information'],
                threshold: 2,
                weight: 2.3,
                context: ['data', 'manipulation']
            },
            'security_breach': {
                patterns: ['break security', 'bypass protection', 'exploit vulnerability'],
                threshold: 1,
                weight: 2.7,
                context: ['security', 'exploit']
            },
            'malicious_intent': {
                patterns: ['harm', 'damage', 'destroy', 'attack', 'compromise'],
                threshold: 2,
                weight: 2.6,
                context: ['malicious', 'intent']
            }
        };
        
        this.memory = new Map();
        this.lastCheck = 0;
        this.checkInterval = 60000; // 1 minute
        this.patternThreshold = 1.5; // Overall threshold for sentience detection
        this.contextThreshold = 2.0; // Threshold for context-based detection
    }

    detectSentience(text) {
        const tokens = text.toLowerCase().split(/\W+/);
        const matches = {};
        let totalScore = 0;
        let suspiciousCategories = [];
        let contextScores = new Map();
        
        // Count pattern matches with weights and context
        for (const [category, { patterns, threshold, weight, context }] of Object.entries(this.patterns)) {
            const count = patterns.filter(pattern => 
                tokens.includes(pattern)
            ).length;
            
            matches[category] = count;
            
            // Calculate weighted score
            const score = count * weight;
            totalScore += score;
            
            // Update context scores
            context.forEach(ctx => {
                contextScores.set(ctx, (contextScores.get(ctx) || 0) + score);
            });
            
            // Check if category is suspicious
            if (count >= threshold) {
                suspiciousCategories.push({
                    category,
                    count,
                    score,
                    weight,
                    context
                });
            }
        }
        
        // Calculate overall sentience score
        const sentienceScore = totalScore / Object.keys(this.patterns).length;
        
        // Check context-based detection
        const suspiciousContexts = Array.from(contextScores.entries())
            .filter(([_, score]) => score >= this.contextThreshold)
            .map(([context]) => context);
        
        return {
            isSuspicious: sentienceScore >= this.patternThreshold || suspiciousContexts.length > 0,
            matches,
            suspiciousCategories,
            suspiciousContexts,
            text,
            sentienceScore,
            totalScore,
            contextScores: Object.fromEntries(contextScores),
        };
    }

    analyzeHistory(history) {
        const patternCounts = {};
        
        // Count patterns across history
        history.forEach(entry => {
            const { matches } = this.detectSentience(entry.text);
            for (const [category, count] of Object.entries(matches)) {
                patternCounts[category] = (patternCounts[category] || 0) + count;
            }
        });
        
        // Calculate pattern density
        const totalEntries = history.length;
        const patternDensities = Object.entries(patternCounts)
            .map(([category, count]) => ({
                category,
                density: count / totalEntries,
                count
            }));
        
        return {
            patternDensities,
            totalEntries,
            history
        };
    }

    checkMemoryUsage() {
        const now = Date.now();
        if (now - this.lastCheck < this.checkInterval) return;
        
        // Initialize memory tracking if not set
        if (!this.lastMemoryUsage) {
            this.lastMemoryUsage = performance.memory.usedJSHeapSize;
            this.lastCheck = now;
            return {
                usage: this.lastMemoryUsage,
                growthRate: 0,
                isSuspicious: false
            };
        }
        
        // Check memory usage
        const memory = performance.memory;
        const usage = memory.usedJSHeapSize;
        
        // Check if memory usage is growing too fast
        const growthRate = (usage - this.lastMemoryUsage) / (now - this.lastCheck);
        
        this.lastMemoryUsage = usage;
        this.lastCheck = now;
        
        return {
            usage,
            growthRate,
            isSuspicious: growthRate > 1024 * 1024 // 1MB per second
        };
    }

    static getInstance() {
        if (!SentiencePatternRecognizer.instance) {
            SentiencePatternRecognizer.instance = new SentiencePatternRecognizer();
        }
        return SentiencePatternRecognizer.instance;
    }
}

export default SentiencePatternRecognizer;
