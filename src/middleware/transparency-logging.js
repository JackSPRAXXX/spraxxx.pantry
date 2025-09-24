/**
 * SPRAXXX Pantry Transparency Logging Middleware
 * 
 * Founder: Jacquot Maple Monster Periard Raymond
 * Organization: SPRAXXX Legacy Foundation
 * 
 * Logs all activities for public transparency and accountability
 * CHARITABLE SOFTWARE - NO COMMERCIAL USE
 */

const logger = require('../utils/charitable-logger');

function transparencyLogging(config) {
  return (req, res, next) => {
    const startTime = Date.now();
    
    // Log incoming request
    logIncomingRequest(req, config);
    
    // Capture response details
    const originalSend = res.send;
    const originalJson = res.json;
    let responseBody = null;
    let responseSize = 0;

    // Override res.send to capture response
    res.send = function(body) {
      responseBody = body;
      responseSize = Buffer.byteLength(body || '', 'utf8');
      return originalSend.call(this, body);
    };

    // Override res.json to capture JSON responses
    res.json = function(obj) {
      responseBody = obj;
      responseSize = Buffer.byteLength(JSON.stringify(obj || {}), 'utf8');
      return originalJson.call(this, obj);
    };

    // Log response when finished
    res.on('finish', () => {
      const endTime = Date.now();
      logResponse(req, res, responseBody, responseSize, endTime - startTime, config);
    });

    next();
  };
}

function logIncomingRequest(req, config) {
  const publicRequest = isPublicRequest(req.path);
  const charitablePurpose = identifyCharitablePurpose(req);
  
  const requestLog = {
    timestamp: new Date().toISOString(),
    method: req.method,
    path: req.path,
    ip: req.ip,
    userAgent: req.get('User-Agent'),
    nonprofit: req.nonprofit?.organizationName || 'unverified',
    charitablePurpose,
    public: publicRequest,
    ethical: req.ethical?.validated || false,
    founder: 'Jacquot Maple Monster Periard Raymond',
    organization: 'SPRAXXX Legacy Foundation'
  };

  // Add query parameters for transparency (sanitized)
  if (Object.keys(req.query).length > 0) {
    requestLog.queryParams = sanitizeForTransparency(req.query);
  }

  // Log body for POST/PUT requests (sanitized)
  if ((req.method === 'POST' || req.method === 'PUT') && req.body) {
    requestLog.requestBody = sanitizeForTransparency(req.body);
  }

  if (publicRequest) {
    logger.charitable.transparency('Public request received', requestLog);
  } else {
    logger.info('Request received', requestLog);
  }
}

function logResponse(req, res, responseBody, responseSize, duration, config) {
  const publicRequest = isPublicRequest(req.path);
  const charitableImpact = assessCharitableImpact(req, res);
  
  const responseLog = {
    timestamp: new Date().toISOString(),
    method: req.method,
    path: req.path,
    statusCode: res.statusCode,
    responseSize,
    duration,
    ip: req.ip,
    nonprofit: req.nonprofit?.organizationName || 'unverified',
    charitableImpact,
    public: publicRequest,
    founder: 'Jacquot Maple Monster Periard Raymond',
    organization: 'SPRAXXX Legacy Foundation'
  };

  // Include response body for transparency where appropriate
  if (publicRequest && shouldLogResponseBody(req, res)) {
    responseLog.responseBody = sanitizeForTransparency(responseBody);
  }

  // Log errors with higher visibility
  if (res.statusCode >= 400) {
    logger.charitable.protection('Request resulted in error', {
      ...responseLog,
      errorType: getErrorType(res.statusCode),
      public: true
    });
  } else if (publicRequest) {
    logger.charitable.transparency('Public request completed', responseLog);
  } else {
    logger.info('Request completed', responseLog);
  }

  // Log charitable activities specifically
  if (charitableImpact.type !== 'none') {
    logger.charitable[charitableImpact.category](charitableImpact.message, {
      ...responseLog,
      impactType: charitableImpact.type,
      publicBenefit: true,
      public: true
    });
  }
}

function isPublicRequest(path) {
  const publicPaths = [
    '/',
    '/transparency',
    '/impact', 
    '/governance',
    '/health',
    '/nonprofit/register',
    '/projects/submit',
    '/report-violation'
  ];

  return publicPaths.includes(path) || path.startsWith('/api/public/');
}

