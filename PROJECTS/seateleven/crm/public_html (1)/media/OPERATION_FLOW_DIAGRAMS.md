# GraphQL Plugin - Operation Flow & Architecture

## Request Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT REQUEST                          │
│                                                                 │
│  POST /graphql                                                  │
│  Headers: { authtoken: "xxx", Content-Type: "application/json" }│
│  Body: { "query": "..." }                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION LAYER                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ validate_token()                                         │  │
│  │ • Extract authtoken from headers                         │  │
│  │ • Retrieve stored token from database                    │  │
│  │ • Compare tokens                                         │  │
│  │ • Return 403 if invalid                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MODULE ACTIVATION CHECK                      │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • Check if GraphQL module is active                      │  │
│  │ • Return 403 if not active                               │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SCHEMA GENERATION                            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Get all database tables                               │  │
│  │    $tables = $this->db->list_tables()                    │  │
│  │                                                           │  │
│  │ 2. For each table:                                       │  │
│  │    ┌─────────────────────────────────────────────────┐  │  │
│  │    │ • Create Query Type                              │  │  │
│  │    │   - getFieldsFromTable()                         │  │  │
│  │    │   - getFilterArgsForTable()                      │  │  │
│  │    │   - Set resolve function                         │  │  │
│  │    │                                                   │  │  │
│  │    │ • Create Mutation Types                          │  │  │
│  │    │   - add<Table> (INSERT)                          │  │  │
│  │    │   - update<Table> (UPDATE)                       │  │  │
│  │    │   - delete<Table> (DELETE)                       │  │  │
│  │    └─────────────────────────────────────────────────┘  │  │
│  │                                                           │  │
│  │ 3. Build GraphQL Schema                                  │  │
│  │    - Query Type with all table queries                  │  │
│  │    - Mutation Type with all mutations                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    QUERY PARSING                                │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • Extract query from request body                        │  │
│  │ • Parse GraphQL query string                             │  │
│  │ • Validate syntax                                        │  │
│  │ • Return error if invalid                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    QUERY EXECUTION                              │
│                                                                 │
│  Is it a QUERY or MUTATION?                                    │
│                                                                 │
│  ┌──────────────────┐              ┌──────────────────────┐    │
│  │     QUERY        │              │      MUTATION        │    │
│  │                  │              │                      │    │
│  │ ┌──────────────┐ │              │ ┌──────────────────┐ │    │
│  │ │ Resolve      │ │              │ │ CREATE (INSERT)  │ │    │
│  │ │ Function     │ │              │ │ • Insert data    │ │    │
│  │ │ Called       │ │              │ │ • Return ID      │ │    │
│  │ └──────┬───────┘ │              │ └──────────────────┘ │    │
│  │        │         │              │                      │    │
│  │        ▼         │              │ ┌──────────────────┐ │    │
│  │ ┌──────────────┐ │              │ │ UPDATE           │ │    │
│  │ │ Apply        │ │              │ │ • Find by ID     │ │    │
│  │ │ Filters      │ │              │ │ • Update fields  │ │    │
│  │ │ And Fetch    │ │              │ │ • Return result  │ │    │
│  │ └──────┬───────┘ │              │ └──────────────────┘ │    │
│  │        │         │              │                      │    │
│  │        ▼         │              │ ┌──────────────────┐ │    │
│  │   See Below      │              │ │ DELETE           │ │    │
│  └──────────────────┘              │ │ • Find by ID     │ │    │
│                                    │ │ • Delete record  │ │    │
│                                    │ │ • Return message │ │    │
│                                    │ └──────────────────┘ │    │
│                                    └──────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Query Resolution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              applyFiltersAndFetch($table, $args)                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Has relational │
                    │ filters?       │
                    └───┬────────┬───┘
                        │        │
                   YES  │        │  NO
                        │        │
                        ▼        └──────────────┐
        ┌───────────────────────────┐           │
        │ RELATIONAL FILTER PROCESS │           │
        │                           │           │
        │ 1. Parse JSON filters     │           │
        │ 2. For each foreign key:  │           │
        │    ┌─────────────────────┐│           │
        │    │ • Get related table ││           │
        │    │   (getRelatedTable  ││           │
        │    │    FromForeignKey)  ││           │
        │    │                     ││           │
        │    │ • Query related     ││           │
        │    │   table with filters││           │
        │    │   (getRelatedIds)   ││           │
        │    │                     ││           │
        │    │ • Get matching IDs  ││           │
        │    │                     ││           │
        │    │ • Apply WHERE IN    ││           │
        │    │   to main query     ││           │
        │    └─────────────────────┘│           │
        └───────────┬───────────────┘           │
                    │                           │
                    └───────────┬───────────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │   DIRECT FILTER PROCESS       │
                │                               │
                │ For each field filter:        │
                │                               │
                │ • field_eq   → WHERE =        │
                │ • field_ne   → WHERE !=       │
                │ • field_gt   → WHERE >        │
                │ • field_gte  → WHERE >=       │
                │ • field_lt   → WHERE <        │
                │ • field_lte  → WHERE <=       │
                │ • field_like → WHERE LIKE     │
                │ • field_in   → WHERE IN       │
                └───────────┬───────────────────┘
                            │
                            ▼
                ┌───────────────────────────────┐
                │   EXECUTE DATABASE QUERY      │
                │                               │
                │   $this->db->get($table)      │
                │         ->result()            │
                └───────────┬───────────────────┘
                            │
                            ▼
                ┌───────────────────────────────┐
                │   RETURN RESULTS              │
                │                               │
                │   Array of objects            │
                └───────────────────────────────┘
