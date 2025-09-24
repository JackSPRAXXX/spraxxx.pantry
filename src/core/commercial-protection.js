/**
 * SPRAXXX Pantry Commercial Protection System
 * 
 * Founder: Jacquot Maple Monster Periard Raymond
 * Organization: SPRAXXX Legacy Foundation
 * 
 * Protects charitable donation from commercial exploitation
 * CHARITABLE SOFTWARE - NO COMMERCIAL USE
 */

const logger = require('../utils/charitable-logger');

class CommercialProtection {
  constructor(config) {
    this.config = config;
    this.violationReports = new Map();
    this.suspiciousActivity = new Map();
    this.commercialIndicators = new Set();
    this.blockedEntities = new Set();
    
    this.initializeProtection();
  }

  initializeProtection() {
    this.initializeCommercialIndicators();
    
    logger.charitable.protection('Commercial Protection System initialized', {
      founder: 'Jacquot Maple Monster Periard Raymond',
      organization: 'SPRAXXX Legacy Foundation',
      purpose: 'Protecting charitable donation from commercial exploitation'
    });
  }

  initializeCommercialIndicators() {
    // Indicators of potential commercial use
    this.commercialIndicators = new Set([
      // Business-related keywords
      'profit', 'revenue', 'sales', 'commercial', 'business', 'enterprise',
      'monetize', 'pricing', 'subscription', 'payment', 'billing',
      'corporate', 'company', 'inc', 'llc', 'ltd', 'corp',
      
      // Competitive advantage keywords  
      'competitive', 'advantage', 'market', 'customer', 'client',
      'proprietary', 'exclusive', 'licensing', 'resell',
      
      // Exploitation indicators
      'exploit', 'leverage', 'maximize', 'optimize', 'scale',
      'automation', 'efficiency', 'productivity'
    ]);
  }

  monitorUsage(req, res, next) {
    const analysis = this.analyzeRequest(req);
    
    if (analysis.suspiciousCommercial) {
      return this.handleSuspiciousActivity(analysis, req, res);
    }

    if (analysis.violatesLicense) {
      return this.blockCommercialViolation(analysis, req, res);
    }

    // Log monitoring activity
    if (analysis.requiresMonitoring) {
      this.logSuspiciousActivity(analysis, req);
    }

    next();
  }

  analyzeRequest(req) {
    const userAgent = (req.get('User-Agent') || '').toLowerCase();
    const referer = (req.get('Referer') || '').toLowerCase();
    const ip = req.ip;
    const headers = req.headers;
    
    let commercialScore = 0;
    const indicators = [];

    // Check user agent for commercial tools
    this.commercialIndicators.forEach(indicator => {
      if (userAgent.includes(indicator)) {
        commercialScore += 2;
        indicators.push(`user_agent:${indicator}`);
      }
    });

    // Check referer for commercial domains
    if (referer) {
      this.commercialIndicators.forEach(indicator => {
        if (referer.includes(indicator)) {
          commercialScore += 3;
          indicators.push(`referer:${indicator}`);
        }
      });
    }

    // Check for business domains
    const businessDomains = ['.com', '.biz', '.corp', '.enterprise'];
    if (referer && businessDomains.some(domain => referer.includes(domain))) {
      commercialScore += 1;
      indicators.push('business_domain_referer');
    }

    // Check request patterns
    if (req.method === 'POST' && req.path.includes('api')) {
      commercialScore += 1;
      indicators.push('api_usage_pattern');
    }

    // Check for automation tools
    const automationTools = ['selenium', 'puppeteer', 'playwright', 'cypress'];
    if (automationTools.some(tool => userAgent.includes(tool))) {
      commercialScore += 2;
      indicators.push('automation_tool');
    }

    // Previous violation history
    if (this.blockedEntities.has(ip)) {
      commercialScore += 5;
      indicators.push('previously_blocked');
    }

    const analysis = {
      ip,
      commercialScore,
      indicators,
      timestamp: Date.now(),
      suspiciousCommercial: commercialScore >= 4,
      violatesLicense: commercialScore >= 6,
      requiresMonitoring: commercialScore >= 2,
      userAgent: req.get('User-Agent'),
      referer: req.get('Referer')
    };

    return analysis;
  }

  handleSuspiciousActivity(analysis, req, res) {
    logger.charitable.protection('Suspicious commercial activity detected', {
      ip: analysis.ip,
      commercialScore: analysis.commercialScore,
      indicators: analysis.indicators,
      action: 'enhanced_monitoring'
    });

    // Store for enhanced monitoring
    this.suspiciousActivity.set(analysis.ip, analysis);

    // Add warning headers
    res.set({
      'X-SPRAXXX-Notice': 'Charitable system - Commercial use prohibited',
      'X-SPRAXXX-Warning': 'Activity monitored for license compliance',
      'X-SPRAXXX-Foundation': 'SPRAXXX Legacy Foundation'
    });

    // Continue with enhanced monitoring
    req.commercialMonitoring = true;
    return this.next();
  }

