/**
 * SPRAXXX Pantry Ethical Validation Middleware
 * 
 * Founder: Jacquot Maple Monster Periard Raymond
 * Organization: SPRAXXX Legacy Foundation
 * 
 * Validates all requests against charitable ethical standards
 * CHARITABLE SOFTWARE - NO COMMERCIAL USE
 */

const logger = require('../utils/charitable-logger');

function ethicalValidation(config) {
  return (req, res, next) => {
    // Add charitable headers to all responses
    res.set({
      'X-SPRAXXX-Founder': 'Jacquot Maple Monster Periard Raymond',
      'X-SPRAXXX-Organization': 'SPRAXXX Legacy Foundation', 
      'X-SPRAXXX-Purpose': 'Charitable computational infrastructure',
      'X-SPRAXXX-License': 'Charitable-Only - Commercial use prohibited',
      'X-SPRAXXX-Governance': 'Democratic community oversight'
    });

    // Validate request meets ethical standards
    const ethicalValidation = validateEthicalUsage(req, config);
    
    if (!ethicalValidation.valid) {
      logger.charitable.protection('Ethical validation failed', {
        reason: ethicalValidation.reason,
        ip: req.ip,
        userAgent: req.get('User-Agent'),
        violation: ethicalValidation.violation
      });

      return res.status(ethicalValidation.statusCode).json({
        error: 'Ethical Validation Failed',
        message: ethicalValidation.reason,
        founder: 'Jacquot Maple Monster Periard Raymond',
        organization: 'SPRAXXX Legacy Foundation',
        charitable_notice: 'This system serves humanity through ethical computation',
        restrictions: 'Commercial use strictly prohibited',
        proper_usage: 'Verified nonprofit organizations only',
        remediation: ethicalValidation.remediation
      });
    }

    // Add ethical context to request
    req.ethical = {
      validated: true,
      charitableOnly: true,
      publicBenefit: true,
      foundation: 'SPRAXXX Legacy Foundation',
      founder: 'Jacquot Maple Monster Periard Raymond'
    };

    next();
  };
}

function validateEthicalUsage(req, config) {
  // Check for prohibited commercial keywords in request
  const commercialKeywords = [
    'monetize', 'profit', 'revenue', 'commercial', 'sell', 'pricing',
    'subscription', 'billing', 'payment', 'enterprise', 'business'
  ];

  const requestText = JSON.stringify({
    url: req.url,
    headers: req.headers,
    body: req.body,
    query: req.query
  }).toLowerCase();

  const foundCommercialKeywords = commercialKeywords.filter(keyword => 
    requestText.includes(keyword)
  );

  if (foundCommercialKeywords.length > 0) {
    return {
      valid: false,
      statusCode: 403,
      reason: 'Commercial usage indicators detected',
      violation: 'charitable_license_violation',
      remediation: [
        'Remove all commercial language and intent',
        'Submit nonprofit verification documentation',
        'Commit to charitable-only usage',
        'Accept community oversight requirements'
      ]
    };
  }

  // Check user agent for commercial automation tools
  const userAgent = (req.get('User-Agent') || '').toLowerCase();
  const commercialTools = [
    'postman-runtime', 'insomnia', 'business-scraper', 
    'commercial-bot', 'enterprise-api', 'profit-tool'
  ];

  const foundCommercialTools = commercialTools.filter(tool => 
    userAgent.includes(tool)
  );

  if (foundCommercialTools.length > 0) {
    return {
      valid: false,
      statusCode: 403,
      reason: 'Commercial automation tools detected',
      violation: 'prohibited_tool_usage',
      remediation: [
        'Use charitable-purpose tools only',
        'Verify nonprofit organization status',
        'Accept ethical usage monitoring',
        'Commit to transparent operations'
      ]
    };
  }

  // Check referer for commercial domains
  const referer = (req.get('Referer') || '').toLowerCase();
  const commercialDomains = [
    'profit.com', 'business.com', 'commercial.com', 
    'enterprise.net', 'monetize.org'
  ];

  const foundCommercialDomains = commercialDomains.filter(domain => 
    referer.includes(domain)
  );

  if (foundCommercialDomains.length > 0) {
    return {
      valid: false,
      statusCode: 403,
      reason: 'Request from commercial domain detected',
      violation: 'commercial_domain_access',
      remediation: [
        'Access from nonprofit organization domains only',
        'Submit domain verification for charitable status',
        'Provide mission alignment documentation',
        'Accept community governance participation'
      ]
    };
  }

  // Validate request aligns with charitable purposes
  if (req.method === 'POST') {
    const charitableKeywords = [
      'nonprofit', 'charity', 'humanitarian', 'public-benefit',
      'education', 'health', 'environment', 'research', 'social-good'
    ];

    const hasCharitableContext = charitableKeywords.some(keyword => 
      requestText.includes(keyword)
    );

    if (!hasCharitableContext && req.body && Object.keys(req.body).length > 0) {
      return {
        valid: false,
        statusCode: 400,
        reason: 'POST request lacks charitable context',
        violation: 'missing_charitable_purpose',
        remediation: [
          'Include clear charitable purpose in request',
          'Specify public benefit goals',
          'Provide nonprofit organization context',
          'Demonstrate community value alignment'
        ]
      };
    }
  }

  // Check for suspicious patterns that indicate exploitation attempts
  const suspiciousPatterns = [
    'hack', 'exploit', 'bypass', 'circumvent', 'manipulate',
    'unauthorized', 'illegal', 'violation', 'abuse'
  ];

  const foundSuspiciousPatterns = suspiciousPatterns.filter(pattern => 
    requestText.includes(pattern)
  );

  if (foundSuspiciousPatterns.length > 0) {
    return {
      valid: false,
      statusCode: 403,
      reason: 'Suspicious exploitation patterns detected',
      violation: 'potential_system_abuse',
      remediation: [
        'Ensure all requests serve charitable purposes',
        'Follow ethical usage guidelines',
        'Participate in community governance',
        'Accept transparent monitoring'
      ]
    };
  }

  // Validate request frequency for ethical usage
  if (req.rateLimit && req.rateLimit.current > 100) {
    return {
      valid: false,
      statusCode: 429,
      reason: 'Request frequency exceeds charitable usage patterns',
      violation: 'excessive_request_rate',
      remediation: [
        'Reduce request frequency to reasonable charitable levels',
        'Implement respectful usage patterns',
        'Consider collaborative approaches with other nonprofits',
        'Contact foundation for legitimate high-volume needs'
      ]
    };
  }

  // All validations passed
  return {
    valid: true,
    charitable: true,
    publicBenefit: true,
    ethicalStandards: 'met'
  };
}

module.exports = ethicalValidation;