```

## Schema Generation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    getFieldsFromTable($table)                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Get table columns          │
                │ $this->db->list_fields()   │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ For each column:           │
                │                            │
                │ ┌────────────────────────┐ │
                │ │ Is field = 'id'?       │ │
                │ │   YES → Type::int()    │ │
                │ │   NO  → Type::string() │ │
                │ └────────────────────────┘ │
                │                            │
                │ ┌────────────────────────┐ │
                │ │ Create field config:   │ │
                │ │ • type                 │ │
                │ │ • resolve function     │ │
                │ └────────────────────────┘ │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Return fields array        │
                └────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                getFilterArgsForTable($table)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Get table columns          │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ For each column:           │
                │                            │
                │ ┌────────────────────────┐ │
                │ │ Detect field type:     │ │
                │ │ • id, *_id, id* → int  │ │
                │ │ • others → string      │ │
                │ └────────────────────────┘ │
                │                            │
                │ ┌────────────────────────┐ │
                │ │ Create 8 operators:    │ │
                │ │ • field_eq             │ │
                │ │ • field_ne             │ │
                │ │ • field_gt             │ │
                │ │ • field_gte            │ │
                │ │ • field_lt             │ │
                │ │ • field_lte            │ │
                │ │ • field_like           │ │
                │ │ • field_in (list)      │ │
                │ └────────────────────────┘ │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Add relational_filters arg │
                │ (JSON string type)         │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Return args array          │
                └────────────────────────────┘
```

## Mutation Flow Diagrams

### CREATE (INSERT) Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              mutation { add<Table>(fields) { ... } }            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Resolve function called    │
                │ with $args (field values)  │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Execute INSERT             │
                │ $this->db->insert(         │
                │   $table, $args            │
                │ )                          │
                └────────────┬───────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                SUCCESS            FAILURE
                    │                 │
                    ▼                 ▼
        ┌───────────────────┐   ┌──────────────────┐
        │ Get inserted ID   │   │ Return error     │
        │ $this->db->       │   │ message          │
        │   insert_id()     │   │                  │
        └─────────┬─────────┘   └──────────────────┘
                  │
                  ▼
        ┌───────────────────┐
        │ Return:           │
        │ • id              │
        │ • message         │
        │ • requested fields│
        └───────────────────┘
```

### UPDATE Flow

```
┌─────────────────────────────────────────────────────────────────┐
│         mutation { update<Table>(id, fields) { ... } }          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Extract ID from args       │
                │ Remove ID from data        │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Execute UPDATE             │
                │ $this->db                  │
                │   ->where('id', $id)       │
                │   ->update($table, $data)  │
                └────────────┬───────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                SUCCESS            FAILURE
                    │                 │
                    ▼                 ▼
        ┌───────────────────┐   ┌──────────────────┐
        │ Fetch updated row │   │ Return error     │
        │ $this->db->       │   │ message          │
        │   get_where()     │   │                  │
        └─────────┬─────────┘   └──────────────────┘
                  │
                  ▼
        ┌───────────────────┐
        │ Return:           │
        │ • message         │
        │ • updated fields  │
        └───────────────────┘
