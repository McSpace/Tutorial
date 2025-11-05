# Quick Start Guide

Get started with the Sabre Flight Search Agent in 5 minutes!

## 1. Install Dependencies

```bash
cd /home/user/Tutorial/sabre_agent
pip install -r requirements.txt
```

## 2. Test the Setup

```bash
./test_agent.sh
```

Expected output: `✓ All tests passed!`

## 3. Try Your First Search

```bash
python3 tools/sabre_api.py '115JUNNYCLAX'
```

This searches for flights from New York to Los Angeles on June 15th.

## 4. Use with JSON Output

```bash
python3 tools/sabre_api.py '115JUNNYCLAX' --json | python3 -m json.tool
```

## 5. Common Commands

```bash
# Basic search: June 15, NYC to LAX
python3 tools/sabre_api.py '115JUNNYCLAX'

# Specific airline (American Airlines)
python3 tools/sabre_api.py '115JUNNYCLAX¥AA'

# Business class
python3 tools/sabre_api.py '115JUNNYCLAX-J'

# Direct flights only
python3 tools/sabre_api.py '115JUNNYCLAX¤'

# Morning departure (around 8 AM)
python3 tools/sabre_api.py '115JUNNYCLAX0800'

# Combined: AA, morning, business, direct
python3 tools/sabre_api.py '115JUNNYCLAX0800¥AA-J¤'
```

## 6. Use as Claude Code Subagent

In Claude Code, say:

```
Use the Sabre flight search agent at /home/user/Tutorial/sabre_agent/
to find business class flights from London to New York on December 10th,
prefer morning departures.
```

The agent will:
- Read `agent_prompt.md` for instructions
- Create a search plan
- Execute Sabre commands
- Present results with recommendations

## Understanding Command Format

```
1  15  JUN  NYC  LAX  ¥  AA  -  J  ¤
│   │   │    │    │   │   │  │  │  │
│   │   │    │    │   │   │  │  │  └─ Direct flights only
│   │   │    │    │   │   │  │  └──── Class (J=Business)
│   │   │    │    │   │   │  └─────── Class separator
│   │   │    │    │   │   └────────── Airline code
│   │   │    │    │   └────────────── Airline separator
│   │   │    │    └────────────────── Destination
│   │   │    └─────────────────────── Origin
│   │   └──────────────────────────── Month
│   └──────────────────────────────── Day (01-31)
└──────────────────────────────────── Availability command
```

## Common Symbols

- `¥` - Airline qualifier
- `¤` - Direct flights
- `‡` - Including connections
- `-` - Class separator

## Month Codes

| Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| JAN | FEB | MAR | APR | MAY | JUN | JUL | AUG | SEP | OCT | NOV | DEC |

## Class Codes

- `F` - First Class
- `J` - Business Class
- `Y` - Economy Class

## Popular Routes to Try

```bash
# Domestic US
python3 tools/sabre_api.py '101JUNJFKLAX'  # NYC to LA
python3 tools/sabre_api.py '115AUGSFOMIA'  # SF to Miami
python3 tools/sabre_api.py '120SEPORDLAS'  # Chicago to Vegas

# Transatlantic
python3 tools/sabre_api.py '110DECLHRJFK'  # London to NYC
python3 tools/sabre_api.py '115JUNCDGJFK'  # Paris to NYC
python3 tools/sabre_api.py '120SEPJFKFCO'  # NYC to Rome

# Transpacific
python3 tools/sabre_api.py '101JULLAXNRT'  # LA to Tokyo
python3 tools/sabre_api.py '115AUGSFOSYD'  # SF to Sydney
python3 tools/sabre_api.py '120SEPSEAHKG'  # Seattle to Hong Kong
```

## Troubleshooting

### "Invalid format" error
- Check date format is DDMMM (e.g., 01JUN, not 1JUN)
- Verify airport codes are 3 letters

### "No availability"
- Try different dates
- Remove airline restrictions
- Check if route exists

### API connection issues
- Verify internet connection
- Check CERT environment status
- Review credentials in config.json

## Next Steps

1. **Read Full Documentation:** [README.md](README.md)
2. **See More Examples:** [examples/search_examples.md](examples/search_examples.md)
3. **Integration Guide:** [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
4. **Command Reference:** [../SABRE_RED_360_TICKET_SEARCH_GUIDE.md](../SABRE_RED_360_TICKET_SEARCH_GUIDE.md)

## Need Help?

- Run `./test_agent.sh` to verify setup
- Check `README.md` for detailed documentation
- Review `examples/search_examples.md` for usage patterns

---

**Happy searching!** 🛫
