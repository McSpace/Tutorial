# Claude Code Integration Guide

This guide explains how to use the Sabre Flight Search Agent as a subagent within Claude Code.

## Overview

The Sabre Flight Search Agent is designed to be invoked as a specialized subagent using Claude Code's Task tool. It operates autonomously to search for flights, plan search strategies, and present results.

## Prerequisites

1. **Claude Code** installed and running
2. **Python 3.7+** with required packages
3. **Sabre API credentials** (pre-configured in `config.json`)
4. **Agent files** in your workspace

## Setup

### 1. Install Dependencies

```bash
cd /home/user/Tutorial/sabre_agent
pip install -r requirements.txt
```

### 2. Verify Installation

Run the test script to ensure everything works:

```bash
cd /home/user/Tutorial/sabre_agent
./test_agent.sh
```

Expected output:
```
✓ All tests passed! Agent is ready to use.
```

## Using the Agent in Claude Code

### Method 1: Direct Task Tool Invocation

When you need flight search capabilities, use the Task tool to invoke the agent:

```python
# In Claude Code conversation
Task(
    subagent_type="general-purpose",
    description="Search flights using Sabre",
    prompt="""
    You are a Sabre Red 360 flight search expert. Read the instructions from:
    /home/user/Tutorial/sabre_agent/agent_prompt.md

    USER REQUEST:
    Find flights from New York (JFK) to Los Angeles (LAX) on June 15th,
    economy class, prefer morning departures.

    Follow the workflow defined in the agent prompt:
    1. Create a search plan
    2. Execute Sabre commands using: python3 /home/user/Tutorial/sabre_agent/tools/sabre_api.py '<command>' --json
    3. Analyze results
    4. Present findings clearly

    Available reference: /home/user/Tutorial/SABRE_RED_360_TICKET_SEARCH_GUIDE.md
    """
)
```

### Method 2: Natural Language Request

Simply describe what you need, and Claude Code can invoke the agent:

**You say:**
```
Use the Sabre flight search agent to find business class flights from
London to Tokyo on August 20th. The agent is located at
/home/user/Tutorial/sabre_agent/
```

**Claude Code will:**
1. Recognize the request requires specialized flight search
2. Load the agent prompt from `agent_prompt.md`
3. Execute the search workflow
4. Return structured results

## Agent Workflow

The agent follows this process autonomously:

```
┌─────────────────────────────────────┐
│  1. Receive Search Request          │
│     - Parse requirements            │
│     - Extract key parameters        │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  2. Create Search Plan              │
│     - Define search strategy        │
│     - List commands to execute      │
│     - Identify fallback options     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  3. Execute Commands                │
│     python3 sabre_api.py '<cmd>'    │
│     - Parse JSON responses          │
│     - Check for errors              │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  4. Analyze Results                 │
│     - Extract flight options        │
│     - Compare alternatives          │
│     - Check availability            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  5. Adapt Plan (if needed)          │
│     - No availability? Try alt dates│
│     - API error? Retry with fix     │
│     - Try different approach        │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  6. Present Results                 │
│     - Formatted flight options      │
│     - Recommendations               │
│     - Alternative suggestions       │
└─────────────────────────────────────┘
```

## Example Interactions

### Example 1: Simple Search

**User:**
```
@sabre-agent Find flights from NYC to Miami on July 4th
```

**Agent Process:**
```
SEARCH PLAN:
1. Basic availability: 104JULNYCMIA
2. If many results, filter by major carriers
3. Present top 5 options

Executing: python3 sabre_agent/tools/sabre_api.py '104JULNYCMIA' --json

RESULTS:
[Agent presents flight options with times, airlines, availability]

RECOMMENDATION:
Best options for different priorities...
```

### Example 2: Complex Search

**User:**
```
@sabre-agent Find the best business class option from San Francisco to
Singapore on September 10th. I prefer direct flights on Singapore
Airlines or United, but show alternatives if needed.
```

