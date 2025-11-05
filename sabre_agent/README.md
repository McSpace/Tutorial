# Sabre Red 360 Flight Search Agent

An expert AI agent specialized in searching for flight tickets using Sabre Red 360 terminal commands through the Sabre SOAP API.

## Overview

This subagent is designed to work with Claude Code and provides intelligent flight search capabilities using Sabre's Global Distribution System (GDS). The agent can:

- Plan multi-step search strategies
- Execute Sabre terminal commands via SOAP API
- Interpret and analyze flight availability results
- Adapt search plans based on results
- Suggest alternatives and best options

## Features

✅ **Intelligent Planning**: Creates structured search plans before executing commands
✅ **API Integration**: Direct connection to Sabre CERT environment for testing
✅ **Adaptive Search**: Adjusts strategy based on results and requirements
✅ **Result Analysis**: Interprets Sabre responses and presents clear options
✅ **Error Handling**: Gracefully handles API errors and provides alternatives
✅ **Best Practices**: Follows Sabre GDS conventions and search optimization

## Architecture

```
sabre_agent/
├── agent_prompt.md          # Agent instructions and capabilities
├── config.json              # Agent configuration
├── requirements.txt         # Python dependencies
├── tools/
│   └── sabre_api.py        # SOAP API client for Sabre
├── examples/
│   └── search_examples.md  # Usage examples
└── README.md               # This file
```

## Prerequisites

### 1. Python Environment
```bash
python3 --version  # Requires Python 3.7+
```

### 2. Install Dependencies
```bash
cd sabre_agent
pip install -r requirements.txt
```

