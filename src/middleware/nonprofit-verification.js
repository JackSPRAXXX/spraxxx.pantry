/**
 * SPRAXXX Pantry Nonprofit Verification Middleware
 * 
 * Founder: Jacquot Maple Monster Periard Raymond
 * Organization: SPRAXXX Legacy Foundation
 * 
 * Verifies nonprofit status for charitable resource access
 * CHARITABLE SOFTWARE - NO COMMERCIAL USE
 */

const logger = require('../utils/charitable-logger');

function nonprofitVerification(config) {
  return (req, res, next) => {
    // Skip verification for public endpoints
    const publicEndpoints = ['/', '/transparency', '/impact', '/governance', '/health'];
    if (publicEndpoints.includes(req.path)) {
      return next();
    }

    // Skip verification for GET requests to documentation
    if (req.method === 'GET' && !req.path.includes('/api/')) {
      return next();
    }

    // Require verification for resource-accessing endpoints
    const protectedEndpoints = [
      '/nonprofit/register',
      '/projects/submit', 
      '/resources/allocate',
      '/api/',
      '/admin/'
    ];

    const requiresVerification = protectedEndpoints.some(endpoint => 
      req.path.startsWith(endpoint)
    );

    if (!requiresVerification) {
      return next();
    }

    // Perform nonprofit verification
    const verification = performNonprofitVerification(req, config);
    
    if (!verification.verified) {
      logger.charitable.nonprofit('Nonprofit verification failed', {
        ip: req.ip,
        path: req.path,
        reason: verification.reason,
        requiresVerification: true
      });

      return res.status(verification.statusCode).json({
        error: 'Nonprofit Verification Required',
        message: verification.reason,
        founder: 'Jacquot Maple Monster Periard Raymond',
        organization: 'SPRAXXX Legacy Foundation',
        charitable_notice: 'This system serves verified nonprofit organizations only',
        verification_process: {
          step1: 'Submit nonprofit documentation (501c3, charity registration)',
          step2: 'Provide mission statement aligned with public benefit',
          step3: 'Commit to transparency and community oversight',
          step4: 'Accept charitable-only usage terms',
          step5: 'Participate in democratic governance processes'
        },
        required_documentation: config.nonprofitVerification.documentationTypes,
        next_steps: verification.nextSteps
      });
    }

    // Add verification context to request
    req.nonprofit = {
      verified: true,
      organizationId: verification.organizationId,
      organizationName: verification.organizationName,
      verificationLevel: verification.level,
      charitableStatus: 'confirmed',
      publicBenefit: true
    };

    logger.charitable.nonprofit('Nonprofit verification successful', {
      organizationId: verification.organizationId,
      organizationName: verification.organizationName,
      verificationLevel: verification.level,
      path: req.path
    });

    next();
  };
}

function performNonprofitVerification(req, config) {
  // Check for nonprofit identification in headers
  const nonprofitId = req.get('X-Nonprofit-ID');
  const nonprofitToken = req.get('X-Nonprofit-Token');
  const organizationName = req.get('X-Organization-Name');

  if (!nonprofitId && !organizationName) {
    return {
      verified: false,
      statusCode: 401,
      reason: 'Nonprofit identification required',
      nextSteps: [
        'Obtain nonprofit organization ID through registration process',
        'Include X-Nonprofit-ID header in requests',
        'Provide valid nonprofit verification token',
        'Ensure organization is verified in SPRAXXX Pantry system'
      ]
    };
  }

  // In a full implementation, this would check against a verified nonprofits database
  // For this initial implementation, we'll simulate the verification process
  
  // Check if this is a registration request (allowed without prior verification)
  if (req.path === '/nonprofit/register') {
    return {
      verified: true,
      organizationId: 'REGISTRATION_PENDING',
      organizationName: organizationName || 'Registering Organization',
      level: 'registration',
      charitable: true
    };
  }

  // Simulate nonprofit verification lookup
  const verificationResult = simulateNonprofitLookup(nonprofitId, organizationName, req);
  
  if (!verificationResult.found) {
    return {
      verified: false,
      statusCode: 403,
      reason: 'Nonprofit organization not verified in system',
      nextSteps: [
        'Register nonprofit organization through /nonprofit/register endpoint',
        'Submit required documentation for verification',
        'Wait for community review and approval process',
        'Obtain verified nonprofit ID and access token'
      ]
    };
  }

  if (verificationResult.status !== 'verified') {
    return {
      verified: false,
      statusCode: 403,
      reason: `Nonprofit verification status: ${verificationResult.status}`,
      nextSteps: [
        'Complete pending verification requirements',
        'Respond to any community review feedback',
        'Provide additional documentation if requested',
        'Participate in governance processes as required'
      ]
    };
  }

  // Check for valid token/credentials
  if (!nonprofitToken || !validateNonprofitToken(nonprofitToken, verificationResult)) {
    return {
      verified: false,
      statusCode: 401,
      reason: 'Invalid or missing nonprofit verification token',
      nextSteps: [
        'Obtain valid verification token from SPRAXXX Pantry system',
        'Ensure token is included in X-Nonprofit-Token header',
        'Contact SPRAXXX Legacy Foundation if token issues persist',
        'Verify token has not expired or been revoked'
      ]
    };
  }

  // Successful verification
  return {
    verified: true,
    organizationId: verificationResult.id,
    organizationName: verificationResult.name,
    level: verificationResult.verificationLevel,
    charitableStatus: 'verified',
    publicBenefit: true,
    transparencyCommitment: verificationResult.transparencyCommitment
  };
}

function simulateNonprofitLookup(nonprofitId, organizationName, req) {
  // In a real implementation, this would query a database of verified nonprofits
  // For demo purposes, we'll create a simple simulation
  
  const knownNonprofits = new Map([
    ['NPR-DEMO-001', {
      id: 'NPR-DEMO-001',
      name: 'Demo Charitable Organization',
      status: 'verified',
      verificationLevel: 'full',
      transparencyCommitment: true,
      lastVerified: '2025-09-24'
    }],
    ['NPR-DEMO-002', {
      id: 'NPR-DEMO-002', 
      name: 'Example Nonprofit Foundation',
      status: 'pending_review',
      verificationLevel: 'preliminary',
      transparencyCommitment: true,
      lastVerified: null
    }]
  ]);

  // Look up by ID first
  if (nonprofitId && knownNonprofits.has(nonprofitId)) {
    return {
      found: true,
      ...knownNonprofits.get(nonprofitId)
    };
  }

  // Look up by name
  if (organizationName) {
    for (const [id, org] of knownNonprofits.entries()) {
      if (org.name.toLowerCase().includes(organizationName.toLowerCase())) {
        return {
          found: true,
          ...org
        };
      }
    }
  }

  return {
    found: false,
    reason: 'Organization not found in verified nonprofit registry'
  };
}

function validateNonprofitToken(token, verificationResult) {
  // In a real implementation, this would validate cryptographic tokens
  // For demo purposes, we'll use a simple validation
  
  const expectedTokenPrefix = `NPT-${verificationResult.id}-`;
  const hasValidPrefix = token.startsWith(expectedTokenPrefix);
  const hasValidLength = token.length >= 32;
  const isNotExpired = true; // Would check expiration timestamp in real implementation
  
  return hasValidPrefix && hasValidLength && isNotExpired;
}

// Helper function to generate nonprofit verification token (for demo)
function generateNonprofitToken(organizationId) {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substr(2, 16);
  return `NPT-${organizationId}-${timestamp}-${random}`;
}

module.exports = nonprofitVerification;
module.exports.generateNonprofitToken = generateNonprofitToken;