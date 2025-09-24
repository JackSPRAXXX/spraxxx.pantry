/**
 * SPRAXXX Pantry - Main Application Server
 * 
 * Founder: Jacquot Maple Monster Periard Raymond
 * Organization: SPRAXXX Legacy Foundation
 * Date: September 24, 2025
 * 
 * CHARITABLE SOFTWARE - NO COMMERCIAL USE
 * This is a donation to humanity for computational charity.
 * Commercial use is theft of charitable property.
 */

const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const path = require('path');

// Import charitable configuration and validation
const charitableConfig = require('../config/charitable.config.js');

// Import core components
const BotDetectionEngine = require('./core/bot-detection');
const CharitableAllocation = require('./core/charitable-allocation');
const AuditingSystem = require('./core/auditing-system');
const CommercialProtection = require('./core/commercial-protection');

// Import middleware
const ethicalMiddleware = require('./middleware/ethical-validation');
const nonprofitVerification = require('./middleware/nonprofit-verification');
const transparencyMiddleware = require('./middleware/transparency-logging');

// Import utilities
const logger = require('./utils/charitable-logger');

class SpraxXXXPantry {
  constructor() {
    this.app = express();
    this.config = charitableConfig;
    this.components = {};
    
    // Validate charitable configuration
    this.validateCharitableSetup();
    
    // Initialize core components
    this.initializeComponents();
    
    // Setup middleware and routes
    this.setupMiddleware();
    this.setupRoutes();
    
    logger.info('SPRAXXX Pantry initialized for charitable service', {
      founder: this.config.charitable.founder,
      organization: this.config.charitable.organization,
      purpose: this.config.charitable.purpose
    });
  }

  validateCharitableSetup() {
    try {
      charitableConfig.validateCharitableConfig(this.config);
      logger.info('Charitable configuration validated successfully');
    } catch (error) {
      logger.error('CRITICAL: Charitable configuration violation detected', {
        error: error.message,
        action: 'SYSTEM_HALT'
      });
      process.exit(1);
    }
  }

  initializeComponents() {
    try {
      // Initialize core charitable components
      this.components.botDetection = new BotDetectionEngine(this.config);
      this.components.charitableAllocation = new CharitableAllocation(this.config);
      this.components.auditingSystem = new AuditingSystem(this.config);
      this.components.commercialProtection = new CommercialProtection(this.config);

      logger.info('Core charitable components initialized', {
        components: Object.keys(this.components)
      });
    } catch (error) {
      logger.error('Failed to initialize charitable components', { error: error.message });
      throw error;
    }
  }

