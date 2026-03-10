---
description: Airline Provider Integration - Quick Start Prompt
---

# Airline Provider Integration - Quick Start Prompt

Use this prompt when asking an AI assistant to integrate a new airline provider.

---

## PROMPT TEMPLATE

```
I need you to integrate a new airline provider called [PROVIDER_NAME] into my Fareos flight booking system.

## CONSTRAINTS
1. Backend ONLY - NO frontend changes allowed (frontend is live in production)
2. Must match EXACT API response formats expected by the frontend
3. Must implement complete booking flow (search → book → ticket confirmation)
4. Service must run on port [PORT] via Docker

## PROVIDER DETAILS
- Base URL: [PROVIDER_BASE_URL]
- Authentication: [Bearer Token / API Key / OAuth]
- Credentials: [API_KEY / REFRESH_TOKEN]

## PROVIDER API ENDPOINTS
[Paste provider's API documentation or endpoint list here]

## REQUIRED OUTPUT ENDPOINTS (must match exactly)
- POST /api/v1/search - Flight search
- GET /api/v1/search/:sessionId - Poll search results  
- POST /api/v1/review - Price validation
- POST /api/v1/book - Create booking + purchase + confirm ticket
- GET /api/v1/booking/:id - Get booking details with PNR
- POST /api/v1/seatmap - Get seat map
- POST /api/v1/ssr - Get SSR (meals, baggage)
- POST /api/v1/farerule - Get fare rules
- POST /api/v1/cancel - Cancel booking
- GET /health - Health check

## FRONTEND EXPECTED RESPONSE FORMATS

### Search Response
{
  "flights": [{
    "ids": ["sessionId:::segmentId"],
    "totalPriceList": [{ "PriceId": "sessionId:::segmentId", "FareDetail": {...} }],
    "SegmentInformation": [...],
    "provider": "PROVIDER_NAME"
  }],
  "isComplete": true,
  "sessionId": "uuid"
}

### Book Response  
{
  "status": { "success": true, "message": "Ticket booked!" },
  "bookingId": "uuid",
  "pnr": "PNR123456"
}

### Booking Details Response
{
  "bookingId": "uuid",
  "pnr": "PNR123456",
  "airlinePnr": "ABC123",
  "passengers": [...],
  "itinerary": [...],
  "status": { "success": true }
}

## REFERENCE IMPLEMENTATIONS
Use these as reference for patterns:

**TripJack (`/tjk/`)** - Recommended for complex providers
- Internal orchestration layer (`/internal/`)
- Redis SSR caching
- Pre-booking review for fresh pricing
- Bidirectional transformers (ToAirline*, FromAirline*)

**AerTicket (`/aer/`)** - Simpler direct handler pattern  
- Session-based booking flow
- Complete workflow in Book handler (create → purchase → poll)
- Inline transformation

Key files to study:
- `/tjk/internal/booking.go` - Orchestration with review/SSR enrichment
- `/tjk/transformers/booking_transformer.go` - Bidirectional transforms
- `/aer/handlers/api/v1/flight_handler.go` - Complete booking flow
- `/aer/transformers/booking_transformer.go` - Response transformation

Also review the full workflow: `/.agent/workflows/airline-provider-integration.md`
```

---

## EXAMPLE USAGE

```
I need you to integrate a new airline provider called "SkyConnect" into my Fareos flight booking system.

## CONSTRAINTS
1. Backend ONLY - NO frontend changes allowed
2. Must match EXACT API response formats expected by the frontend
3. Must implement complete booking flow
4. Service must run on port 8088 via Docker

## PROVIDER DETAILS
- Base URL: https://api.skyconnect.com/v2
- Authentication: Bearer Token (OAuth2)
- Credentials: Refresh token in env: SKYCONNECT_REFRESH_TOKEN

## PROVIDER API ENDPOINTS
- POST /flights/search - Search flights
- POST /flights/pricing - Get pricing
- POST /flights/book - Create booking
- POST /flights/pay - Process payment
- GET /flights/status/{id} - Get booking status
- GET /flights/ticket/{id} - Get ticket details

[Continue with the template above...]
```

---

## QUICK VALIDATION CHECKLIST

After integration, verify:

- [ ] `curl localhost:PORT/health` returns healthy
- [ ] Search returns flights with correct `PriceId` format
- [ ] Review returns `bookingId` and `isValid`
- [ ] Book returns `success: true` and `pnr`
- [ ] GetBooking returns full passenger and itinerary details
- [ ] Errors return `success: false` with message

---

**Tip**: Always test the complete flow:
1. Search for flights
2. Select a flight and call review
3. Book with passenger details
4. Fetch booking to verify ticket is confirmed
