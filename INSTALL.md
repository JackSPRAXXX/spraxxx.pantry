# SPRAXXX Pantry Installation Guide

**Founder:** Jacquot Maple Monster Periard Raymond  
**Organization:** SPRAXXX Legacy Foundation  
**Date:** September 24, 2025  

---

## Prerequisites

Before installing SPRAXXX Pantry, ensure you meet these requirements:

### System Requirements
- Node.js 18.0.0 or higher
- NPM 8.0.0 or higher
- Git (for cloning the repository)
- Minimum 512MB RAM
- 1GB available disk space

### Charitable Requirements
- **Verified nonprofit organization status**
- Official documentation (501(c)(3), charity registration, etc.)
- Mission statement aligned with public benefit
- Commitment to transparent operations
- Acceptance of charitable-only usage terms

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/JackSPRAXXX/spraxxx.pantry.git
cd spraxxx.pantry
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Verify Charitable Configuration

The system will automatically validate charitable configuration on startup. Ensure all ethical restrictions are in place:

```bash
node -e "console.log(require('./config/charitable.config.js'))"
```

### 4. Start the System

```bash
# Development mode
npm run dev

# Production mode
npm start
```

The system will start on port 3000 by default.

## Configuration

### Environment Variables

Create a `.env` file (not included in repository for security):

```env
# Server Configuration
PORT=3000
NODE_ENV=production

# Charitable Configuration
CHARITABLE_ONLY=true
COMMERCIAL_USE=false
MONETIZATION=false

# Nonprofit Verification
NONPROFIT_VERIFICATION_REQUIRED=true
TRANSPARENCY_REQUIRED=true

# Logging
LOG_LEVEL=info
PUBLIC_TRANSPARENCY=true
```

### Charitable Configuration

The system includes a comprehensive charitable configuration file at `config/charitable.config.js`. This file:

- Enforces charitable-only usage
- Prevents commercial exploitation
- Ensures transparent governance
- Validates ethical compliance

**DO NOT MODIFY** the charitable restrictions in this configuration.

## First-Time Setup

### 1. Verify System Health

```bash
curl http://localhost:3000/health
```

Expected response should show `"status": "serving_humanity"`.

### 2. Access Public Information

```bash
# System information
curl http://localhost:3000/

# Transparency dashboard
curl http://localhost:3000/transparency

# Impact reporting
curl http://localhost:3000/impact

# Governance information
curl http://localhost:3000/governance
```

### 3. Register Your Nonprofit Organization

To access charitable resources, your organization must be verified:

```bash
curl -X POST http://localhost:3000/nonprofit/register \
  -H "Content-Type: application/json" \
  -H "User-Agent: Mozilla/5.0 (charitable-purpose)" \
  -d '{
    "organizationName": "Your Nonprofit Name",
    "missionStatement": "Your mission aligned with public benefit...",
    "nonprofitStatus": "501c3",
    "documentation": {
      "501c3_determination_letter": "path/to/document.pdf"
    },
    "contactInformation": {
      "email": "contact@yournonprofit.org",
      "website": "https://yournonprofit.org"
    },
    "publicBenefitDescription": "Detailed description of how your organization serves the public good...",
    "transparencyCommitment": true
  }'
```

## Verification Process

After registration, your organization will undergo:

1. **Community Review** (7-14 days)
   - Verification of nonprofit documentation
   - Mission alignment assessment
   - Public benefit evaluation

2. **Advisory Board Assessment**
   - Detailed review of application
   - Ethical compliance verification
   - Community input consideration

3. **Foundation Approval**
   - Final review by SPRAXXX Legacy Foundation
   - Issuance of verification credentials
   - Access to charitable resources

## Security Considerations

### Charitable Protection
- The system actively monitors for commercial use attempts
- Violations result in immediate access blocking
- All activities are logged for transparency

### Ethical Compliance
- Requests are validated against charitable standards
- Commercial indicators trigger protection mechanisms
- Community reporting system for violations

## Usage Guidelines

### Acceptable Use
- ✅ Verified nonprofit organizations
- ✅ Public benefit projects
- ✅ Transparent reporting commitments
- ✅ Community governance participation

### Prohibited Use
- ❌ Commercial purposes
- ❌ Monetization attempts
- ❌ Private benefit over public good
- ❌ Circumventing charitable restrictions

## Troubleshooting

### Common Issues

**Error: "Charitable configuration violations"**
- Solution: Do not modify charitable restrictions in config files
- The system is designed to prevent commercial exploitation

**Error: "Nonprofit verification required"**
- Solution: Complete nonprofit registration process
- Provide valid documentation and await community approval

**Error: "Commercial usage indicators detected"**
- Solution: Ensure all requests serve charitable purposes
- Remove any commercial language or intent

**Server won't start**
- Check Node.js version (requires 18.0+)
- Verify all dependencies installed (`npm install`)
- Check logs for specific error messages

### Getting Help

For charitable usage and nonprofit partnerships:
- **Organization:** SPRAXXX Legacy Foundation
- **Founder:** Jacquot Maple Monster Periard Raymond
- **Purpose:** Serving humanity through ethical computation

## License Compliance

This installation is subject to the SPRAXXX Charitable License:

- **Commercial use is STRICTLY PROHIBITED**
- **Monetization is STRICTLY PROHIBITED**
- **Charitable purposes only**
- **Community governance required**

By installing and using this system, you agree to:
1. Use exclusively for charitable purposes
2. Participate in transparent governance
3. Accept community oversight
4. Protect the charitable mission

---

*SPRAXXX Pantry: Transforming wasted digital energy into charitable computation for the public good.*

**© 2025 SPRAXXX Legacy Foundation - Charitable Technology for Humanity**