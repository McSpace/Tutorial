# Sabre Flight Search Examples

This document provides real-world examples of using the Sabre Flight Search Agent.

## Example 1: Simple Domestic Search

**User Request:**
```
Find flights from New York (JFK) to Los Angeles (LAX) on June 15th
```

**Agent Plan:**
```
SEARCH PLAN:
1. Execute basic availability search
2. If many results, filter by major carriers
3. Present top 5 options with different times
```

**Commands Executed:**
```bash
python3 sabre_agent/tools/sabre_api.py '115JUNJFKLAX' --json
```

**Expected Result:**
- Multiple flight options from various airlines
- Different departure times throughout the day
- Direct flights (LAX-JFK is a major route)

---

## Example 2: International Business Class

**User Request:**
```
Find business class flights from London to New York on December 10th,
prefer morning departures on British Airways or American Airlines
```

**Agent Plan:**
```
SEARCH PLAN:
1. Search BA morning business class: 110DECLHRJFK0800¥BA-J
2. Search AA morning business class: 110DECLHRJFK0800¥AA-J
3. If limited options, expand to all-day: 110DECLHRJFK¥BA-J
4. Compare both airlines and present best options
```

**Commands Executed:**
```bash
# Step 1: British Airways morning business
python3 sabre_agent/tools/sabre_api.py '110DECLHRJFK0800¥BA-J' --json

# Step 2: American Airlines morning business
python3 sabre_agent/tools/sabre_api.py '110DECLHRJFK0800¥AA-J' --json

# Step 3: If needed, all-day search
python3 sabre_agent/tools/sabre_api.py '110DECLHRJFK¥BA-J' --json
```

**Expected Result:**
- Business class availability on transatlantic flights
- Morning departure options
- Comparison between BA and AA offerings

---

## Example 3: Direct Flights Only

**User Request:**
```
Find direct flights from San Francisco to Tokyo on July 1st,
any airline, economy class
```

**Agent Plan:**
```
SEARCH PLAN:
1. Search direct flights only in economy: 101JULSFOTYO-Y¤
2. If no direct flights, inform user and suggest:
   - 1-stop options via common hubs (SEA, LAX, HNL)
   - Alternative airlines
```

**Commands Executed:**
```bash
# Step 1: Direct flights only
python3 sabre_agent/tools/sabre_api.py '101JULSFOTYO-Y¤' --json

# If no results, try without direct-only modifier
python3 sabre_agent/tools/sabre_api.py '101JULSFOTYO-Y' --json
```

**Expected Result:**
- Direct SFO-TYO flights (likely on UA, ANA, JAL)
- Economy class availability
- If no direct: 1-stop options presented

---

## Example 4: Multi-Airline Comparison

**User Request:**
```
Compare flights from Dubai to Singapore on August 20th
for Emirates, Qatar Airways, and Singapore Airlines
```

**Agent Plan:**
```
SEARCH PLAN:
1. Search Emirates: 120AUGDXBSIN¥EK
2. Search Qatar Airways: 120AUGDXBSIN¥QR
3. Search Singapore Airlines: 120AUGDXBSIN¥SQ
4. Compile results and compare:
   - Flight times
   - Available classes
   - Number of stops
```

**Commands Executed:**
```bash
# Emirates
python3 sabre_agent/tools/sabre_api.py '120AUGDXBSIN¥EK' --json

# Qatar Airways
python3 sabre_agent/tools/sabre_api.py '120AUGDXBSIN¥QR' --json

# Singapore Airlines
python3 sabre_agent/tools/sabre_api.py '120AUGDXBSIN¥SQ' --json
```

**Expected Result:**
- Side-by-side comparison of three premium carriers
- Different routing options (EK/QR likely via hubs)
- Class availability across all airlines

---

## Example 5: Flexible Dates Search

**User Request:**
```
Find cheapest flights from Chicago to Paris around September 15th
(flexible ±3 days), economy class
```

**Agent Plan:**
```
SEARCH PLAN:
1. Search target date: 115SEPORDDVA-Y (CDG main Paris airport)
2. Search day before: 114SEPORDCDG-Y
3. Search day after: 116SEPORDCDG-Y
4. Search ±2 days if needed
5. Compare availability and typical pricing indicators
6. Recommend dates with best options
```

**Commands Executed:**
```bash
# September 12-18 search range
python3 sabre_agent/tools/sabre_api.py '112SEPORDCDG-Y' --json
python3 sabre_agent/tools/sabre_api.py '113SEPORDCDG-Y' --json
python3 sabre_agent/tools/sabre_api.py '114SEPORDCDG-Y' --json
python3 sabre_agent/tools/sabre_api.py '115SEPORDCDG-Y' --json
python3 sabre_agent/tools/sabre_api.py '116SEPORDCDG-Y' --json
python3 sabre_agent/tools/sabre_api.py '117SEPORDCDG-Y' --json
python3 sabre_agent/tools/sabre_api.py '118SEPORDCDG-Y' --json
```