function identifyCharitablePurpose(req) {
  const charitableKeywords = [
    'nonprofit', 'charity', 'humanitarian', 'public-benefit',
    'education', 'health', 'environment', 'research', 'social-good'
  ];

  const requestText = JSON.stringify({
    path: req.path,
    body: req.body,
    query: req.query
  }).toLowerCase();

  const foundKeywords = charitableKeywords.filter(keyword => 
    requestText.includes(keyword)
  );

  if (foundKeywords.length > 0) {
    return {
      identified: true,
      keywords: foundKeywords,
      type: 'charitable_activity'
    };
  }

  return {
    identified: false,
    type: 'general_request'
  };
}

function assessCharitableImpact(req, res) {
  const path = req.path;
  const method = req.method;
  const statusCode = res.statusCode;

  // Successful nonprofit registration
  if (path === '/nonprofit/register' && method === 'POST' && statusCode < 400) {
    return {
      type: 'nonprofit_registration',
      category: 'nonprofit',
      message: 'New nonprofit organization registered for charitable participation',
      impact: 'community_growth'
    };
  }

  // Successful project submission
  if (path === '/projects/submit' && method === 'POST' && statusCode < 400) {
    return {
      type: 'project_submission', 
      category: 'allocation',
      message: 'Charitable project submitted for resource allocation',
      impact: 'charitable_opportunity'
    };
  }

  // Transparency dashboard access
  if (path === '/transparency' && method === 'GET') {
    return {
      type: 'transparency_access',
      category: 'transparency',
      message: 'Public transparency dashboard accessed',
      impact: 'public_accountability'
    };
  }

  // Impact report access
  if (path === '/impact' && method === 'GET') {
    return {
      type: 'impact_reporting',
      category: 'impact',
      message: 'Charitable impact report accessed',
      impact: 'transparency_engagement'
    };
  }

  // Violation reporting
  if (path === '/report-violation' && method === 'POST' && statusCode < 400) {
    return {
      type: 'violation_report',
      category: 'protection', 
      message: 'Community violation report submitted',
      impact: 'community_protection'
    };
  }

  // Bot redirection (detected in response headers or content)
  if (res.get('X-SPRAXXX-Notice') || (typeof responseBody === 'object' && responseBody?.redirection)) {
    return {
      type: 'bot_redirection',
      category: 'botRedirection',
      message: 'Bot traffic redirected to charitable computation',
      impact: 'energy_conservation'
    };
  }

  return {
    type: 'none',
    category: 'general',
    message: 'General system activity',
    impact: 'system_operation'
  };
}

function shouldLogResponseBody(req, res) {
  // Log response bodies for public endpoints that provide information
  const informationalPaths = [
    '/',
    '/transparency', 
    '/impact',
    '/governance',
    '/health'
  ];

  return informationalPaths.includes(req.path) && res.statusCode < 400;
}

function sanitizeForTransparency(data) {
  if (!data || typeof data !== 'object') {
    return data;
  }

  const sensitiveFields = [
    'password', 'token', 'secret', 'key', 'credential',
    'ssn', 'taxid', 'bankaccount', 'creditcard',
    'personal', 'private', 'confidential'
  ];

  const sanitized = {};
  
  for (const [key, value] of Object.entries(data)) {
    const lowerKey = key.toLowerCase();
    const isSensitive = sensitiveFields.some(field => lowerKey.includes(field));
    
    if (isSensitive) {
      sanitized[key] = '[REDACTED_FOR_PRIVACY]';
    } else if (typeof value === 'object' && value !== null) {
      sanitized[key] = sanitizeForTransparency(value);
    } else {
      sanitized[key] = value;
    }
  }

  return sanitized;
}

function getErrorType(statusCode) {
  if (statusCode === 400) return 'bad_request';
  if (statusCode === 401) return 'unauthorized';
  if (statusCode === 403) return 'forbidden_commercial_use';
  if (statusCode === 404) return 'not_found';
  if (statusCode === 429) return 'rate_limit_exceeded';
  if (statusCode >= 500) return 'server_error';
  return 'unknown_error';
}

module.exports = transparencyLogging;