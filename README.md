# Sabre Red 360 Flight Search System

Complete solution for searching flight tickets using Sabre Red 360 commands and API.

## 🎯 Overview

This project provides two complementary components:

1. **Command Reference Guide** - Comprehensive documentation of Sabre Red 360 terminal commands
2. **AI Flight Search Agent** - Intelligent subagent that executes searches via Sabre SOAP API

## 📚 Components

### 1. Sabre Red 360 Command Guide

**File:** `SABRE_RED_360_TICKET_SEARCH_GUIDE.md`

Comprehensive instruction manual covering:
- Basic and advanced availability commands
- Search modifiers (airlines, classes, times, direct/indirect flights)
- Flight segment selling procedures
- PNR (Passenger Name Record) creation workflow
- Reservation management and retrieval
- Quick reference tables and troubleshooting

**Perfect for:**
- Travel agents learning Sabre Red 360
- Quick command reference
- Understanding GDS search syntax

### 2. Flight Search Agent

**Directory:** `sabre_agent/`

Intelligent AI agent specialized in flight searches:
- Plans multi-step search strategies
- Executes Sabre commands via SOAP API
- Interprets and analyzes results
- Adapts search approach based on findings
- Presents clear, actionable recommendations

**Perfect for:**
- Automated flight searches
- Integration with booking systems
- Claude Code subagent deployment
- API-based GDS access

## 🚀 Quick Start

### Using the Command Guide

Simply open and read:
```bash
cat SABRE_RED_360_TICKET_SEARCH_GUIDE.md
```

### Using the Flight Search Agent

**1. Install Dependencies:**
```bash
cd sabre_agent
pip install -r requirements.txt
```

**2. Test Setup:**
```bash
./test_agent.sh
```

**3. Search for Flights:**
```bash
python3 tools/sabre_api.py '115JUNNYCLAX'
```

**4. Use with Claude Code:**
```
Use the Sabre flight search agent at /home/user/Tutorial/sabre_agent/
to find flights from New York to London on June 15th.
```

## 📖 Documentation

| Document | Description |
|----------|-------------|
| `SABRE_RED_360_TICKET_SEARCH_GUIDE.md` | Complete command reference guide |
| `sabre_agent/README.md` | Agent overview and architecture |
| `sabre_agent/QUICK_START.md` | 5-minute getting started guide |
| `sabre_agent/INTEGRATION_GUIDE.md` | Claude Code integration instructions |
| `sabre_agent/examples/search_examples.md` | Real-world usage examples |

## 🎓 Learning Path

### For Beginners
1. Read `SABRE_RED_360_TICKET_SEARCH_GUIDE.md`
2. Try `sabre_agent/QUICK_START.md`
3. Experiment with basic commands
4. Review `examples/search_examples.md`

### For Integration
1. Read `sabre_agent/README.md`
2. Follow `sabre_agent/INTEGRATION_GUIDE.md`
3. Test with `./test_agent.sh`
4. Integrate with your workflow

## 🔧 Architecture

```
Tutorial/
├── SABRE_RED_360_TICKET_SEARCH_GUIDE.md  # Command reference
├── README.md                              # This file
└── sabre_agent/                           # AI Agent
    ├── tools/
    │   └── sabre_api.py                   # SOAP API client
    ├── agent_prompt.md                    # Agent instructions
    ├── config.json                        # Configuration
    ├── requirements.txt                   # Python dependencies
    ├── test_agent.sh                      # Test suite
    ├── README.md                          # Agent documentation
    ├── QUICK_START.md                     # Quick start guide
    ├── INTEGRATION_GUIDE.md               # Integration instructions
    └── examples/
        └── search_examples.md             # Usage examples
```

## 🌟 Features

### Command Guide Features
✅ Complete Sabre command syntax reference
✅ Real-world examples for every command type
✅ Quick reference tables
✅ Troubleshooting section
✅ Best practices from industry experts

### Agent Features
✅ Intelligent search planning
✅ Sabre SOAP API integration
✅ Adaptive search strategies
✅ Result interpretation and analysis
✅ Error handling and alternatives
✅ Claude Code integration
✅ JSON output support

## 🎯 Common Use Cases

### Manual Terminal Use
Use the **Command Guide** to learn Sabre syntax and work directly in Red 360 terminal:
```
1. Open Sabre Red 360
2. Refer to SABRE_RED_360_TICKET_SEARCH_GUIDE.md
3. Type commands directly
4. Create PNR and book flights
```

### Automated API Searches
Use the **Flight Search Agent** for programmatic access:
```bash
# Single command
python3 sabre_agent/tools/sabre_api.py '115JUNNYCLAX' --json

# Or let the agent plan and execute
# (via Claude Code or custom integration)
```

### Learning and Training
Use **both** components together:
1. Read command guide to understand syntax
2. Use agent to see commands in action
3. Experiment with different searches
4. Build your Sabre expertise

## 🔐 API Credentials

The agent is pre-configured with **CERT (test) environment** credentials:

