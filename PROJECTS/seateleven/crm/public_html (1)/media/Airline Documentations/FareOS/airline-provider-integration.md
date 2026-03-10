---
description: Complete airline provider integration workflow - backend only, no frontend changes
---

# Airline Provider Integration - Vibe Prompt Template

## 🎯 OBJECTIVE
Integrate a new airline/flight provider into the Fareos booking system. The integration MUST:
- Work with existing frontend without ANY changes
- Match exact API response formats expected by `sme-front-end`
- Support complete booking flow from search to confirmed ticket
- Handle all error cases gracefully

---

## 📚 REFERENCE IMPLEMENTATIONS

You have TWO working provider implementations to reference:

| Provider | Location | Architecture Style | Key Feature |
|----------|----------|-------------------|-------------|
| **TripJack (TJK)** | `/tjk/` | Internal orchestration layer | Redis caching, SSR enrichment, Pre-booking review |
| **AerTicket (AER)** | `/aer/` | Direct handler pattern | Session-based booking, Purchase + Poll workflow |

### TJK Architecture (Recommended for Complex Providers)
```
Handlers → Internal (Orchestration) → Transformers → Services → Provider API
```

### AER Architecture (Simple/Direct)
```
Handlers → Services → Provider API (with inline transformation)
```

---

## 📋 PRE-INTEGRATION CHECKLIST

Before starting, ensure you have:
1. Provider API documentation (OpenAPI/Swagger or Markdown)
2. Provider credentials (API keys, tokens, base URLs)
3. Sample request/response payloads for all endpoints
4. Access to provider sandbox/test environment

---

## 🏗️ ARCHITECTURE PATTERNS

### Option 1: TJK-Style (With Internal Orchestration Layer)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Handler Layer (HTTP)                                │
│   handlers/api/v1/flight_handler.go                                      │
│   - Parse HTTP requests, bind JSON                                       │
│   - Call internal orchestration functions                                │
│   - Return standardized responses                                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   Internal Layer (Orchestration)                         │
│   internal/booking.go, internal/search.go                                │
│   - Business logic and validation                                        │
│   - Cache management (Redis)                                             │
│   - SSR enrichment                                                       │
│   - Pre-booking review for fresh pricing                                 │
│   - Calls transformers then services                                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
┌─────────────────────────────┐   ┌─────────────────────────────┐
│    Transformers              │   │    Services (API Clients)    │
│ - UnifiedModel → ProviderReq│   │ - Pure HTTP calls            │
│ - ProviderResp → UnifiedModel│   │ - Auth handling             │
└─────────────────────────────┘   └─────────────────────────────┘
```

### Option 2: AER-Style (Direct Handler Pattern)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Handler Layer                                       │
│   - Parse requests                                                       │
│   - Call services directly                                               │
│   - Call transformers for response                                       │
│   - Handle multi-step workflows inline                                   │
└─────────────────────────────────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌───────────────────┐   ┌───────────────────┐
│    Services       │   │   Transformers    │
└───────────────────┘   └───────────────────┘
```

---

## 📁 FILE STRUCTURE TEMPLATE

```
/{provider}/
├── main.go                          # Service entry point
├── Dockerfile                       # Container config
├── go.mod, go.sum                   # Dependencies
├── docs/
│   ├── {provider}_doc.md            # Provider API docs
│   └── {provider}-openapi.yaml      # OpenAPI spec
├── router/
│   └── v1/
│       └── routes.go                # Route definitions
├── handlers/
│   └── api/
│       └── v1/
│           └── flight_handler.go    # All flight handlers
├── services/
│   ├── client.go                    # HTTP client with auth
│   ├── search.go                    # Search APIs
│   └── booking.go                   # Booking APIs
├── models/
│   ├── search_request.go            # Unified search models
│   ├── review_request.go            # Review/pricing models
│   ├── booking_request.go           # Booking models
│   ├── ancillary_request.go         # SSR/Seatmap models
│   └── {provider}/
│       ├── search_types.go          # Provider search models
│       ├── booking_types.go         # Provider booking models
│       └── common_types.go          # Shared provider models
├── transformers/
│   ├── search_transformer.go        # Search response transformation
│   └── booking_transformer.go       # Booking response transformation
└── utils/
    └── validators.go                # Name validation, etc.
```

---

