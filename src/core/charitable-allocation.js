/**
 * SPRAXXX Pantry Charitable Allocation System
 * 
 * Founder: Jacquot Maple Monster Periard Raymond
 * Organization: SPRAXXX Legacy Foundation
 * 
 * Manages allocation of computational resources to verified nonprofit organizations
 * CHARITABLE SOFTWARE - NO COMMERCIAL USE
 */

const logger = require('../utils/charitable-logger');

class CharitableAllocation {
  constructor(config) {
    this.config = config;
    this.nonprofitRegistry = new Map();
    this.projectQueue = [];
    this.allocationHistory = [];
    this.impactMetrics = new Map();
    
    logger.charitable.allocation('Charitable Allocation System initialized', {
      founder: 'Jacquot Maple Monster Periard Raymond',
      organization: 'SPRAXXX Legacy Foundation',
      purpose: 'Computational charity for verified nonprofits'
    });
  }

  async registerNonprofit(registrationData) {
    const registrationId = this.generateRegistrationId();
    
    // Validate required fields
    this.validateNonprofitRegistration(registrationData);
    
    const registration = {
      id: registrationId,
      organizationName: registrationData.organizationName,
      missionStatement: registrationData.missionStatement,
      nonprofitStatus: registrationData.nonprofitStatus,
      documentation: registrationData.documentation,
      contactInformation: registrationData.contactInformation,
      requestedResources: registrationData.requestedResources,
      publicBenefitDescription: registrationData.publicBenefitDescription,
      transparencyCommitment: registrationData.transparencyCommitment,
      status: 'pending_verification',
      submissionDate: new Date().toISOString(),
      charitable: true,
      founder: 'Jacquot Maple Monster Periard Raymond',
      organization: 'SPRAXXX Legacy Foundation'
    };

    // Store registration for community review
    this.nonprofitRegistry.set(registrationId, registration);

    logger.charitable.nonprofit('New nonprofit registration submitted', {
      registrationId,
      organizationName: registrationData.organizationName,
      missionStatement: registrationData.missionStatement,
      publicBenefit: registrationData.publicBenefitDescription,
      public: true
    });

    return {
      id: registrationId,
      status: 'pending_verification',
      nextSteps: [
        'Community review of nonprofit status and mission alignment',
        'Verification of submitted documentation',
        'Ethical assessment of public benefit claims',
        'Advisory board evaluation and recommendation',
        'Final approval by SPRAXXX Legacy Foundation'
      ],
      estimatedReviewTime: '7-14 days',
      transparencyNotice: 'This application will be reviewed transparently with community input'
    };
  }

  validateNonprofitRegistration(data) {
    const required = [
      'organizationName',
      'missionStatement', 
      'nonprofitStatus',
      'documentation',
      'contactInformation',
      'publicBenefitDescription',
      'transparencyCommitment'
    ];

    const missing = required.filter(field => !data[field]);
    
    if (missing.length > 0) {
      throw new Error(`Missing required fields: ${missing.join(', ')}`);
    }

    // Validate nonprofit status documentation
    if (!this.config.nonprofitVerification.documentationTypes.some(type => 
      data.documentation[type])) {
      throw new Error('Valid nonprofit documentation required');
    }

    // Ensure transparency commitment
    if (data.transparencyCommitment !== true) {
      throw new Error('Transparency commitment required for charitable participation');
    }

    // Validate public benefit description
    if (data.publicBenefitDescription.length < 100) {
      throw new Error('Public benefit description must be detailed (minimum 100 characters)');
    }
  }

  async submitProject(projectData) {
    const projectId = this.generateProjectId();
    
    // Validate project submission
    this.validateProjectSubmission(projectData);
    
    const project = {
      id: projectId,
      nonprofitId: projectData.nonprofitId,
      projectName: projectData.projectName,
      description: projectData.description,
      computationalRequirements: projectData.computationalRequirements,
      publicBenefitGoals: projectData.publicBenefitGoals,
      timelineExpectations: projectData.timelineExpectations,
      impactMeasurements: projectData.impactMeasurements,
      transparencyPlan: projectData.transparencyPlan,
      status: 'submitted',
      submissionDate: new Date().toISOString(),
      priority: this.calculateProjectPriority(projectData),
      charitable: true
    };

    // Add to project queue
    this.projectQueue.push(project);
    this.sortProjectQueue();

    logger.charitable.allocation('New charitable project submitted', {
      projectId,
      nonprofitId: projectData.nonprofitId,
      projectName: projectData.projectName,
      publicBenefit: projectData.publicBenefitGoals,
      priority: project.priority,
      public: true
    });

    return {
      id: projectId,
      status: 'submitted',
      priority: project.priority,
      estimatedProcessing: this.estimateProcessingTime(project),
      queuePosition: this.projectQueue.findIndex(p => p.id === projectId) + 1,
      transparencyNotice: 'Project progress will be publicly reported'
    };
  }