**Agent Process:**
```
SEARCH PLAN:
Phase 1 - Preferred Direct Flights:
1. SQ direct business: 110SEPSFOSIN¥SQ-J¤
2. UA direct business: 110SEPSFOSIN¥UA-J¤

Phase 2 - Alternative Direct:
3. If limited, try other carriers direct: 110SEPSFOSIN-J¤

Phase 3 - Connecting Options:
4. If no suitable direct, try via major hubs

Executing commands...

[Agent executes each step, analyzes results]

RESULTS FOUND:
Option 1: Singapore Airlines SQ31 (Direct)
- Departure: 11:30 SFO
- Arrival: 18:45+1 SIN
- Business Class: 8 seats available
[Full details...]

Option 2: United Airlines UA1 (Direct)
- Departure: 14:00 SFO
- Arrival: 21:30+1 SIN
- Business Class: 4 seats available
[Full details...]

RECOMMENDATION:
Singapore Airlines SQ31 for:
- Earlier arrival
- More seat availability
- Newer aircraft (A350)
```

### Example 3: No Availability Scenario

**User:**
```
@sabre-agent Find flights from Small Town (SBN) to London (LHR)
on December 25th
```

**Agent Process:**
```
SEARCH PLAN:
1. Try direct: 125DECSBNLHR
2. Expected: No direct flights (small market)
3. Fallback: Search via major hubs (ORD, JFK, EWR)

Executing: 125DECSBNLHR
Result: No availability (no direct service)

Adapting plan - Searching connections...

Executing: 125DECSBNORD (SBN to Chicago)
Executing: 125DECORDLHR (Chicago to London)

Executing: 125DECSBNEWK (SBN to Newark)
Executing: 125DECEWRLHR (Newark to London)

RESULTS:
Connection Option 1: Via Chicago
- SBN-ORD: AA3456 depart 06:30, arrive 07:45
- ORD-LHR: AA098 depart 17:00, arrive 07:30+1
- Total time: 19h 00m (with layover)

Connection Option 2: Via Newark
[Similar details...]

RECOMMENDATION:
Via Newark route offers:
- Shorter layover (3h vs 9h)
- Single terminal connection
- Better on-time performance
```

## Configuration Options

### Custom Credentials

To use different Sabre credentials, edit `config.json`:

```json
{
  "api_config": {
    "environment": "cert",  // or "prod"
    "credentials": {
      "username": "YOUR_USERNAME",
      "password": "YOUR_PASSWORD",
      "pcc": "YOUR_PCC"
    }
  }
}
```

### Agent Behavior Customization

Edit `agent_prompt.md` to customize:

- Search strategy priorities
- Result presentation format
- Error handling approach
- Default assumptions

### Example Customization:

```markdown
## Custom Rule: Always Prefer Star Alliance

When multiple airlines are available, prioritize:
1. United Airlines (UA)
2. Lufthansa (LH)
3. Air Canada (AC)
4. Other Star Alliance members
5. Non-alliance airlines

Modify search plan to include Star Alliance preference.
```

## Advanced Usage

### Chaining Multiple Searches

For round-trip or multi-city searches:

```python
Task(
    subagent_type="general-purpose",
    prompt="""
    Read agent prompt from: /home/user/Tutorial/sabre_agent/agent_prompt.md

    COMPLEX REQUEST:
    Plan a round-trip itinerary:
    - Outbound: NYC to Tokyo on June 1st (business class)
    - Return: Tokyo to NYC on June 15th (business class)

    Requirements:
    1. Search both legs independently
    2. Ensure compatible booking classes
    3. Consider time zones and travel time
    4. Present complete round-trip options

    Use: python3 /home/user/Tutorial/sabre_agent/tools/sabre_api.py '<cmd>' --json
    """
)
```

### Integration with Booking Workflow

The agent can be extended to:

1. **Search** for flights (current capability)
2. **Select** best option based on criteria
3. **Create PNR** (requires additional Sabre API integration)
4. **Add passenger details**
5. **Issue ticket**

See Sabre API documentation for booking workflow implementation.

## Troubleshooting

### Agent Not Responding

**Issue:** Task tool doesn't invoke agent

**Solution:**
```bash
# Verify agent files exist
ls -la /home/user/Tutorial/sabre_agent/

# Check agent_prompt.md is readable
cat /home/user/Tutorial/sabre_agent/agent_prompt.md | head -20
```

### API Connection Errors

**Issue:** "Failed to create session" or HTTP errors