## 🔌 REQUIRED API ENDPOINTS

The backend MUST expose these exact endpoints to match frontend expectations:

### Search Flow
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/search` | POST | Initiate flight search |
| `/api/v1/search/:sessionId` | GET | Poll/get search results |

### Pricing & Ancillaries
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/review` | POST | Validate pricing before booking |
| `/api/v1/farerule` | POST | Get fare rules (singular for compat) |
| `/api/v1/farerules` | POST | Get fare rules (alias) |
| `/api/v1/seatmap` | POST | Get seat map |
| `/api/v1/ssr` | POST | Get SSR (meals, baggage, seats) |

### Booking Flow
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/book` | POST | Create booking + purchase + confirm |
| `/api/v1/booking/:id` | GET | Get booking details/ticket status |
| `/api/v1/confirm` | POST | Manual purchase (if separate step) |
| `/api/v1/confirm-status/:id` | GET | Poll purchase status |
| `/api/v1/cancel` | POST | Cancel booking |

### Health
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |

---

## 📝 RESPONSE FORMAT SPECIFICATIONS

### Search Response Format
```json
{
  "flights": [
    {
      "ids": ["sessionId:::segmentId"],
      "airlineCode": "AI",
      "airlineName": "Air India",
      "flightNumber": "AI-123",
      "origin": "DEL",
      "destination": "BOM",
      "depTime": "2026-01-20T08:00:00",
      "arrTime": "2026-01-20T10:00:00",
      "durationMinutes": 120,
      "price": 5000.00,
      "currency": "INR",
      "stops": 0,
      "SegmentInformation": [...],
      "totalPriceList": [
        {
          "PriceId": "sessionId:::segmentId",
          "fareIdentifier": "ECONOMY",
          "FareDetail": {
            "ADULT": {
              "CabinClass": "Economy",
              "ClassOfBooking": "S",
              "FareBasis": "SAVER",
              "SeatsRemaining": 5,
              "fareComponents": {
                "BaseFare": 4000.00,
                "TaxesAndFees": 1000.00,
                "TotalFare": 5000.00
              },
              "BaggageInformation": {
                "CabinBaggage": "7 Kg",
                "CheckingBaggage": "15 Kg"
              }
            }
          }
        }
      ],
      "provider": "PROVIDER_NAME"
    }
  ],
  "returnFlights": [],
  "isComplete": true,
  "sessionId": "uuid"
}
```

### Review Response Format
```json
{
  "status": {
    "httpStatus": 200,
    "success": true,
    "message": ""
  },
  "bookingId": "session_id_for_booking",
  "isValid": true,
  "priceChanged": false,
  "newPrice": 5000.00,
  "oldPrice": 5000.00,
  "conditions": {
    "dateOfBirth": { "adultDateofBirthRequired": true },
    "documentConditions": { "isDocumentIdApplicable": false },
    "gst": { "gstApplicable": true }
  }
}
```

### Book Response Format
```json
{
  "status": {
    "httpStatus": 200,
    "success": true,
    "message": "Ticket booked successfully!"
  },
  "bookingId": "uuid",
  "pnr": "FLT25-0115-0001",
  "tui": "session_id",
  "sessionId": "session_id",
  "provider": "PROVIDER_NAME",
  "condition": {
    "isRefundable": true,
    "isDateChangeable": true,
    "isFareChanged": false
  }
}
```

### Booking Details Response Format
```json
{
  "bookingId": "uuid",
  "displayId": "FLT25-0115-0001",
  "pnr": "FLT25-0115-0001",
  "airlinePnr": "ABC123",
  "bookingStatus": "Confirmed",
  "ticketStatus": "Ticketed",
  "totalAmount": 5000.00,
  "passengers": [
    {
      "type": "ADULT",
      "title": "Mr",
      "firstName": "John",
      "lastName": "Doe",
      "ticketNo": "0987654321"
    }
  ],
  "itinerary": [
    {
      "segmentId": "seg1",
      "carrier": "AI",
      "carrierName": "Air India",
      "flightNumber": "AI-123",
      "origin": "DEL",
      "originName": "Delhi",
      "destination": "BOM",
      "destinationName": "Mumbai",
      "departureTime": "2026-01-20T08:00:00",
      "arrivalTime": "2026-01-20T10:00:00",
      "cabinClass": "Economy"
    }
  ],
  "contact": {
    "email": "test@email.com",
    "mobile": "9999999999"
  },
  "status": {
    "httpStatus": 200,
    "success": true,
    "message": "Booking details retrieved"
  }
}
```

---

## 🔄 BOOKING FLOW - CRITICAL PATTERN

The `/api/v1/book` handler MUST implement this complete workflow internally:

```go
func (h *FlightHandler) Book(c *gin.Context) {
    // STEP 1: Create Booking
    bookingResp, err := h.client.CreateBooking(ctx, sessionID, req)
    if err != nil || !bookingResp.Status {
        // Return error with message
        return
    }
    
    bookingID := bookingResp.BookingID
    
    // STEP 2: Initiate Purchase (payment via wallet)
    purchaseResp, err := h.client.Purchase(ctx, sessionID, bookingID, amount, "Wallet")
    if err != nil || !purchaseResp.Status {
        // Return partial success - booking created but payment failed
        return
    }
    
    // STEP 3: Poll Purchase Status until confirmed
    var ticketStatus string
    var displayID string
    for i := 0; i < 10; i++ {
        time.Sleep(2 * time.Second)
        
        statusResp, err := h.client.GetPurchaseStatus(ctx, sessionID, bookingID)
        if err != nil {
            continue
        }
        
        ticketStatus = statusResp.Status
        displayID = statusResp.DisplayID
        
        if ticketStatus == "success" || ticketStatus == "failed" {
            break
        }
    }
    
    // STEP 4: Build response with confirmed ticket info
    response := transformers.TransformBookingResponse(bookingResp)
    if ticketStatus == "success" {
        response.Status.Success = true
        response.Status.Message = "Ticket booked successfully!"
        response.PNR = displayID
    }
    
    c.JSON(http.StatusOK, response)
}
```

---

## 🔧 TRANSFORMER PATTERNS

### Price ID Composition Pattern
```go
// Create composite PriceID: sessionId:::segmentId
compositePriceID := sessionID + ":::" + segmentID