  validateProjectSubmission(data) {
    const required = [
      'nonprofitId',
      'projectName',
      'description', 
      'computationalRequirements',
      'publicBenefitGoals',
      'impactMeasurements',
      'transparencyPlan'
    ];

    const missing = required.filter(field => !data[field]);
    
    if (missing.length > 0) {
      throw new Error(`Missing required project fields: ${missing.join(', ')}`);
    }

    // Verify nonprofit is registered and verified
    const nonprofit = this.nonprofitRegistry.get(data.nonprofitId);
    if (!nonprofit || nonprofit.status !== 'verified') {
      throw new Error('Project must be submitted by verified nonprofit organization');
    }

    // Validate public benefit goals
    if (data.publicBenefitGoals.length < 200) {
      throw new Error('Public benefit goals must be detailed (minimum 200 characters)');
    }

    // Ensure transparency plan is adequate
    if (!data.transparencyPlan.publicReporting || !data.transparencyPlan.impactSharing) {
      throw new Error('Comprehensive transparency plan required');
    }
  }

  calculateProjectPriority(projectData) {
    const factors = this.config.resourceAllocation.priorityFactors;
    let score = 0;

    // Public benefit impact (40%)
    const benefitKeywords = ['education', 'health', 'environment', 'poverty', 'research', 'humanitarian'];
    const benefitMatches = benefitKeywords.filter(keyword => 
      projectData.publicBenefitGoals.toLowerCase().includes(keyword)).length;
    score += (benefitMatches / benefitKeywords.length) * factors.publicBenefit;

    // Nonprofit status verification (20%)
    const nonprofit = this.nonprofitRegistry.get(projectData.nonprofitId);
    if (nonprofit && nonprofit.status === 'verified') {
      score += factors.nonprofitStatus;
    }

    // Transparency commitment (20%)
    if (projectData.transparencyPlan.publicReporting && 
        projectData.transparencyPlan.impactSharing &&
        projectData.transparencyPlan.communityUpdates) {
      score += factors.transparency;
    }

    // Community support (10%) - simplified for initial implementation
    score += factors.communitySupport * 0.5; // Assume moderate community support

    // Impact potential (10%)
    const urgencyKeywords = ['urgent', 'critical', 'emergency', 'immediate'];
    const hasUrgency = urgencyKeywords.some(keyword => 
      projectData.description.toLowerCase().includes(keyword));
    if (hasUrgency) {
      score += factors.impactPotential;
    }

    return Math.min(score, 1.0); // Cap at 1.0
  }

  sortProjectQueue() {
    this.projectQueue.sort((a, b) => {
      // Higher priority first, then earlier submission date
      if (b.priority !== a.priority) {
        return b.priority - a.priority;
      }
      return new Date(a.submissionDate) - new Date(b.submissionDate);
    });
  }

  estimateProcessingTime(project) {
    const baseTime = 24; // 24 hours base processing time
    const queuePosition = this.projectQueue.findIndex(p => p.id === project.id) + 1;
    const positionDelay = Math.max(0, (queuePosition - 1) * 6); // 6 hours per position
    
    return `${baseTime + positionDelay} hours`;
  }

  getPublicAllocationReport() {
    const activeProjects = this.projectQueue.length;
    const verifiedNonprofits = Array.from(this.nonprofitRegistry.values())
      .filter(np => np.status === 'verified').length;
    
    const report = {
      founder: 'Jacquot Maple Monster Periard Raymond',
      organization: 'SPRAXXX Legacy Foundation',
      purpose: 'Transparent charitable resource allocation',
      statistics: {
        verifiedNonprofits,
        activeProjects,
        totalAllocations: this.allocationHistory.length,
        charitableOnly: true
      },
      principles: {
        publicBenefit: 'Maximum positive impact for humanity',
        transparency: 'Open reporting and community oversight',
        democraticGovernance: 'Community input in allocation decisions',
        ethicalStewardship: 'Responsible use of donated computational resources'
      },
      restrictions: 'Commercial use prohibited - Charitable purposes only'
    };

    logger.charitable.transparency('Public allocation report generated', {
      report,
      public: true
    });

    return report;
  }

  generateRegistrationId() {
    return `NPR-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  generateProjectId() {
    return `CPR-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  getHealthStatus() {
    return {
      status: 'allocating_for_humanity',
      registeredNonprofits: this.nonprofitRegistry.size,
      activeProjects: this.projectQueue.length,
      completedAllocations: this.allocationHistory.length,
      charitable: true,
      publicBenefit: true
    };
  }
}

module.exports = CharitableAllocation;