**Solution:**
```bash
# Test API directly
python3 /home/user/Tutorial/sabre_agent/tools/sabre_api.py '115JUNNYCLAX' --json

# Check credentials in config.json
cat /home/user/Tutorial/sabre_agent/config.json
```

### Invalid Command Format

**Issue:** Agent receives "Invalid format" errors

**Solution:**
- Verify command syntax matches Sabre format
- Check date format (DDMMM, e.g., 01JUN)
- Ensure airport codes are valid 3-letter IATA codes
- Refer to SABRE_RED_360_TICKET_SEARCH_GUIDE.md

### Python Package Issues

**Issue:** ImportError for requests or lxml

**Solution:**
```bash
pip install -r /home/user/Tutorial/sabre_agent/requirements.txt
```

## Best Practices

### 1. Be Specific in Requests

❌ **Bad:** "Find flights to Europe"
✅ **Good:** "Find flights from JFK to London (LHR) on June 15th, economy class"

### 2. Provide Context

Include:
- Exact dates
- Origin and destination (airport codes if known)
- Class preference (economy, business, first)
- Airline preferences
- Time of day preferences
- Special requirements (direct only, etc.)

### 3. Let the Agent Plan

Don't micromanage the search process. The agent will:
- Create an optimal search plan
- Execute commands systematically
- Adapt based on results
- Present findings clearly

### 4. Review and Refine

After initial results:
```
"Can you also check flights one day earlier?"
"What if I'm flexible on airlines?"
"Show me first class options instead"
```

## Performance Tips

### Faster Searches

1. **Use specific dates** rather than date ranges
2. **Specify airline** if you have strong preference
3. **Avoid peak search times** (Sabre API may be slower)

### More Comprehensive Results

1. **Allow flexible dates** (±1-2 days)
2. **Consider nearby airports**
3. **Include connecting flights** for more options

## Integration Checklist

Before using the agent:

- [ ] Python 3.7+ installed
- [ ] Required packages installed (`pip install -r requirements.txt`)
- [ ] Test script passes (`./test_agent.sh`)
- [ ] Agent prompt file exists and is readable
- [ ] Sabre API credentials configured
- [ ] Network access to Sabre CERT environment

## Example Task Tool Calls

### Basic Pattern

```python
# Minimal invocation
Task(
    subagent_type="general-purpose",
    description="Sabre flight search",
    prompt=f"""
    Read: /home/user/Tutorial/sabre_agent/agent_prompt.md
    Request: {user_request}
    Tool: python3 /home/user/Tutorial/sabre_agent/tools/sabre_api.py '<cmd>' --json
    """
)
```

### With Context

```python
# Include additional context
Task(
    subagent_type="general-purpose",
    description="Complex flight search",
    prompt=f"""
    Agent Prompt: /home/user/Tutorial/sabre_agent/agent_prompt.md
    Command Reference: /home/user/Tutorial/SABRE_RED_360_TICKET_SEARCH_GUIDE.md

    USER CONTEXT:
    - Booking for: Business trip
    - Budget: Premium economy or business class
    - Flexibility: ±2 days on dates
    - Alliance: Prefers Star Alliance

    REQUEST: {user_request}

    TOOL: python3 /home/user/Tutorial/sabre_agent/tools/sabre_api.py '<cmd>' --json

    After search, provide:
    1. Top 3 options with full details
    2. Comparison matrix
    3. Booking recommendation
    """
)
```

## Reference Quick Links

- **Agent Prompt:** `/home/user/Tutorial/sabre_agent/agent_prompt.md`
- **Command Guide:** `/home/user/Tutorial/SABRE_RED_360_TICKET_SEARCH_GUIDE.md`
- **API Tool:** `/home/user/Tutorial/sabre_agent/tools/sabre_api.py`
- **Examples:** `/home/user/Tutorial/sabre_agent/examples/search_examples.md`
- **Config:** `/home/user/Tutorial/sabre_agent/config.json`

## Support

For issues:
1. Check **README.md** for general documentation
2. Review **examples/search_examples.md** for usage patterns
3. Run **test_agent.sh** to verify setup
4. Check Sabre Dev Studio for API status

---

**You're ready to search!** The agent handles the complexity of Sabre commands and presents clear, actionable flight options.