// Extract sessionId from composite PriceID
parts := strings.SplitN(compositePriceID, ":::", 2)
sessionID := parts[0]
segmentID := parts[1]
```

### Error Handling Pattern
```go
func TransformBookingResponse(aerResp *provider.BookingResponse) *models.FrontendBookingResponse {
    isSuccess := aerResp.Status && aerResp.BookingID != ""
    
    message := "Booking created successfully"
    if !isSuccess {
        if aerResp.ErrorInfo != "" {
            message = aerResp.ErrorInfo
        } else if aerResp.SessionExpired {
            message = "Session expired. Please search again."
        } else {
            message = "Booking failed. Please try again."
        }
    }
    
    return &models.FrontendBookingResponse{
        Status: models.Status{
            HTTPStatus: 200,
            Success:    isSuccess,
            Message:    message,
        },
        BookingID: aerResp.BookingID,
        PNR:       aerResp.DisplayID,
        // ...
    }
}
```

### Dynamic JSON Parsing Pattern (for variable keys)
```go
type BookingDetailsResponse struct {
    BookingID      string                   `json:"booking_id"`
    BookingDetails map[string]BookingResult `json:"booking_details"` // Dynamic keys
    FlightSegments map[string]SegmentSet    `json:"flight_segments"` // Dynamic keys
}

// Iterate through dynamic keys
for key, result := range resp.BookingDetails {
    pnr = result.GdsPNR
    status = result.Status
    break // Take first one
}
```

---

## 🔐 AUTHENTICATION PATTERN

```go
type Client struct {
    BaseURL      string
    AccessToken  string
    RefreshToken string
    HTTPClient   *http.Client
}

