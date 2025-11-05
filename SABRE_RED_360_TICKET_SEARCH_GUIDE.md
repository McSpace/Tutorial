# Sabre Red 360 Ticket Search Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Basic Availability Commands](#basic-availability-commands)
3. [Advanced Search Modifiers](#advanced-search-modifiers)
4. [Selling Flight Segments](#selling-flight-segments)
5. [Creating a Passenger Name Record (PNR)](#creating-a-passenger-name-record-pnr)
6. [Managing Reservations](#managing-reservations)
7. [Quick Reference Commands](#quick-reference-commands)

---

## Introduction

Sabre Red 360 is a Global Distribution System (GDS) used by travel professionals to search, book, and manage travel reservations. This guide focuses on the essential commands for searching and booking flight tickets.

### Command Line Basics
- All commands are entered in the Sabre command line
- Commands are case-sensitive
- Press **Enter** to execute a command
- Use the **Format Finder** tool within Sabre for additional help

---

## Basic Availability Commands

### Standard Availability Search

**Format:**
```
1[DD][MMM][ORIGIN][DESTINATION]
```

**Components:**
- `1` = Availability command
- `DD` = Day of the month (01-31)
- `MMM` = Month abbreviation (JAN, FEB, MAR, etc.)
- `ORIGIN` = 3-letter airport/city code
- `DESTINATION` = 3-letter airport/city code

**Examples:**
```
101JUNNYCLAX       Search flights from New York to Los Angeles on June 1st
125DECLONJFK       Search flights from London to JFK on December 25th
115SEPDFWMIA       Search flights from Dallas to Miami on September 15th
```

### Response Interpretation
After entering an availability command, Sabre displays:
- Flight numbers
- Departure/arrival times
- Number of stops
- Available booking classes
- Number of seats available in each class

---

## Advanced Search Modifiers

### Direct Flights Only
**Format:**
```
1[DD][MMM][ORIGIN][DESTINATION]¤[AIRLINE]
```

**Symbol:** `¤` (Direct availability)

**Example:**
```
101JUNNYCDFW¤AA    Direct flights only from NYC to DFW on June 1st with American Airlines
```

### Indirect/Connecting Flights
**Format:**
```
1[DD][MMM][ORIGIN][DESTINATION]‡[AIRLINE]
```

**Symbol:** `‡` (Indirect availability)

**Example:**
```
101JUNNYCDFW‡UA    Connecting flights from NYC to DFW with United Airlines
```

### Specific Airline Search
**Format:**
```
1[DD][MMM][ORIGIN][DESTINATION]¥[AIRLINE CODE]
```

**Symbol:** `¥` (Airline qualifier)

**Examples:**
```
101JUNLAXSFO¥AA    American Airlines flights only
120JUNDACSIN¥BG    Biman Bangladesh Airlines flights only
```

### Search by Departure Time
**Format:**
```
1[DD][MMM][ORIGIN][DESTINATION][TIME]
```

**Time Format:**
- Use 24-hour format or specify AM/PM
- A = Morning, P = Afternoon/Evening

**Examples:**
```
101JUNNYCDFW0800   Flights departing around 8:00 AM
130JUNBAHPAR2P     Flights departing around 2:00 PM
```

### Search by Booking Class
**Format:**
```
1[DD][MMM][ORIGIN][DESTINATION]-[CLASS]
```

**Common Booking Classes:**
- `Y` = Economy
- `J` = Business
- `F` = First Class

**Example:**
```
101JUNNYCDFW-J     Business class availability
101JUNLAXLHR-F     First class availability
```

### Combined Modifiers
You can combine multiple modifiers:

**Examples:**
```
101JUNNYCDFW¥AA-Y           American Airlines, Economy class
101JUNLAXLHR0900¥BA-J       British Airways, 9 AM departure, Business class
125OCTSHJELQ¤                Direct flights only (any airline)
```

---

## Selling Flight Segments

Once you've found the desired flight, you need to "sell" (book) the segment.

### Sell from Availability Display

**Format:**
```
0[LINE NUMBER]
```

**Example:**
```
01        Sell the flight on line 1
02        Sell the flight on line 2
```

### Long Sell (Without Prior Availability)
If you know the flight details, you can sell directly:

**Format:**
```
0[AIRLINE][FLIGHT NUMBER][CLASS][DD][MMM][ORIGIN][DESTINATION]NN[NUMBER OF SEATS]
```

**Components:**
- `0` = Sell command
- `NN` = Need (requesting seats)

**Example:**
```
0EK786Y01DECKHIJED-NN1     Sell 1 seat in Y class on Emirates 786 from Karachi to Jeddah
0AA100J15JUNNYCDFW-NN2     Sell 2 seats in J class on American 100 from NYC to DFW
```

### Verify Segment Status
After selling, verify the segment is confirmed:
- `HK` = Holding Confirmed
- `NN` = Need/Requested
- `UC` = Unable to Confirm

---

## Creating a Passenger Name Record (PNR)

A PNR contains all booking information. Follow these steps in order:

### 1. Add Passenger Name(s)

**Format:**
```
-[LAST NAME]/[FIRST NAME] [TITLE]
```

**Titles:**
- `MR` = Male adult
- `MS` or `MRS` = Female adult
- `MSTR` = Male child
- `MISS` = Female child

**Examples:**
```
-SMITH/JOHN MR                        One adult passenger
-JOHNSON/MARY MS                      Female passenger
-WILLIAMS/ROBERT MR*WILLIAMS/SUSAN MRS    Two passengers (use * to separate)
-BROWN/EMILY MISS                     Child passenger
```

### 2. Add Phone Contact

**Format:**
```
9[AREA CODE][PHONE NUMBER]-[TYPE]
```

**Contact Types:**
- `A` = Agency phone
- `H` = Home phone
- `B` = Business phone
- `M` = Mobile phone

**Examples:**
```
9212555-1234-A        Agency phone
9305555-6789-H        Home phone
9415555-0000-M        Mobile phone
```

**Note:** Always add the agency phone number first if multiple contacts are included.

### 3. Add Ticketing Time Limit

**Format:**
```
TKTL[DD][MMM]
```

**Example:**
```
TKTL15JUN         Ticket by June 15th
TKTL01DEC         Ticket by December 1st
```

### 4. Add Received From Field

**Format:**
```
6[NAME OR INITIALS]
```

**Example:**
```
6JOHN             Received from John
6JS               Received from initials JS
```

### 5. End Transaction

**Format:**
```
E         End and save the PNR
ER        End and redisplay the PNR
ET        End and price the itinerary
```

**Example Workflow:**
```
1. Enter availability: 101JUNNYCDFW¥AA
2. Sell segment: 01
3. Add passenger: -SMITH/JOHN MR
4. Add phone: 9212555-1234-A
5. Add ticketing: TKTL05JUN
6. Received from: 6JOHNSMITH
7. End transaction: ER
```

---

## Managing Reservations

### Retrieve a PNR

**By Record Locator:**
```
*[RECORD LOCATOR]
```
**Example:**
```
*ABC123        Retrieve PNR with locator ABC123
```

**By Passenger Name:**
```
*-[LAST NAME]
```
**Example:**
```
*-SMITH        Retrieve PNRs for passenger Smith
```

**By Flight Number and Date:**
```
*[AIRLINE][FLIGHT NUMBER]/[DD][MMM]
```
**Example:**
```
*AA100/15JUN   Retrieve PNRs on American 100 on June 15th
```

### Display PNR Information

```
*R        Redisplay current PNR
*P        Display PNR pricing
*T        Display ticketing information
```

### Modify a PNR

**Change passenger name:**
```
-[LAST NAME]/[FIRST NAME]@[NEW LAST NAME]/[NEW FIRST NAME]
```

**Cancel a segment:**
```
X[LINE NUMBER]
```
**Example:**
```
X1        Cancel segment on line 1
```

**Add remarks:**
```
5[REMARK TEXT]
```
**Example:**
```
5WHEELCHAIR ASSISTANCE REQUIRED
5FREQUENT FLYER AA1234567
```

### Important Transaction Commands

```
E         End and save changes
ER        End and redisplay
I         Ignore changes (do not save)
IR        Ignore changes and redisplay original PNR
```

---

## Quick Reference Commands

### Essential Commands

| Command | Description |
|---------|-------------|
| `1DDMMMORIGDEST` | Check flight availability |
| `0[LINE]` | Sell segment from availability |
| `-NAME/FIRST TITLE` | Add passenger name |
| `9PHONE-TYPE` | Add phone number |
| `TKTLDDMMM` | Add ticketing deadline |
| `6NAME` | Add received from |
| `E` | End transaction (save) |
| `ER` | End and redisplay |
| `*LOCATOR` | Retrieve PNR by record locator |
| `*-NAME` | Retrieve PNR by passenger name |
| `*R` | Redisplay current PNR |
| `I` | Ignore changes |
| `IR` | Ignore and retrieve |
| `X[LINE]` | Cancel segment |
| `5REMARK` | Add remark |
| `*T` | Display ticket information |
| `*P` | Display pricing |

### Availability Modifiers

| Modifier | Symbol | Description |
|----------|--------|-------------|
| Direct flights | `¤` | Direct/non-stop only |
| Indirect flights | `‡` | Including connections |
| Specific airline | `¥` | Filter by airline code |
| Specific class | `-CLASS` | Filter by booking class |
| Time | `HHMM` or `#P/A` | Specific departure time |

### Booking Classes

| Code | Description |
|------|-------------|
| `F` | First Class |
| `J` | Business Class |
| `Y` | Full-fare Economy |
| `B/M/H` | Discount Economy |
| `Q/K/L` | Deep Discount Economy |

### Month Abbreviations

| Code | Month | Code | Month |
|------|-------|------|-------|
| `JAN` | January | `JUL` | July |
| `FEB` | February | `AUG` | August |
| `MAR` | March | `SEP` | September |
| `APR` | April | `OCT` | October |
| `MAY` | May | `NOV` | November |
| `JUN` | June | `DEC` | December |

---

## Tips and Best Practices

1. **Always verify segment status** after selling to ensure confirmation (HK status)
2. **Check ticketing time limits** to avoid automatic cancellations
3. **Add agency contact first** when entering multiple phone numbers
4. **Use IR command** to discard unwanted changes and start over
5. **Save frequently** using ER command to avoid losing work
6. **Review PNR carefully** before issuing tickets
7. **Use Format Finder** within Sabre Red 360 for command help
8. **Practice in training mode** before working with live bookings

---

## Additional Resources

- **Sabre Central:** http://central.sabre.com/ - Official documentation and training
- **Format Finder:** Built-in tool within Sabre Red 360 workspace
- **Help Command:** Type `HELP` in command line for context-sensitive assistance
- **Sabre Dev Studio:** https://developer.sabre.com/ - API documentation and resources

---

## Troubleshooting Common Issues

### "INVALID FORMAT" Error
- Check command syntax carefully
- Verify date format (DDMMM)
- Ensure airport codes are valid 3-letter codes

### "NO AVAILABILITY" Message
- Try different dates or times
- Remove restrictive modifiers
- Check if route is valid

### "UNABLE TO COMPLETE" Error
- Flight may be full or unavailable
- Try alternative flights or airlines

### PNR Not Saving
- Ensure all mandatory fields are complete (name, phone, ticketing, received from)
- Check for error messages before ending transaction

---

**Document Version:** 1.0
**Last Updated:** November 2025
**Compiled from:** Official Sabre training materials and command references

---

*Note: This guide covers fundamental ticket searching and booking commands in Sabre Red 360. For advanced features, complex itineraries, or specific airline requirements, consult official Sabre documentation or contact Sabre support.*