  blockCommercialViolation(analysis, req, res) {
    logger.charitable.violation('Commercial license violation blocked', {
      ip: analysis.ip,
      commercialScore: analysis.commercialScore,
      indicators: analysis.indicators,
      action: 'access_blocked',
      severity: 'high'
    });

    // Add to blocked entities
    this.blockedEntities.add(analysis.ip);

    // Return violation notice
    res.status(403).json({
      error: 'Commercial License Violation',
      message: 'SPRAXXX Pantry is charitable software - Commercial use is strictly prohibited',
      founder: 'Jacquot Maple Monster Periard Raymond',
      organization: 'SPRAXXX Legacy Foundation',
      violation: {
        type: 'commercial_exploitation_attempt',
        severity: 'license_violation',
        consequence: 'access_blocked',
        legal_notice: 'Commercial use constitutes theft of charitable property'
      },
      charitable_notice: {
        purpose: 'This system serves humanity through charitable computation',
        restrictions: 'NO commercial use, monetization, or profit generation',
        proper_use: 'Verified nonprofit organizations only',
        governance: 'Community oversight and transparent accountability'
      },
      remediation: {
        nonprofit_verification: 'Submit valid nonprofit documentation',
        charitable_mission: 'Demonstrate alignment with public benefit',
        transparency_commitment: 'Accept community oversight requirements',
        ethical_compliance: 'Agree to charitable-only usage terms'
      },
      contact: 'SPRAXXX Legacy Foundation for charitable usage inquiries'
    });
  }

  logSuspiciousActivity(analysis, req) {
    const activity = this.suspiciousActivity.get(analysis.ip) || {
      firstSeen: analysis.timestamp,
      requestCount: 0,
      indicators: new Set()
    };

    activity.requestCount++;
    activity.lastSeen = analysis.timestamp;
    analysis.indicators.forEach(indicator => activity.indicators.add(indicator));

    this.suspiciousActivity.set(analysis.ip, activity);

    logger.charitable.protection('Commercial monitoring activity logged', {
      ip: analysis.ip,
      requestCount: activity.requestCount,
      indicatorCount: activity.indicators.size,
      public: false
    });
  }

  async reportViolation(reportData) {
    const reportId = this.generateReportId();
    
    const report = {
      id: reportId,
      type: reportData.type || 'license_violation',
      description: reportData.description,
      evidence: reportData.evidence,
      reporterInfo: reportData.anonymous ? 'anonymous' : reportData.reporterInfo,
      suspectedEntity: reportData.suspectedEntity,
      timestamp: new Date().toISOString(),
      status: 'under_investigation',
      charitable: true,
      public: !reportData.sensitive
    };

    this.violationReports.set(reportId, report);

    logger.charitable.violation('Violation report submitted', {
      reportId,
      type: report.type,
      anonymous: reportData.anonymous,
      public: true
    });

    // Auto-investigate if sufficient evidence
    if (reportData.evidence && reportData.evidence.length > 0) {
      this.autoInvestigate(report);
    }

    return report;
  }

  autoInvestigate(report) {
    logger.charitable.protection('Auto-investigation initiated', {
      reportId: report.id,
      type: report.type,
      evidence: report.evidence?.length || 0
    });

    // Enhanced monitoring for reported entity
    if (report.suspectedEntity.ip) {
      const existing = this.suspiciousActivity.get(report.suspectedEntity.ip) || {};
      existing.violationReport = report.id;
      existing.enhanced_monitoring = true;
      this.suspiciousActivity.set(report.suspectedEntity.ip, existing);
    }

    // Update report status
    report.status = 'investigating';
    report.investigationStarted = new Date().toISOString();
  }

  getProtectionReport() {
    const report = {
      founder: 'Jacquot Maple Monster Periard Raymond',
      organization: 'SPRAXXX Legacy Foundation',
      purpose: 'Commercial exploitation protection report',
      generated: new Date().toISOString(),
      
      summary: {
        totalViolationReports: this.violationReports.size,
        blockedEntities: this.blockedEntities.size,
        suspiciousActivities: this.suspiciousActivity.size,
        protectionActive: true
      },

      protectionMechanisms: {
        commercialDetection: 'Automated scanning for commercial indicators',
        licenseEnforcement: 'Progressive actions against violations',
        communityReporting: 'Anonymous violation reporting system',
        transparentInvestigation: 'Public investigation processes'
      },

      violationCategories: this.getViolationCategories(),

      enforcement_actions: {
        warnings_issued: Array.from(this.suspiciousActivity.values()).length,
        access_blocked: this.blockedEntities.size,
        investigations_active: Array.from(this.violationReports.values())
          .filter(r => r.status === 'investigating').length
      },

      charitable_protection: {
        mission: 'Protecting charitable donation to humanity',
        restrictions: 'Commercial use strictly prohibited',
        consequences: 'Legal action for exploitation attempts',
        community_vigilance: 'Transparent reporting and investigation'
      }
    };

    logger.charitable.transparency('Protection report generated', {
      totalReports: report.summary.totalViolationReports,
      blockedEntities: report.summary.blockedEntities,
      public: true
    });

    return report;
  }

  getViolationCategories() {
    const categories = {};
    
    for (const report of this.violationReports.values()) {
      const type = report.type;
      if (!categories[type]) {
        categories[type] = {
          count: 0,
          lastReported: report.timestamp,
          status: 'monitoring'
        };
      }
      categories[type].count++;
      if (new Date(report.timestamp) > new Date(categories[type].lastReported)) {
        categories[type].lastReported = report.timestamp;
      }
    }

    return categories;
  }

  generateReportId() {
    return `VIO-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  getHealthStatus() {
    return {
      status: 'protecting_charitable_mission',
      violationReports: this.violationReports.size,
      blockedEntities: this.blockedEntities.size,
      suspiciousActivities: this.suspiciousActivity.size,
      protectionActive: true,
      charitable: true
    };
  }
}

module.exports = CommercialProtection;