  setupMiddleware() {
    // Security middleware
    this.app.use(helmet({
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          styleSrc: ["'self'", "'unsafe-inline'"],
          scriptSrc: ["'self'"],
          imgSrc: ["'self'", "data:", "https:"],
        },
      },
    }));

    // CORS for charitable organizations only
    this.app.use(cors({
      origin: (origin, callback) => {
        // Allow requests from verified nonprofit domains
        callback(null, true); // In production, implement proper nonprofit verification
      }
    }));

    // Parse JSON requests
    this.app.use(express.json({ limit: '10mb' }));
    this.app.use(express.urlencoded({ extended: true, limit: '10mb' }));

    // Charitable middleware stack
    this.app.use(ethicalMiddleware(this.config));
    this.app.use(nonprofitVerification(this.config));
    this.app.use(transparencyMiddleware(this.config));

    // Bot detection and redirection
    this.app.use((req, res, next) => {
      this.components.botDetection.analyzeTraffic(req, res, next);
    });

    // Commercial protection monitoring
    this.app.use((req, res, next) => {
      this.components.commercialProtection.monitorUsage(req, res, next);
    });
  }

  setupRoutes() {
    // Charitable mission information
    this.app.get('/', (req, res) => {
      res.json({
        name: 'SPRAXXX Pantry',
        founder: this.config.charitable.founder,
        organization: this.config.charitable.organization,
        purpose: this.config.charitable.purpose,
        dateCreated: this.config.charitable.dateCreated,
        missionStatement: this.config.charitable.missionStatement,
        restrictions: {
          commercialUse: 'STRICTLY PROHIBITED',
          monetization: 'STRICTLY PROHIBITED',
          charitableOnly: 'REQUIRED',
          publicBenefit: 'REQUIRED'
        },
        governance: {
          transparentDecisions: true,
          communityOversight: true,
          democraticParticipation: true,
          publicDocumentation: true
        }
      });
    });

    // Public transparency dashboard
    this.app.get('/transparency', (req, res) => {
      const auditData = this.components.auditingSystem.getPublicDashboard();
      res.json(auditData);
    });

    // Nonprofit registration endpoint
    this.app.post('/nonprofit/register', async (req, res) => {
      try {
        const registration = await this.components.charitableAllocation.registerNonprofit(req.body);
        res.json({
          status: 'pending_verification',
          message: 'Nonprofit application submitted for community review',
          registrationId: registration.id,
          nextSteps: registration.nextSteps
        });
      } catch (error) {
        logger.error('Nonprofit registration error', { error: error.message });
        res.status(400).json({ error: 'Registration failed', details: error.message });
      }
    });

    // Charitable project submission
    this.app.post('/projects/submit', async (req, res) => {
      try {
        const project = await this.components.charitableAllocation.submitProject(req.body);
        res.json({
          status: 'submitted',
          message: 'Charitable project submitted for allocation review',
          projectId: project.id,
          estimatedProcessing: project.estimatedProcessing
        });
      } catch (error) {
        logger.error('Project submission error', { error: error.message });
        res.status(400).json({ error: 'Submission failed', details: error.message });
      }
    });

    // Public impact reporting
    this.app.get('/impact', (req, res) => {
      const impactData = this.components.auditingSystem.getImpactReport();
      res.json(impactData);
    });

    // Community governance information
    this.app.get('/governance', (req, res) => {
      res.json({
        framework: 'Democratic oversight with charitable mission protection',
        structure: {
          foundation: 'SPRAXXX Legacy Foundation - Ultimate stewardship',
          advisoryBoard: 'Nonprofit organizations representation',
          community: 'Democratic participation and oversight'
        },
        decisionMaking: 'Transparent, community-input, charitable-priority',
        enforcement: 'Progressive actions with community protection',
        participation: 'Open to verified nonprofit organizations'
      });
    });

    // Violation reporting endpoint
    this.app.post('/report-violation', async (req, res) => {
      try {
        const report = await this.components.commercialProtection.reportViolation(req.body);
        res.json({
          status: 'received',
          message: 'Violation report submitted for investigation',
          reportId: report.id,
          anonymous: req.body.anonymous || false
        });
      } catch (error) {
        logger.error('Violation reporting error', { error: error.message });
        res.status(400).json({ error: 'Report submission failed', details: error.message });
      }
    });

    // Health check for charitable operations
    this.app.get('/health', (req, res) => {
      const health = {
        status: 'serving_humanity',
        charitableConfig: 'validated',
        components: Object.keys(this.components).reduce((acc, key) => {
          acc[key] = this.components[key].getHealthStatus();
          return acc;
        }, {}),
        restrictions: {
          commercialUse: 'blocked',
          monetization: 'blocked',
          charitableOnly: 'enforced'
        }
      };
      res.json(health);
    });

    // 404 handler with charitable message
    this.app.use('*', (req, res) => {
      res.status(404).json({
        message: 'SPRAXXX Pantry - Charitable computational infrastructure',
        founder: this.config.charitable.founder,
        organization: this.config.charitable.organization,
        note: 'This system serves humanity through ethical computation redirection',
        restrictions: 'Commercial use is prohibited - Charitable purposes only'
      });
    });

    // Error handler
    this.app.use((error, req, res, next) => {
      logger.error('Application error', { 
        error: error.message, 
        stack: error.stack,
        url: req.url,
        method: req.method 
      });
      
      res.status(500).json({
        error: 'System error in charitable service',
        message: 'SPRAXXX Pantry encountered an error while serving humanity',
        support: 'Please report issues to maintain charitable operations'
      });
    });
  }

  start(port = process.env.PORT || 3000) {
    const server = this.app.listen(port, () => {
      logger.info('SPRAXXX Pantry started - Serving humanity', {
        port: port,
        founder: this.config.charitable.founder,
        organization: this.config.charitable.organization,
        purpose: this.config.charitable.purpose,
        restrictions: 'NO COMMERCIAL USE - CHARITABLE ONLY'
      });
    });

    // Graceful shutdown
    process.on('SIGTERM', () => {
      logger.info('SPRAXXX Pantry shutting down gracefully');
      server.close(() => {
        logger.info('Charitable service stopped');
        process.exit(0);
      });
    });

    return server;
  }
}

// Export the charitable class
module.exports = SpraxXXXPantry;

// Start server if run directly
if (require.main === module) {
  const pantry = new SpraxXXXPantry();
  pantry.start();
}