- **Environment:** CERT (https://webservices.cert.platform.sabre.com)
- **Username:** 302596
- **Password:** lon23don
- **PCC:** U3VL

> ⚠️ **Note:** These are test credentials. For production use, obtain your own credentials from Sabre and update `sabre_agent/config.json`.

## 📝 Example Commands

### Basic Availability
```bash
115JUNNYCLAX      # NYC to LAX, June 15
120DECLHRJFK      # London to NYC, December 20
101JULSFOTYO      # SF to Tokyo, July 1
```

### With Modifiers
```bash
115JUNNYCLAX¥AA        # American Airlines only
115JUNNYCLAX-J         # Business class
115JUNNYCLAX¤          # Direct flights
115JUNNYCLAX0800       # Morning (8 AM) departure
115JUNNYCLAX0800¥AA-J¤ # Combined: AA, 8AM, Business, Direct
```

### Using the API
```bash
# Basic search
python3 sabre_agent/tools/sabre_api.py '115JUNNYCLAX'

# JSON output
python3 sabre_agent/tools/sabre_api.py '115JUNNYCLAX' --json

# With filters
python3 sabre_agent/tools/sabre_api.py '115JUNNYCLAX¥AA-J' --json
```

## 🛠️ Troubleshooting

### Command Guide Issues
- **Q:** What does "Invalid Format" mean?
- **A:** Check command syntax in the guide, verify date format (DDMMM)

### Agent Issues
- **Q:** API returns "Authentication failed"
- **A:** Verify credentials in `sabre_agent/config.json`

- **Q:** "No availability" for every search
- **A:** Check date format, verify route exists, try removing filters

- **Q:** Python packages missing
- **A:** Run `pip install -r sabre_agent/requirements.txt`

### Test the Setup
```bash
cd sabre_agent
./test_agent.sh
```

## 🔗 Resources

### Sabre Documentation
- **Sabre Dev Studio:** https://developer.sabre.com/
- **SOAP APIs:** https://developer.sabre.com/docs/soap_apis
- **Format Finder:** Available in Sabre Red 360 workspace

### Project Documentation
- **Command Reference:** `SABRE_RED_360_TICKET_SEARCH_GUIDE.md`
- **Agent README:** `sabre_agent/README.md`
- **Quick Start:** `sabre_agent/QUICK_START.md`
- **Examples:** `sabre_agent/examples/search_examples.md`

## 🤝 Integration Examples

### With Claude Code
```python
# Natural language request
"Use the Sabre agent to find business class flights from
London to Singapore on August 20th"

# Claude Code will:
# 1. Load agent prompt
# 2. Plan search strategy
# 3. Execute Sabre commands
# 4. Present results
```

### With Python
```python
from sabre_agent.tools.sabre_api import SabreAPIClient

client = SabreAPIClient("302596", "lon23don", "U3VL", "cert")
result = client.execute_command("115JUNNYCLAX")

if result['success']:
    print(result['response_text'])

client.close_session()
```

### Command Line
```bash
# Pipe to JSON processor
python3 sabre_agent/tools/sabre_api.py '115JUNNYCLAX' --json | jq '.response_text'

# Save to file
python3 sabre_agent/tools/sabre_api.py '115JUNNYCLAX' > results.txt
```

## 📊 Supported Search Types

| Search Type | Command Guide | Agent Support | Example |
|-------------|---------------|---------------|---------|
| Basic Availability | ✅ | ✅ | `115JUNNYCLAX` |
| Airline Specific | ✅ | ✅ | `115JUNNYCLAX¥AA` |
| Direct Flights | ✅ | ✅ | `115JUNNYCLAX¤` |
| By Class | ✅ | ✅ | `115JUNNYCLAX-J` |
| By Time | ✅ | ✅ | `115JUNNYCLAX0800` |
| Complex Queries | ✅ | ✅ | `115JUNNYCLAX0800¥AA-J¤` |
| Multi-leg | ✅ | ✅ | Sequential searches |
| Flexible Dates | ✅ | ✅ | Agent adapts automatically |

## 🎓 Best Practices

### Command Guide Usage
1. Start with basic commands
2. Add modifiers incrementally
3. Use quick reference tables
4. Refer to troubleshooting section

### Agent Usage
1. Be specific in search requests
2. Let agent create search plan
3. Trust adaptive strategies
4. Review and refine results

### General Tips
1. Test in CERT before production
2. Verify airport codes are valid
3. Use proper date format (DDMMM)
4. Consider time zones for international flights
5. Check multiple options before booking

## 📜 License

This project is provided for educational and development purposes. Sabre API usage is subject to Sabre's terms of service.

## 🔄 Version History

### v1.0.0 (2025-11-05)
- ✅ Complete Sabre Red 360 command reference guide
- ✅ AI-powered flight search agent
- ✅ SOAP API integration
- ✅ Claude Code subagent support
- ✅ Comprehensive documentation
- ✅ Example library
- ✅ Test suite

## 🚦 Getting Started Checklist

- [ ] Read `SABRE_RED_360_TICKET_SEARCH_GUIDE.md`
- [ ] Install Python dependencies
- [ ] Run `sabre_agent/test_agent.sh`
- [ ] Try a basic search command
- [ ] Review example searches
- [ ] Test Claude Code integration (if using)
- [ ] Customize agent prompt (optional)
- [ ] Update credentials for production (if needed)

## 💡 Tips for Success

1. **Start Simple:** Begin with basic availability commands
2. **Use Documentation:** Reference the guide frequently
3. **Test Thoroughly:** Always test in CERT environment first
4. **Learn Patterns:** Notice how similar routes/searches work
5. **Leverage Agent:** Let the AI handle complex searches
6. **Provide Feedback:** The agent adapts based on results

## 📞 Support

For issues with:
- **Command Syntax:** Refer to `SABRE_RED_360_TICKET_SEARCH_GUIDE.md`
- **Agent Logic:** Check `sabre_agent/agent_prompt.md`
- **API Issues:** Review `sabre_agent/README.md` troubleshooting
- **Sabre Platform:** Contact Sabre support or check Dev Studio

---

**Ready to search for flights!** 🛫

Start with the Quick Start guide or dive into the comprehensive documentation.
