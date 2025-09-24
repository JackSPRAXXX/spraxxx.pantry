/**
 * SPRAXXX Pantry Charitable Logger
 * 
 * Founder: Jacquot Maple Monster Periard Raymond
 * Organization: SPRAXXX Legacy Foundation
 * 
 * Transparent logging system for charitable operations
 * All logs contribute to public accountability and transparency
 */

const winston = require('winston');
const path = require('path');

// Custom format for charitable logging
const charitableFormat = winston.format.combine(
  winston.format.timestamp(),
  winston.format.errors({ stack: true }),
  winston.format.json(),
  winston.format.printf(({ timestamp, level, message, ...meta }) => {
    const logEntry = {
      timestamp,
      level,
      message,
      charitable: {
        founder: 'Jacquot Maple Monster Periard Raymond',
        organization: 'SPRAXXX Legacy Foundation',
        purpose: 'Transparent charitable operations'
      },
      ...meta
    };
    return JSON.stringify(logEntry);
  })
);

// Create logger instance
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: charitableFormat,
  defaultMeta: {
    service: 'spraxxx-pantry',
    charitable: true,
    commercialUse: 'PROHIBITED'
  },
  transports: [
    // Console output for development
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple(),
        winston.format.printf(({ timestamp, level, message, ...meta }) => {
          const metaStr = Object.keys(meta).length ? JSON.stringify(meta, null, 2) : '';
          return `${timestamp} [SPRAXXX-PANTRY] ${level}: ${message} ${metaStr}`;
        })
      )
    }),
    
    // File logging for transparency
    new winston.transports.File({
      filename: path.join(process.cwd(), 'logs', 'charitable-operations.log'),
      maxsize: 10 * 1024 * 1024, // 10MB
      maxFiles: 5,
      tailable: true
    }),
    
    // Error logging
    new winston.transports.File({
      filename: path.join(process.cwd(), 'logs', 'charitable-errors.log'),
      level: 'error',
      maxsize: 10 * 1024 * 1024, // 10MB
      maxFiles: 5,
      tailable: true
    })
  ]
});

// Add public transparency logging
logger.add(new winston.transports.File({
  filename: path.join(process.cwd(), 'logs', 'public-transparency.log'),
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json(),
    winston.format.printf(({ timestamp, level, message, ...meta }) => {
      // Only log public-facing information for transparency
      if (meta.public === true || level === 'error') {
        return JSON.stringify({
          timestamp,
          level,
          message,
          charitable: {
            founder: 'Jacquot Maple Monster Periard Raymond',
            organization: 'SPRAXXX Legacy Foundation'
          },
          publicInfo: meta.publicInfo || 'Charitable operation logged'
        });
      }
      return null;
    }).replace(/null\n/g, '')
  )
}));

// Enhanced logging methods for charitable operations
logger.charitable = {
  // Log nonprofit activities
  nonprofit: (message, meta = {}) => {
    logger.info(message, {
      ...meta,
      category: 'nonprofit',
      public: true,
      publicInfo: 'Nonprofit organization activity'
    });
  },

  // Log resource allocation
  allocation: (message, meta = {}) => {
    logger.info(message, {
      ...meta,
      category: 'allocation',
      public: true,
      publicInfo: 'Charitable resource allocation'
    });
  },

  // Log governance activities
  governance: (message, meta = {}) => {
    logger.info(message, {
      ...meta,
      category: 'governance',
      public: true,
      publicInfo: 'Democratic governance activity'
    });
  },

  // Log commercial protection actions
  protection: (message, meta = {}) => {
    logger.warn(message, {
      ...meta,
      category: 'protection',
      public: true,
      publicInfo: 'Commercial exploitation protection'
    });
  },

  // Log violations
  violation: (message, meta = {}) => {
    logger.error(message, {
      ...meta,
      category: 'violation',
      public: true,
      publicInfo: 'License violation detected',
      severity: 'high'
    });
  },

  // Log impact measurements
  impact: (message, meta = {}) => {
    logger.info(message, {
      ...meta,
      category: 'impact',
      public: true,
      publicInfo: 'Charitable impact measurement'
    });
  },

  // Log bot redirection activities
  botRedirection: (message, meta = {}) => {
    logger.info(message, {
      ...meta,
      category: 'bot-redirection',
      public: true,
      publicInfo: 'Bot traffic redirected to charitable computation'
    });
  },

  // Log transparency activities
  transparency: (message, meta = {}) => {
    logger.info(message, {
      ...meta,
      category: 'transparency',
      public: true,
      publicInfo: 'Transparency and accountability activity'
    });
  }
};

// Create logs directory if it doesn't exist
const fs = require('fs');
const logsDir = path.join(process.cwd(), 'logs');
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir, { recursive: true });
}

// Log startup message
logger.info('SPRAXXX Pantry Charitable Logger initialized', {
  founder: 'Jacquot Maple Monster Periard Raymond',
  organization: 'SPRAXXX Legacy Foundation',
  purpose: 'Transparent logging for charitable operations',
  restrictions: 'Commercial use prohibited'
});

module.exports = logger;