```

### DELETE Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              mutation { delete<Table>(id) { ... } }             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Extract ID from args       │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Execute DELETE             │
                │ $this->db->delete(         │
                │   $table, ['id' => $id]    │
                │ )                          │
                └────────────┬───────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                SUCCESS            FAILURE
                    │                 │
                    ▼                 ▼
        ┌───────────────────┐   ┌──────────────────┐
        │ Return success    │   │ Return error     │
        │ message           │   │ message          │
        └───────────────────┘   └──────────────────┘
```

## Relational Filtering Flow

```
┌─────────────────────────────────────────────────────────────────┐
│   relational_filters: "{\"task_id\": {\"startdate_eq\": ...}}"  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Parse JSON string          │
                │ json_decode()              │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ For each foreign key:      │
                │ e.g., "task_id"            │
                └────────────┬───────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────┐
        │ getRelatedTableFromForeignKey("task_id")   │
        │                                            │
        │ 1. Remove "_id" → "task"                   │
        │ 2. Try patterns:                           │
        │    • "tbltasks"  ✓ (found)                 │
        │    • "tbltask"                             │
        │ 3. Return first match                      │
        └────────────┬───────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────────────┐
        │ getRelatedIds("tbltasks", filters)         │
        │                                            │
        │ 1. Apply filters to related table:         │
        │    • startdate_eq: "2025-12-12"            │
        │                                            │
        │ 2. Execute query on "tbltasks"             │
        │                                            │
        │ 3. Extract IDs from results:               │
        │    • [1, 5, 12, 23]                        │
        └────────────┬───────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────────────┐
        │ Apply to main query:                       │
        │ $this->db->where_in('task_id', [1,5,12,23])│
        └────────────────────────────────────────────┘
```

## Type Detection Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      Field Type Detection                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Field name     │
                    └───┬────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ name = "id"? │ │ name ends    │ │ name starts  │
│              │ │ with "_id"?  │ │ with "id"?   │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
      YES              YES              YES
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
                ┌──────────────┐
                │ Type::int()  │
                └──────────────┘
                        
                       NO (all)
                        │
                        ▼
                ┌──────────────┐
                │Type::string()│
                └──────────────┘
```

## Complete Request-Response Cycle

```
CLIENT                    SERVER                     DATABASE
  │                         │                            │
  │  POST /graphql          │                            │
  │  + authtoken            │                            │
  │────────────────────────>│                            │
  │                         │                            │
  │                         │ Validate Token             │
  │                         │ Check Module Active        │
  │                         │                            │
  │                         │ Get Tables                 │
  │                         │───────────────────────────>│
  │                         │<───────────────────────────│
  │                         │ [table1, table2, ...]      │
  │                         │                            │
  │                         │ For each table:            │
  │                         │   Get Fields               │
  │                         │───────────────────────────>│
  │                         │<───────────────────────────│
  │                         │ [field1, field2, ...]      │
  │                         │                            │
  │                         │ Generate Schema            │
  │                         │ Parse Query                │
  │                         │                            │
  │                         │ Execute Query/Mutation     │
  │                         │───────────────────────────>│
  │                         │<───────────────────────────│
  │                         │ Results                    │
  │                         │                            │
  │                         │ Format Response            │
  │<────────────────────────│                            │
  │  JSON Response          │                            │
  │                         │                            │
