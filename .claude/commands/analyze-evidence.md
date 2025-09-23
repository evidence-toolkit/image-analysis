---
name: analyze-evidence
description: Orchestrated legal evidence analysis using specialized sub-agents with cost controls and UK law compliance
---

# Legal Evidence Analysis Pipeline

This command orchestrates the complete legal evidence analysis workflow using specialized sub-agents optimized for UK employment law cases.

## Usage

```bash
/analyze-evidence <images_directory> [options]
```

### Options
- `--cost-limit <amount>` - Set maximum cost threshold (default: £10)
- `--fast` - Use faster, cost-efficient models where possible
- `--critical-only` - Focus only on critical violations
- `--detailed-report` - Generate comprehensive tribunal-ready documentation

## Orchestration Workflow

### Phase 1: Cost Estimation & Approval
1. Count images in directory
2. Estimate total analysis costs
3. Present cost breakdown by agent type
4. Request approval if >£10 total cost

### Phase 2: Evidence Triage
```
evidence-triage-agent:
- Batch classify all images
- Assign to specialized agents
- Identify critical incidents
- Optimize cost allocation
```

### Phase 3: Specialized Analysis
```
Parallel Processing by Evidence Type:

health_safety images → forensic-health-safety-agent
critical violations → critical-incident-agent
cleanliness issues → hygiene-compliance-agent
documentation gaps → records-analysis-agent
```

### Phase 4: Quality Validation
```
legal-validator-agent:
- Review all analysis for UK law compliance
- Verify evidence strength assessments
- Check expert witness standards
- Validate chain of custody
```

### Phase 5: Report Generation
```
tribunal-reporter-agent:
- Generate court-ready documentation
- Organize by legal significance
- Create comprehensive case summary
- Prepare expert witness materials
```

## Cost Management

### Automatic Cost Controls
- **£5 Warning**: Display cost alert
- **£10 Approval**: Require user confirmation
- **£25 Circuit Breaker**: Hard stop with manual override

### Cost Optimization Strategy
1. Use `gpt-5-nano` for triage (£0.02/image)
2. Use `claude-sonnet` for detailed analysis (£0.15/image)
3. Use `claude-opus` only for critical incidents (£0.50/image)
4. Batch processing for efficiency

## UK Legal Compliance Features

### Automatic Regulation Mapping
- Health & Safety at Work Act 1974
- Workplace (Health, Safety and Welfare) Regulations 1992
- Control of Substances Hazardous to Health Regulations 2002
- Food Safety Act 1990
- Management of Health and Safety at Work Regulations 1999

### Employment Tribunal Standards
- Objective, bias-free analysis
- Expert witness quality documentation
- Proper legal terminology
- Chain of custody maintenance

## Output Structure

```
evidence/
├── 01_critical_violations/     # Immediate action required
├── 02_health_safety/          # HSE regulation breaches
├── 03_cleanliness/            # Hygiene & food safety
├── 04_documentation/          # Records & compliance
├── case_summary.md            # Executive overview
├── cost_report.txt            # Billing breakdown
└── expert_witness_report.pdf  # Tribunal-ready document
```

## Error Handling & Recovery

### API Failures
- Retry with exponential backoff
- Switch to lower-cost models
- Maintain partial results
- Generate cost-adjusted reports

### Quality Assurance
- Cross-validation between agents
- Consistency checks across analysis
- UK law compliance verification
- Evidence strength validation

## Example Usage

```bash
# Standard analysis
/analyze-evidence ./workplace-photos/

# Fast, cost-efficient analysis
/analyze-evidence ./photos/ --fast --cost-limit 5

# Critical incidents only
/analyze-evidence ./incident-photos/ --critical-only

# Full tribunal preparation
/analyze-evidence ./case-evidence/ --detailed-report --cost-limit 50
```

## Cost Estimation Examples

| Image Count | Fast Mode | Standard | Detailed |
|-------------|-----------|----------|----------|
| 10 images   | £0.50     | £1.50    | £3.00    |
| 50 images   | £2.50     | £7.50    | £15.00   |
| 100 images  | £5.00     | £15.00   | £30.00   |

*Costs include all sub-agent analysis and report generation*

## Legal Quality Assurance

Every analysis includes:
- ✅ UK employment law compliance verification
- ✅ Expert witness standard documentation
- ✅ Objective, professional language
- ✅ Proper chain of custody tracking
- ✅ Tribunal-ready evidence formatting
- ✅ Cost transparency for client billing

This command ensures comprehensive, cost-controlled legal evidence analysis suitable for UK employment tribunal proceedings.