**Expected Result:**
- Availability across 7-day window
- Indication of which dates have better options
- Recommendation for best travel dates

---

## Example 6: Afternoon Departure

**User Request:**
```
Find flights from Boston to Miami on October 5th,
departure after 2 PM, any airline
```

**Agent Plan:**
```
SEARCH PLAN:
1. Search afternoon flights: 105OCTBOSMIA2P
2. If limited, search specific afternoon times:
   - 105OCTBOSMIA1400 (2 PM)
   - 105OCTBOSMIA1600 (4 PM)
   - 105OCTBOSMIA1800 (6 PM)
3. Present all afternoon options
```

**Commands Executed:**
```bash
# General afternoon search
python3 sabre_agent/tools/sabre_api.py '105OCTBOSMIA2P' --json

# If needed, specific times
python3 sabre_agent/tools/sabre_api.py '105OCTBOSMIA1400' --json
python3 sabre_agent/tools/sabre_api.py '105OCTBOSMIA1600' --json
```

**Expected Result:**
- Multiple afternoon departure options
- BOS-MIA is a frequent route with many daily flights
- Various airlines (AA, DL, UA, B6, etc.)

---

## Example 7: No Availability - Alternative Strategy

**User Request:**
```
Find flights from Small City Airport (SBN) to International Hub (LHR) on June 1st
```

**Agent Plan:**
```
SEARCH PLAN:
1. Try direct search: 101JUNSBNLHR
2. If no direct flights (expected), search via major hubs:
   - Via Chicago: 101JUNSBNORD + 101JUNORDLHR
   - Via New York: 101JUNSBNJ FK + 101JUNJFKLHR
   - Via Newark: 101JUBNEWR + 101JUNEWRLHR
3. Present best connection options
```

**Commands Executed:**
```bash
# Direct attempt (likely no results)
python3 sabre_agent/tools/sabre_api.py '101JUNSBNLHR' --json

# Via Chicago O'Hare
python3 sabre_agent/tools/sabre_api.py '101JUNSBNORD' --json
python3 sabre_agent/tools/sabre_api.py '101JUNORDLHR' --json

# Via JFK
python3 sabre_agent/tools/sabre_api.py '101JUNSBN JFK' --json
python3 sabre_agent/tools/sabre_api.py '101JUNJFKLHR' --json
```

**Expected Result:**
- No direct flights from small airport to international destination
- Multiple connection options via major hubs
- Coordinated arrival/departure times for connections

---

## Example 8: First Class Availability

**User Request:**
```
Check first class availability from Los Angeles to Sydney on November 25th,
interested in Qantas or United
```

**Agent Plan:**
```
SEARCH PLAN:
1. Search Qantas first class: 125NOVLAXSYD¥QF-F
2. Search United first class: 125NOVLAXSYD¥UA-F
3. If no first class (F), check business class (J) as alternative
4. Note: Not all airlines operate true First on all routes
```

**Commands Executed:**
```bash
# Qantas First
python3 sabre_agent/tools/sabre_api.py '125NOVLAXSYD¥QF-F' --json

# United First/Polaris
python3 sabre_agent/tools/sabre_api.py '125NOVLAXSYD¥UA-F' --json

# Fallback: Business class
python3 sabre_agent/tools/sabre_api.py '125NOVLAXSYD¥QF-J' --json
```

**Expected Result:**
- First class availability (if offered on route)
- May show "F" class even if airline calls it "Business"
- Long-haul route with premium cabin options

---

## Example 9: Nearby Airports

**User Request:**
```
Find flights from Washington DC area to San Francisco on March 10th
```

**Agent Plan:**
```
SEARCH PLAN:
1. Search from Reagan (DCA): 110MARDCASFO
2. Search from Dulles (IAD): 110MARIADSFO
3. Search from BWI: 110MARBWISFO
4. Compare all three airports:
   - Flight options
   - Departure times
   - Airlines serving each airport
5. Recommend best airport option
```

**Commands Executed:**
```bash
# Reagan National
python3 sabre_agent/tools/sabre_api.py '110MARDCASFO' --json

# Dulles International
python3 sabre_agent/tools/sabre_api.py '110MARIADSFO' --json

# Baltimore Washington
python3 sabre_agent/tools/sabre_api.py '110MARBWISFO' --json
```

**Expected Result:**
- Options from all three DC-area airports
- DCA may have limited cross-country flights
- IAD and BWI likely have more options
- Recommendation based on convenience and availability

---

## Example 10: Complex Multi-Step Search

