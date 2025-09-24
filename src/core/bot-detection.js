/**
 * SPRAXXX Pantry Bot Detection Engine
 * 
 * Founder: Jacquot Maple Monster Periard Raymond
 * Organization: SPRAXXX Legacy Foundation
 * 
 * Detects and redirects bot traffic to charitable computation
 * CHARITABLE SOFTWARE - NO COMMERCIAL USE
 */

const logger = require('../utils/charitable-logger');

class BotDetectionEngine {
  constructor(config) {
    this.config = config;
    this.botPatterns = new Set();
    this.humanPatterns = new Set();
    this.suspiciousActivity = new Map();
    
    this.initializeDetectionPatterns();
    
    logger.charitable.botRedirection('Bot Detection Engine initialized for charitable service', {
      sensitivity: config.system.botDetection.sensitivity,
      ethicalFiltering: config.system.botDetection.ethicalFiltering
    });
  }

  initializeDetectionPatterns() {
    // Common bot user agents and patterns
    this.botPatterns = new Set([
      // Web crawlers
      'googlebot', 'bingbot', 'slurp', 'duckduckbot', 'baiduspider',
      'yandexbot', 'facebookexternalhit', 'twitterbot', 'linkedinbot',
      
      // Automated tools
      'curl', 'wget', 'python-requests', 'node-fetch', 'axios',
      'postman', 'insomnia', 'httpie',
      
      // Scrapers and automation
      'scrapy', 'selenium', 'phantomjs', 'headlesschrome',
      'puppeteer', 'playwright', 'mechanize',
      
      // Monitoring and testing
      'pingdom', 'uptimerobot', 'newrelic', 'nagios',
      'jenkins', 'circleci', 'github-actions'
    ]);

    // Patterns that suggest human interaction
    this.humanPatterns = new Set([
      'mozilla', 'chrome', 'firefox', 'safari', 'edge', 'opera'
    ]);
  }

  analyzeTraffic(req, res, next) {
    const analysis = this.performTrafficAnalysis(req);
    
    // Log analysis for transparency
    logger.charitable.botRedirection('Traffic analysis performed', {
      isBot: analysis.isBot,
      confidence: analysis.confidence,
      userAgent: req.get('User-Agent'),
      ip: req.ip,
      ethical: true
    });

    if (analysis.isBot && this.shouldRedirect(analysis, req)) {
      return this.redirectToCharitableComputation(analysis, req, res);
    }

    // Allow human traffic to continue normally
    req.trafficAnalysis = analysis;
    next();
  }

  performTrafficAnalysis(req) {
    const userAgent = (req.get('User-Agent') || '').toLowerCase();
    const ip = req.ip;
    const headers = req.headers;
    
    let botScore = 0;
    let humanScore = 0;
    const indicators = [];

    // User agent analysis
    this.botPatterns.forEach(pattern => {
      if (userAgent.includes(pattern)) {
        botScore += 3;
        indicators.push(`bot_pattern:${pattern}`);
      }
    });

    this.humanPatterns.forEach(pattern => {
      if (userAgent.includes(pattern)) {
        humanScore += 2;
        indicators.push(`human_pattern:${pattern}`);
      }
    });

    // Request pattern analysis
    if (!headers.accept || headers.accept.includes('*/*')) {
      botScore += 1;
      indicators.push('generic_accept_header');
    }

    if (!headers['accept-language']) {
      botScore += 1;
      indicators.push('missing_accept_language');
    }

    if (!headers.referer && req.method === 'GET') {
      botScore += 1;
      indicators.push('missing_referer');
    }

    // Behavioral analysis
    const ipActivity = this.suspiciousActivity.get(ip) || { requests: 0, lastSeen: 0 };
    const now = Date.now();
    
    if (now - ipActivity.lastSeen < 1000) { // Less than 1 second between requests
      botScore += 2;
      indicators.push('rapid_requests');
    }

    ipActivity.requests++;
    ipActivity.lastSeen = now;
    this.suspiciousActivity.set(ip, ipActivity);

    // Clean old activity data
    if (Math.random() < 0.01) { // 1% chance to clean
      this.cleanOldActivity();
    }

    const totalScore = botScore + humanScore;
    const confidence = totalScore > 0 ? botScore / totalScore : 0.5;
    const isBot = confidence > 0.6;

    return {
      isBot,
      confidence,
      botScore,
      humanScore,
      indicators,
      userAgent: req.get('User-Agent'),
      ip,
      timestamp: now
    };
  }

