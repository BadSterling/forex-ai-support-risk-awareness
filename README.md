# Forex AI Support & Risk Awareness Assistant

A transparent conversational prototype for forex customer support,
risk communication and AI identity-disclosure research.

## Current features

- Streamlit chat interface
- User experience-level selection
- Multiple AI identity-disclosure modes
- Rule-based intent detection
- Forex knowledge base
- Conversational risk classification
- Beginner-friendly response mode
- High-risk query warnings
- Conversation history
- Anonymous participant IDs
- Random disclosure-condition assignment
- Consent screen
- Structured conversation logging
- Response-time measurement
- Post-conversation trust survey
- Risk-awareness questionnaire
- Perceived AI identity measurement
- Anonymous CSV session export

## Supported topics

- Forex basics
- Lot sizes
- Leverage
- Margin
- Spreads
- Stop-loss orders
- Loss exposure
- Guaranteed-profit claims

## Experimental design

The prototype randomly assigns each anonymous session to one of three
AI identity-disclosure conditions:

- Explicit AI disclosure
- Brief AI disclosure
- Control condition without a prominent disclosure banner

The control condition does not claim that the assistant is human.
Information about the system remains available within the application.

After completing at least two conversation turns, participants can
complete a five-point Likert survey measuring:

- Perceived reliability
- Confidence in the assistant
- Perceived credibility
- Risk awareness
- Understanding of leverage and losses
- Clarity of AI identity disclosure

## Statistical analysis

The research dashboard includes:

- Cronbach's alpha for internal-consistency assessment
- Group means with 95% confidence intervals
- One-way ANOVA across disclosure conditions
- Eta-squared effect-size estimation
- Automated cautious statistical interpretation

The statistical interface is intended to demonstrate an analytical
workflow. Results generated from synthetic data are not empirical
research findings.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py

## Privacy

The prototype does not request names, email addresses, account numbers
or other directly identifying information.

Conversation records remain in the active Streamlit browser session
unless the user explicitly downloads them.

This portfolio prototype is not configured as a production research
data-collection system.