### 3. Sabre API Credentials
This agent is pre-configured with CERT (testing) environment credentials:
- **Username**: 302596
- **Password**: lon23don
- **PCC/Office ID**: U3VL
- **Environment**: CERT (https://webservices.cert.platform.sabre.com)

> **Note**: For production use, update credentials in `config.json` and change environment to `prod`

## Installation

### Option 1: Manual Setup
1. Clone or copy the `sabre_agent` directory to your project
2. Install Python dependencies:
   ```bash
   pip install -r sabre_agent/requirements.txt
   ```
3. Verify the API client works:
   ```bash
   python3 sabre_agent/tools/sabre_api.py '115JUNNYCLAX' --json
   ```

### Option 2: Using with Claude Code
1. Place the `sabre_agent` directory in your Claude Code workspace
2. The agent can be invoked using the Task tool with a custom prompt
3. Reference the agent prompt file when creating tasks

## Usage

### Direct API Usage

Execute a single Sabre command:

```bash
python3 sabre_agent/tools/sabre_api.py '<COMMAND>'
```

**Examples:**

```bash
# Basic availability search
python3 sabre_agent/tools/sabre_api.py '115JUNNYCLAX'

# With specific airline
python3 sabre_agent/tools/sabre_api.py '115JUNNYCLAX¥AA'

# Direct flights only
python3 sabre_agent/tools/sabre_api.py '115JUNNYCLAX¤AA'

# Business class
python3 sabre_agent/tools/sabre_api.py '115JUNNYCLAX-J'

# JSON output
python3 sabre_agent/tools/sabre_api.py '115JUNNYCLAX' --json
```

### Using the Agent with Claude Code

When using Claude Code, invoke this agent by referencing the agent prompt:

```
I need to search for flights from New York to London on December 15th.
Please use the Sabre flight search agent located at /home/user/Tutorial/sabre_agent/
```

The agent will:
1. Read the agent_prompt.md for instructions
2. Create a search plan
3. Execute Sabre commands using the API tool
4. Analyze results and present options
5. Suggest alternatives if needed

### Example Interaction

**User Request:**
```
Find flights from San Francisco to Tokyo on June 20th,
direct flights preferred, business class, morning departure
```

**Agent Process:**

1. **Plan Creation:**
   ```
   SEARCH PLAN:
   1. Search direct morning business class flights: 120JUNSFOTYO0800-J¤
   2. If limited, broaden to all-day direct business: 120JUNSFOTYO-J¤
   3. If needed, include connecting flights: 120JUNSFOTYO-J
   4. Compare airlines and present best options
   ```

2. **Command Execution:**
   ```bash
   python3 sabre_agent/tools/sabre_api.py '120JUNSFOTYO0800-J¤' --json
   ```

3. **Result Analysis & Presentation:**
   ```
   FLIGHT OPTIONS FOUND:

   Option 1: United Airlines UA837
   - Departure: 09:30 from SFO
   - Arrival: 14:30+1 at NRT
   - Duration: 11h 00m
   - Aircraft: Boeing 777-300ER
   - Class: Business (J) - 4 seats available

   Option 2: ANA NH7
   - Departure: 10:55 from SFO
   - Arrival: 15:10+1 at HND
   - Duration: 10h 15m
   - Aircraft: Boeing 787-9
   - Class: Business (J) - 7 seats available

   RECOMMENDATION: Option 2 (ANA NH7)
   - Shorter flight time
   - More seat availability
   - Arrives at Haneda (closer to Tokyo city center)
   ```

## Command Reference

### Basic Search Format
```
1[DD][MMM][ORIGIN][DEST]
```

### Modifiers

| Modifier | Symbol | Example | Description |
|----------|--------|---------|-------------|
| Specific Airline | `¥` | `115JUNNYCLAX¥AA` | American Airlines only |
| Direct Flights | `¤` | `115JUNNYCLAX¤` | Non-stop flights |
| Connections | `‡` | `115JUNNYCLAX‡UA` | Include connections |
| Time | `HHMM` or `#A/P` | `115JUNNYCLAX0800` | Around 8 AM |
| Class | `-CLASS` | `115JUNNYCLAX-J` | Business class |

### Common Airport Codes

| Code | Airport | City |
|------|---------|------|
| JFK | John F. Kennedy | New York |
| LAX | Los Angeles Intl | Los Angeles |
| LHR | Heathrow | London |
| CDG | Charles de Gaulle | Paris |
| NRT | Narita | Tokyo |
| DXB | Dubai Intl | Dubai |
| SIN | Changi | Singapore |

### Airline Codes

| Code | Airline |
|------|---------|
| AA | American Airlines |
| UA | United Airlines |
| DL | Delta Air Lines |
| BA | British Airways |
| LH | Lufthansa |
| AF | Air France |
| EK | Emirates |
| QR | Qatar Airways |

For comprehensive command reference, see: [SABRE_RED_360_TICKET_SEARCH_GUIDE.md](../SABRE_RED_360_TICKET_SEARCH_GUIDE.md)

## API Client Details

### SabreAPIClient Class

The `sabre_api.py` module provides a Python client for Sabre SOAP API:

**Key Methods:**

- `create_session()`: Authenticates and creates API session
- `execute_command(command)`: Executes a terminal command
- `close_session()`: Closes the API session

**Response Format:**
```json
{
  "success": true,
  "command": "115JUNNYCLAX",
  "response_text": "...[Sabre terminal response]...",
  "raw_response": "...[Full SOAP XML]..."
}
```

**Error Response:**
```json
{
  "success": false,
  "command": "115JUNNYCLAX",
  "error": "Error description",
  "response_text": null,
  "raw_response": "...[Error details]..."
}
```

## Configuration

### config.json

```json
{
  "api_config": {
    "environment": "cert",  // or "prod"
    "base_url": "https://webservices.cert.platform.sabre.com",
    "credentials": {
      "username": "302596",
      "password": "lon23don",
      "pcc": "U3VL"
    }
  }
}
```

### Environment Variables (Alternative)

You can also set credentials via environment variables:

```bash
export SABRE_USERNAME="302596"
export SABRE_PASSWORD="lon23don"
export SABRE_PCC="U3VL"
export SABRE_ENV="cert"
```

## Troubleshooting

### Common Issues

#### 1. Authentication Failure
```
Error: Could not extract security token from response
```
**Solution:** Verify credentials in `config.json` are correct

#### 2. Invalid Command Format
```
Error: Invalid format
```
**Solution:** Check command syntax against reference guide

#### 3. No Availability
```
Response shows "NO AVAILABILITY" or empty results
```
**Solution:**
- Try different dates (±1-2 days)
- Remove airline restrictions
- Check if route is valid
- Try connecting flights instead of direct

#### 4. API Connection Issues
```
Error: HTTP 403/500 or connection timeout
```
**Solution:**
- Verify CERT environment is accessible
- Check network connection
- Wait and retry (may be temporary outage)

### Debug Mode

For detailed logging, examine the raw SOAP response:

```bash
python3 sabre_agent/tools/sabre_api.py '115JUNNYCLAX' --json | jq '.raw_response'
```

## Best Practices

1. **Start Broad, Then Narrow**: Begin with general availability, then add filters
2. **Use Direct Search When Possible**: Reduces API calls and improves performance
3. **Cache Results**: Store frequently searched routes
4. **Handle Errors Gracefully**: Always have fallback search strategies
5. **Session Management**: Close sessions after use to free resources
6. **Test in CERT First**: Always test in CERT environment before production

## Limitations

- **CERT Environment**: Test data only, not real availability
- **Rate Limits**: Sabre API has rate limiting (exact limits vary by contract)
- **Session Timeout**: Sessions expire after period of inactivity
- **Command Support**: Not all terminal commands supported via SabreCommandLLSRQ
- **Real-time Data**: CERT data may not reflect real-world scenarios

## Advanced Usage

### Custom Search Strategies

Modify `agent_prompt.md` to implement custom search logic:

```markdown
## Custom Strategy: Lowest Fare Finder

1. Search all airlines for the route
2. For each airline with availability:
   - Check all booking classes (Y, B, M, H, Q, K, L)
   - Note lowest available class
3. Compare and rank by typical pricing hierarchy
4. Present lowest fare options
```

### Integration with Booking Systems

The agent can be extended to:
- Create PNRs (Passenger Name Records)
- Add passenger details
- Issue tickets
- Manage bookings

Refer to Sabre API documentation for additional services.

## Resources

- **Sabre Dev Studio**: https://developer.sabre.com/
- **SOAP API Docs**: https://developer.sabre.com/docs/soap_apis
- **Command Guide**: [SABRE_RED_360_TICKET_SEARCH_GUIDE.md](../SABRE_RED_360_TICKET_SEARCH_GUIDE.md)
- **Format Finder**: Available in Sabre Red 360 Workspace

## Support

For issues related to:
- **Agent Logic**: Modify `agent_prompt.md`
- **API Client**: Check `tools/sabre_api.py`
- **Sabre API**: Consult Sabre Dev Studio or support
- **Claude Code**: Refer to Claude Code documentation

## License

This agent is provided as-is for educational and development purposes. Sabre API usage is subject to Sabre's terms of service and requires valid credentials.

## Version History

- **v1.0.0** (2025-11-05): Initial release
  - Sabre SOAP API integration
  - Flight search capabilities
  - Adaptive planning system
  - CERT environment support

## Contributing

To enhance this agent:

1. **Add New Commands**: Extend `agent_prompt.md` with new command patterns
2. **Improve API Client**: Add error handling or new methods to `sabre_api.py`
3. **Create Examples**: Add real-world scenarios to `examples/`
4. **Optimize Searches**: Develop new search strategies in the agent prompt

---

**Ready to search for flights!** 🛫

For questions or improvements, please refer to the documentation or create an issue in your project repository.