func (c *Client) Request(ctx context.Context, method, path string, body, respDest interface{}) error {
    // 1. Ensure access token exists
    if c.AccessToken == "" && c.RefreshToken != "" {
        c.RefreshAuthToken()
    }
    
    // 2. Execute request
    resp, respBody, err := execute(c.AccessToken)
    
    // 3. If 401, refresh token and retry
    if resp.StatusCode == 401 {
        c.RefreshAuthToken()
        resp, respBody, err = execute(c.AccessToken)
    }
    
    // 4. Parse response
    return json.Unmarshal(respBody, respDest)
}
```

---

## ⚡ PERFORMANCE OPTIMIZATIONS

1. **Connection Pooling**
   ```go
   HTTPClient: &http.Client{
       Timeout: 120 * time.Second,
       Transport: &http.Transport{
           MaxIdleConns:        100,
           MaxIdleConnsPerHost: 100,
           IdleConnTimeout:     90 * time.Second,
       },
   }
   ```

2. **Context Timeouts**
   ```go
   ctx, cancel := context.WithTimeout(c.Request.Context(), 60*time.Second)
   defer cancel()
   ```

3. **Search Polling Optimization**
   ```go
   for i := 0; i < 5; i++ {
       resp := c.GetSearchData(sessionID)
       if resp.IsComplete {
           break
       }
       time.Sleep(2 * time.Second)
   }
   ```

4. **Itinerary Caching**
   ```go
   // If itineraries not provided, fetch from search cache
   if len(itineraries) == 0 {
       searchResp, _ := c.SearchWithSession(ctx, sessionID)
       itineraries = searchResp.Itineraries
   }
   ```

---

## ✅ INTEGRATION STEPS CHECKLIST

### Phase 1: Setup
- [ ] Create service directory structure
- [ ] Set up Docker configuration
- [ ] Configure environment variables (API keys, URLs)
- [ ] Implement HTTP client with auth
- [ ] Set up Redis cache (if using TJK-style architecture)

### Phase 2: Models
- [ ] Create provider-specific API models (`models/{provider}/`)
- [ ] Create unified frontend models (matching frontend expectations)
- [ ] Add JSON tags matching exact field names
- [ ] Handle dynamic/variable JSON keys with `map[string]Type`

### Phase 3: Services (API Clients)
- [ ] Implement Search (init + poll)
- [ ] Implement Review (air-pricing)
- [ ] Implement SSR (get ancillaries)
- [ ] Implement SeatMap
- [ ] Implement FareRules
- [ ] Implement Book (create-booking)
- [ ] Implement Purchase/Confirm (payment)
- [ ] Implement PurchaseStatus (poll)
- [ ] Implement GetBookingDetails (ticket-status)
- [ ] Implement Cancel

### Phase 4: Transformers
Create bidirectional transformers for each operation:
- [ ] `ToAirlineSearchRequest` / `FromAirlineSearchResponse`
- [ ] `ToAirlineReviewRequest` / `FromAirlineReviewResponse`
- [ ] `ToAirlineBookRequest` / `FromAirlineBookResponse`
- [ ] `ToAirlineConfirmRequest` / `FromAirlineConfirmResponse`
- [ ] `ToAirlineBookingDetailsRequest` / `FromAirlineBookingDetailsResponse`
- [ ] `ToAirlineCancelRequest` / `FromAirlineCancelResponse`
- [ ] SSR/SeatMap transformers

### Phase 5: Internal Orchestration (TJK-style)
If using TJK architecture:
- [ ] `internal/search.go` - Search orchestration with caching
- [ ] `internal/booking.go` - Pre-booking review, SSR enrichment
- [ ] `internal/ancillary.go` - SSR/Seatmap orchestration
- [ ] `internal/cancel.go` - Cancellation logic

### Phase 6: Handlers
- [ ] Search handler (POST search, GET poll)
- [ ] Review handler
- [ ] Book handler (with complete workflow)
- [ ] Confirm handler (if separate step)
- [ ] GetBooking handler
- [ ] SSR/SeatMap/FareRules handlers
- [ ] Cancel handler
- [ ] Health check handler

### Phase 7: Testing
- [ ] Test search → poll → results
- [ ] Test review → pricing validation
- [ ] Test book → purchase → confirm → ticket
- [ ] Test getBooking → full details with SSR
- [ ] Test error scenarios (session timeout, payment failure)
- [ ] Test round-trip bookings

---

## 🔷 TJK-SPECIFIC PATTERNS (Internal Orchestration)

### Pre-Booking Review Pattern
```go
// Always perform review before book to get fresh BookingID and Amount
func BookFlight(ctx context.Context, req models.BookRequest, client BookingClient) (*models.BookResponse, error) {
    // If PriceIds are provided, ALWAYS perform a Review first
    if len(req.PriceIDs) > 0 {
        reviewReq := models.ReviewRequest{
            PriceIDs:   req.PriceIDs,
            Adults:     countByType(req.Passengers, "ADULT"),
            Children:   countByType(req.Passengers, "CHILD"),
            Infants:    countByType(req.Passengers, "INFANT"),
            Passengers: req.Passengers,
        }
        
        tjkReviewReq, _ := transformers.ToAirlineReviewRequest(reviewReq)
        tjkReviewResp, err := client.ReviewFlight(ctx, tjkReviewReq)
        
        if err == nil && tjkReviewResp.Status.Success {
            // Update BookingID from review response
            req.BookingID = tjkReviewResp.BookingId
            
            // Update amount from review (may include SSR prices)
            transformedReview, _ := transformers.FromAirlineReviewResponse(tjkReviewResp, reviewReq)
            if transformedReview != nil && transformedReview.NewPrice > 0 {
                req.Amount = transformedReview.NewPrice
            }
            
            // Build segmentSSRMap for SSR assignment
            segmentSSRMap = buildSegmentSSRMap(tjkReviewResp)
        }
    }
    
    // Now proceed with booking using updated BookingID and Amount
    tjkReq, _ := transformers.ToAirlineBookRequest(req, segmentSSRMap)
    tjkResp, err := client.BookFlight(ctx, tjkReq)
    
    return transformers.FromAirlineBookResponse(tjkResp)
}
```

### Redis SSR Caching Pattern
```go
// Cache SSR info from Review for later enrichment
func cacheSSRFromReview(bookingId string, tjkResp *tjk.ReviewResponse) {
    rc, err := cache.GetRedisClient()
    if err != nil || rc == nil {
        return
    }
    
    ssrResp := buildSSRResponseFromReview(tjkResp)
    data, _ := json.Marshal(ssrResp)
    rc.Set(context.Background(), "ssr:"+bookingId, data, 24*time.Hour)
}