**User Request:**
```
Find the best option for a family trip (2 adults, 2 children) from
Atlanta to Orlando on April 15th, returning April 22nd,
economy class, prefer Delta or Southwest, morning outbound
```

**Agent Plan:**
```
SEARCH PLAN:
Phase 1 - Outbound (April 15):
1. Search Delta morning flights: 115APRATLORL0800¥DL-Y
2. Search Southwest morning flights: 115APRATLORL0800¥WN-Y
3. Verify at least 4 seats available

Phase 2 - Return (April 22):
1. Search Delta return: 122APRORLATL¥DL-Y
2. Search Southwest return: 122APRORLATL¥WN-Y
3. Check afternoon/evening flights (easier with kids)

Phase 3 - Analysis:
1. Match outbound and return options
2. Consider total travel time
3. Verify 4+ seats on both flights
4. Present complete round-trip options
```

**Commands Executed:**
```bash
# Outbound searches
python3 sabre_agent/tools/sabre_api.py '115APRATLORL0800¥DL-Y' --json
python3 sabre_agent/tools/sabre_api.py '115APRATLORL0800¥WN-Y' --json

# Return searches
python3 sabre_agent/tools/sabre_api.py '122APRORLATL¥DL-Y' --json
python3 sabre_agent/tools/sabre_api.py '122APRORLATL¥WN-Y' --json

# Alternative return times if needed
python3 sabre_agent/tools/sabre_api.py '122APRORLATL1400¥DL-Y' --json
```

**Expected Result:**
- Complete round-trip options
- Confirmed availability for 4 passengers
- Morning outbound, flexible return
- Family-friendly flight times

---

## Tips for Effective Searches

### 1. Start Broad
```bash
# Good: Start with basic search
115JUNNYCDFW

# Then narrow down
115JUNNYCDFW¥AA        # Specific airline
115JUNNYCDFW¥AA-J      # Specific airline and class
115JUNNYCDFW0800¥AA-J¤ # All modifiers
```

### 2. Handle "No Availability"
```bash
# If no results:
1. Remove airline restriction
2. Remove class restriction
3. Try ±1 day
4. Check nearby airports
5. Search connecting flights
```

### 3. Time-of-Day Searches
```bash
115JUNNYCDFW0600   # Early morning (around 6 AM)
115JUNNYCDFW1200   # Noon
115JUNNYCDFW1800   # Evening (6 PM)
115JUNNYCDFW1A     # Early morning (general)
115JUNNYCDFW2P     # Afternoon (general)
```

### 4. Multi-City Searches
For complex itineraries, search each leg separately:
```bash
# NYC -> London -> Paris -> NYC
101JUNJFKLHR      # Leg 1
108JUNLHRCDG      # Leg 2
115JUNCDGJFK      # Leg 3
```

### 5. Using Alliance Codes
While Sabre uses individual airline codes, you can search multiple alliance members:
```bash
# Star Alliance examples on same route
115JUNJFKLHR¥UA   # United
115JUNJFKLHR¥LH   # Lufthansa
115JUNJFKLHR¥AC   # Air Canada
```

---

## Common Scenarios Checklist

- [ ] Basic domestic search
- [ ] International long-haul
- [ ] Direct flights only
- [ ] Business/First class
- [ ] Specific airline preference
- [ ] Time of day requirements
- [ ] Flexible dates (±1-3 days)
- [ ] Nearby airports comparison
- [ ] Multi-passenger availability
- [ ] Round-trip planning
- [ ] Connection searches
- [ ] No availability alternatives

---

## Error Scenarios and Resolutions

### Scenario: "Invalid Format"
**Command:** `1JUNNYCDFW` (missing day)
**Fix:** `101JUNNYCDFW` (must have 2-digit day)

### Scenario: "No Availability"
**Command:** `101JUNSMALLTINYTOWN` (invalid city codes)
**Fix:** Verify airport codes, try major nearby airport

### Scenario: API Timeout
**Command:** Any
**Fix:** Wait 30 seconds, retry. If persists, check CERT environment status

### Scenario: Empty Response
**Command:** `101JANNYCDFW` (past date)
**Fix:** Use current or future dates only

---

## Integration Examples

### Use with Claude Code Task Tool
```python
# In your Claude Code session
"""
Please use the Sabre flight search agent to find flights from
Miami to Bogotá on February 14th, economy class, any airline.

Agent location: /home/user/Tutorial/sabre_agent/
"""
```

### Programmatic Usage
```python
from sabre_agent.tools.sabre_api import SabreAPIClient

client = SabreAPIClient("302596", "lon23don", "U3VL", "cert")

# Single search
result = client.execute_command("115JUNMIABOG-Y")

if result['success']:
    print(result['response_text'])

client.close_session()
```

---

**Ready to search!** Use these examples as templates for your own flight searches.