```

## Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         REQUEST RECEIVED                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Token valid?   │
                    └───┬────────┬───┘
                        │        │
                       NO       YES
                        │        │
                        ▼        │
            ┌───────────────┐   │
            │ Return 403    │   │
            │ "Unauthorized"│   │
            └───────────────┘   │
                                │
                                ▼
                    ┌────────────────┐
                    │ Module active? │
                    └───┬────────┬───┘
                        │        │
                       NO       YES
                        │        │
                        ▼        │
            ┌───────────────┐   │
            │ Return 403    │   │
            │ "Not active"  │   │
            └───────────────┘   │
                                │
                                ▼
                    ┌────────────────┐
                    │ Query provided?│
                    └───┬────────┬───┘
                        │        │
                       NO       YES
                        │        │
                        ▼        │
            ┌───────────────┐   │
            │ Return error  │   │
            │ "No query"    │   │
            └───────────────┘   │
                                │
                                ▼
                    ┌────────────────┐
                    │ Execute query  │
                    └───┬────────┬───┘
                        │        │
                    ERROR      SUCCESS
                        │        │
                        ▼        ▼
            ┌───────────────┐   ┌───────────────┐
            │ Catch         │   │ Return data   │
            │ Exception     │   │ in JSON       │
            │ Return error  │   └───────────────┘
            └───────────────┘
```

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                         │
│  • HTTP Request/Response                                        │
│  • JSON Encoding/Decoding                                       │
│  • Header Processing                                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                      SECURITY LAYER                             │
│  • Token Authentication                                         │
│  • Module Activation Check                                      │
│  • CSRF Exclusion                                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                      GRAPHQL LAYER                              │
│  • Schema Generation                                            │
│  • Query Parsing                                                │
│  • Type System                                                  │
│  • Resolvers                                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                       │
│  • Field Detection                                              │
│  • Filter Processing                                            │
│  • Relational Mapping                                           │
│  • Query Building                                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                      DATA ACCESS LAYER                          │
│  • CodeIgniter Query Builder                                    │
│  • Database Connection                                          │
│  • Result Formatting                                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                             │
│  • MySQL/MariaDB                                                │
│  • Tables & Columns                                             │
│  • Data Storage                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Component Interaction Map

```
┌──────────────────────────────────────────────────────────────────┐
│              GraphqlIntegrationController                        │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐   │
│  │ validate_token │  │     index      │  │getFieldsFromTable│  │
│  │                │  │                │  │                 │   │
│  │ • Check auth   │  │ • Generate     │  │ • List fields   │   │
│  │ • Return 403   │  │   schema       │  │ • Detect types  │   │
│  │   if invalid   │  │ • Parse query  │  │ • Create config │   │
│  └────────┬───────┘  │ • Execute      │  └────────┬────────┘   │
│           │          │ • Return JSON  │           │            │
│           │          └────────┬───────┘           │            │
│           │                   │                   │            │
│           │          ┌────────▼───────┐           │            │
│           │          │getFilterArgs   │           │            │
│           │          │ForTable        │           │            │
│           │          │                │           │            │
│           │          │ • Create 8 ops │           │            │
│           │          │ • Add relational│          │            │
│           │          └────────┬───────┘           │            │
│           │                   │                   │            │
│           │          ┌────────▼───────────────────▼────┐       │
│           │          │ applyFiltersAndFetch           │       │
│           │          │                                │       │
│           │          │ • Process relational filters   │       │
│           │          │ • Apply direct filters         │       │
│           │          │ • Execute query                │       │
│           │          └────────┬───────────────────────┘       │
│           │                   │                               │
│           │          ┌────────▼──────────┐                    │
│           │          │getRelatedTable    │                    │
│           │          │FromForeignKey     │                    │
│           │          │                   │                    │
│           │          │ • Parse FK name   │                    │
│           │          │ • Find table      │                    │
│           │          └────────┬──────────┘                    │
│           │                   │                               │
│           │          ┌────────▼──────────┐                    │
│           │          │ getRelatedIds     │                    │
│           │          │                   │                    │
│           │          │ • Query related   │                    │
│           │          │ • Extract IDs     │                    │
│           │          └───────────────────┘                    │
│           │                                                   │
└───────────┼───────────────────────────────────────────────────┘
            │
            ▼
┌───────────────────────────────────────────────────────────────┐
│                    External Dependencies                      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ GraphQL-PHP  │  │ CodeIgniter  │  │ Database         │   │
│  │ Library      │  │ Framework    │  │ (MySQL/MariaDB)  │   │
│  │              │  │              │  │                  │   │
│  │ • Schema     │  │ • Query      │  │ • Tables         │   │
│  │ • Types      │  │   Builder    │  │ • Columns        │   │
│  │ • Execution  │  │ • Database   │  │ • Data           │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
└───────────────────────────────────────────────────────────────┘
```

---

**Document Version:** 1.0  
**Last Updated:** December 16, 2025  
**Plugin Version:** 1.0.1