// Later: Enrich booking details with cached SSR
func enrichWithCachedSSR(ctx context.Context, bookingID string, tjkResp *tjk.BookingDetailsResponse) {
    rc, _ := cache.GetRedisClient()
    cachedData, err := rc.Get(ctx, "ssr:"+bookingID).Bytes()
    if err == nil {
        var ssrResp tjk.SsrResponse
        json.Unmarshal(cachedData, &ssrResp)
        // Merge SSR into booking response
        mergeSsrIntoBooking(tjkResp, &ssrResp)
    }
}
```

### SSR Enrichment in Booking Details
```go
func GetBookingDetails(ctx context.Context, bookingID string, client BookingClient) (*models.BookingDetailsResponse, error) {
    // Fetch booking details
    tjkResp, err := client.GetBookingDetails(ctx, &tjk.BookingDetailsRequest{BookingId: bookingID})
    if err != nil {
        return nil, err
    }
    
    // Check if SSR info is missing
    hasSsr := checkIfTravellersHaveSSR(tjkResp)
    
    if !hasSsr {
        // Try Redis cache first
        var ssrResp tjk.SsrResponse
        foundInCache := tryGetFromRedis("ssr:"+bookingID, &ssrResp)
        
        if !foundInCache {
            // Fall back to live SSR call
            liveSsrResp, err := client.GetSsr(ctx, &tjk.SsrRequest{BookingId: bookingID})
            if err == nil && liveSsrResp.Status.Success {
                ssrResp = *liveSsrResp
                foundInCache = true
            }
        }
        
        if foundInCache {
            // Enrich traveller infos with fetched SSR
            enrichTravellersWithSSR(tjkResp, &ssrResp)
        }
    }
    
    return transformers.FromAirlineBookingDetailsResponse(tjkResp)
}
```

### Segment SSR Mapping
```go
// Build map of SSR codes to segment IDs
func buildSegmentSSRMap(reviewResp *tjk.ReviewResponse) map[string][]string {
    segmentSSRMap := make(map[string][]string)
    
    for _, trip := range reviewResp.TripInfos {
        for _, seg := range trip.SI {
            if seg.SsrInfo != nil {
                // Map meal codes to segment
                for _, m := range seg.SsrInfo.Meal {
                    segmentSSRMap[m.Code] = append(segmentSSRMap[m.Code], seg.ID)
                }
                // Map baggage codes to segment
                for _, b := range seg.SsrInfo.Baggage {
                    segmentSSRMap[b.Code] = append(segmentSSRMap[b.Code], seg.ID)
                }
                // Map seat codes to segment
                for _, s := range seg.SsrInfo.Seat {
                    segmentSSRMap[s.Code] = append(segmentSSRMap[s.Code], seg.ID)
                }
            }
        }
    }
    
    return segmentSSRMap
}
```

---

## 🔶 AER-SPECIFIC PATTERNS (Session-Based Workflow)

### Complete Booking in Single Handler
```go
func (h *FlightHandler) Book(c *gin.Context) {
    // STEP 1: Create Booking
    aerResp, _ := h.client.Book(ctx, sessionID, req)
    if !aerResp.Status || aerResp.BookingID == "" {
        // Return error response
        return
    }
    
    // STEP 2: Call Purchase (wallet payment)
    amount := fmt.Sprintf("%.2f", req.Amount)
    purchaseResp, _ := h.client.Confirm(ctx, sessionID, aerResp.BookingID, amount, "Wallet")
    if !purchaseResp.Status {
        // Booking created but payment failed
        return
    }
    
    // STEP 3: Poll Purchase Status
    for i := 0; i < 10; i++ {
        time.Sleep(2 * time.Second)
        statusResp, _ := h.client.GetPurchaseStatus(ctx, sessionID, aerResp.BookingID)
        
        if statusResp.Status == "success" {
            response.PNR = statusResp.DisplayID
            break
        } else if statusResp.Status == "failed" {
            response.Status.Success = false
            break
        }
    }
    
    c.JSON(http.StatusOK, response)
}
```

### Session ID Extraction
```go
// Extract sessionID from composite priceID (sessionId:::segmentId)
func extractSessionFromPriceID(priceID string) (sessionID, segmentID string) {
    parts := strings.SplitN(priceID, ":::", 2)
    if len(parts) == 2 {
        return parts[0], parts[1]
    }
    return priceID, priceID
}