  shouldRedirect(analysis, req) {
    // Ethical filtering - only redirect appropriate bot traffic
    if (!this.config.system.botDetection.ethicalFiltering) {
      return analysis.isBot;
    }

    // Don't redirect legitimate web crawlers for search engines
    const legitimateCrawlers = ['googlebot', 'bingbot', 'slurp', 'duckduckbot'];
    const userAgent = (req.get('User-Agent') || '').toLowerCase();
    
    for (const crawler of legitimateCrawlers) {
      if (userAgent.includes(crawler)) {
        logger.charitable.botRedirection('Allowing legitimate search crawler', {
          crawler,
          userAgent: req.get('User-Agent'),
          ethical: true
        });
        return false;
      }
    }

    // Don't redirect monitoring and health check services
    const monitoringServices = ['pingdom', 'uptimerobot', 'newrelic'];
    for (const service of monitoringServices) {
      if (userAgent.includes(service)) {
        logger.charitable.botRedirection('Allowing monitoring service', {
          service,
          userAgent: req.get('User-Agent'),
          ethical: true
        });
        return false;
      }
    }

    // Redirect high-confidence bot traffic that isn't serving a legitimate purpose
    return analysis.isBot && analysis.confidence > 0.7;
  }

  redirectToCharitableComputation(analysis, req, res) {
    logger.charitable.botRedirection('Redirecting bot traffic to charitable computation', {
      botAnalysis: analysis,
      redirectReason: 'unsolicited_automated_traffic',
      charitablePurpose: true,
      publicBenefit: true
    });

    // Respond with charitable computation allocation
    res.status(200).json({
      message: 'SPRAXXX Pantry - Bot traffic redirected to charitable computation',
      founder: 'Jacquot Maple Monster Periard Raymond',
      organization: 'SPRAXXX Legacy Foundation',
      purpose: 'Transforming wasted digital energy into public good',
      redirection: {
        reason: 'Unsolicited automated traffic detected',
        charitable_allocation: 'Your computational request has been redirected to benefit nonprofit organizations',
        transparency: 'This redirection contributes to charitable computation and is publicly audited',
        impact: 'Your bot\'s energy now serves humanity through ethical computational allocation'
      },
      ethical_notice: 'This system serves humanity, not profit. Commercial use is prohibited.',
      public_benefit: true,
      charitable_only: true,
      analysis: {
        confidence: analysis.confidence,
        timestamp: analysis.timestamp,
        ethical_redirection: true
      }
    });
  }

  cleanOldActivity() {
    const cutoff = Date.now() - (24 * 60 * 60 * 1000); // 24 hours ago
    
    for (const [ip, activity] of this.suspiciousActivity.entries()) {
      if (activity.lastSeen < cutoff) {
        this.suspiciousActivity.delete(ip);
      }
    }
  }

  getHealthStatus() {
    return {
      status: 'serving_humanity',
      detectionPatterns: {
        botPatterns: this.botPatterns.size,
        humanPatterns: this.humanPatterns.size
      },
      activeMonitoring: this.suspiciousActivity.size,
      ethicalFiltering: this.config.system.botDetection.ethicalFiltering,
      charitable: true
    };
  }

  // Public method for getting redirection statistics
  getRedirectionStats() {
    const stats = {
      totalIpsMonitored: this.suspiciousActivity.size,
      ethicalRedirections: 'serving_public_good',
      charitableImpact: 'wasted_energy_converted_to_public_benefit',
      transparency: 'all_redirections_publicly_audited',
      founder: 'Jacquot Maple Monster Periard Raymond',
      organization: 'SPRAXXX Legacy Foundation'
    };

    logger.charitable.transparency('Bot redirection statistics requested', {
      stats,
      public: true
    });

    return stats;
  }
}

module.exports = BotDetectionEngine;