// In handler:
sessionID := ""
if len(req.PriceIDs) > 0 {
    sessionID, _ = extractSessionFromPriceID(req.PriceIDs[0])
}
if sessionID == "" && req.BookingID != "" {
    sessionID = req.BookingID  // BookingID from review is actually sessionID
}
```

### Itinerary Fetching from Cache
```go
// AerTicket requires itineraries in booking request
// If not provided, fetch from cached search response
func (c *Client) Book(ctx context.Context, sessionID string, req models.BookingRequest) (*aer.CreateBookingResponse, error) {
    itineraries := req.Itineraries
    
    if len(itineraries) == 0 {
        // Fetch from search cache using session ID
        searchResp, err := c.SearchWithSession(ctx, sessionID)
        if err == nil && searchResp != nil {
            itineraries = searchResp.FlightSearchResponse.Itineraries
        }
    }
    
    aerReq := aer.CreateBookingRequest{
        SessionID:   sessionID,
        Itineraries: itineraries,
        // ... other fields
    }
    
    return c.Request(ctx, "POST", "/flights/create-booking", aerReq, &resp)
}
```

---

---

## 📌 COMMON PITFALLS TO AVOID

1. **Session Management**
   - Sessions expire (typically 15-30 min)
   - Always extract sessionId from composite priceIds
   - Fetch itineraries from search cache if not provided

2. **Response Field Naming**
   - Frontend expects specific JSON field names
   - Use exact casing: `bookingId`, `PriceId`, `totalPriceList`
   - Add both singular and plural endpoints if needed

3. **Async Workflows**
   - Provider APIs often require polling
   - Implement polling internally in handlers
   - Don't return incomplete data to frontend

4. **Error Handling**
   - Always return structured error responses
   - Include provider's error message when available
   - Return HTTP 200 with `success: false` for business errors

5. **Amount Formatting**
   - Providers may expect string amounts: `"3267.00"`
   - Frontend sends numeric amounts
   - Convert appropriately in handlers

---

## 🚀 USAGE

To integrate a new provider, copy this template and:

1. Replace `{provider}` with actual provider name (lowercase)
2. Study provider API docs thoroughly
3. Map each provider endpoint to required endpoints above
4. Implement transformers to convert provider responses
5. Test complete flow end-to-end

---

**Version**: 2.0
**Last Updated**: 2026-01-15
**Based On**: TripJack (TJK) and AerTicket (AER) Integration Experience
**Reference Implementations**: `/tjk/`, `/aer/`

