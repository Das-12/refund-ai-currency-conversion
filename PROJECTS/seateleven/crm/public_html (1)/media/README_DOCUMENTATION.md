# GraphQL Plugin Documentation

## 📚 Documentation Overview

This directory contains comprehensive documentation for the Perfex CRM GraphQL Plugin. The documentation is organized into multiple files for easy navigation and reference.

---

## 📖 Documentation Files

### 1. **OPERATIONS_DOCUMENTATION.md** (Main Documentation)
**Complete reference guide covering all operations**

**Contents:**
- Overview and key features
- Authentication methods
- Query operations (read data)
- Mutation operations (create, update, delete)
- Filtering operations (8 comparison operators)
- Relational operations (foreign key filtering)
- Technical implementation details
- API reference and examples
- Best practices and troubleshooting

**Use this when:** You need detailed information about any operation or feature.

---

### 2. **QUICK_REFERENCE.md** (Quick Lookup)
**Fast reference for common operations and syntax**

**Contents:**
- Authentication syntax
- Query templates
- Mutation templates
- Filter operator table
- Common examples
- cURL examples
- Error responses
- Tips and limitations

**Use this when:** You need a quick syntax reminder or example.

---

### 3. **COMPLETE_OPERATIONS_LIST.md** (Structured List)
**Comprehensive structured list of all supported operations**

**Contents:**
- Query operations breakdown
- Mutation operations breakdown
- Filter operations catalog
- Schema operations
- Operation counts and statistics
- Naming conventions
- Capabilities matrix
- Limitations and security

**Use this when:** You need to understand the full scope of available operations.

---

### 4. **OPERATION_FLOW_DIAGRAMS.md** (Visual Guide)
**Visual flowcharts and architecture diagrams**

**Contents:**
- Request flow diagram
- Query resolution flow
- Schema generation flow
- Mutation flow diagrams
- Relational filtering flow
- Type detection flow
- Error handling flow
- Architecture layers
- Component interaction map

**Use this when:** You need to understand how operations work internally.

---

### 5. **GRAPHQL_FILTERING_GUIDE.md** (Existing Guide)
**Original filtering documentation with examples**

**Contents:**
- Basic filtering
- Comparison operators
- Relational filtering
- Advanced examples
- Best practices
- Common use cases
- Troubleshooting

**Use this when:** You need filtering-specific examples and use cases.

---

## 🚀 Quick Start

### Step 1: Authentication
Get your auth token from the admin panel:
```
Admin → GraphQL → Token Management
```

### Step 2: Make Your First Request
```bash
curl -X POST https://your-domain.com/graphql \
  -H "Content-Type: application/json" \
  -H "authtoken: your-token-here" \
  -d '{
    "query": "query {\n  tblstaff {\n    staffid\n    firstname\n    email\n  }\n}"
  }'
```

### Step 3: Explore Operations
- **Read data:** Use queries
- **Create data:** Use `add<TableName>` mutations
- **Update data:** Use `update<TableName>` mutations
- **Delete data:** Use `delete<TableName>` mutations
- **Filter data:** Use operator suffixes (`_eq`, `_gt`, `_like`, etc.)

---

## 📋 Supported Operations Summary

### Core Operations
✅ **Query (Read)** - Fetch data from any table  
✅ **Create (Insert)** - Add new records  
✅ **Update** - Modify existing records  
✅ **Delete** - Remove records  

### Filter Operators (8 Total)
✅ Equal (`_eq`)  
✅ Not Equal (`_ne`)  
✅ Greater Than (`_gt`)  
✅ Greater Than or Equal (`_gte`)  
✅ Less Than (`_lt`)  
✅ Less Than or Equal (`_lte`)  
✅ Like (`_like`)  
✅ In (`_in`)  

### Advanced Features
✅ Multi-table queries  
✅ Relational filtering (foreign keys)  
✅ Dynamic schema generation  
✅ Token authentication  
✅ Automatic type detection  

---

## 🎯 Common Use Cases

### 1. Fetch All Records
```graphql
query {
  tblstaff {
    staffid
    firstname
    email
  }
}
```

### 2. Filter by Date
```graphql
query {
  tbltasks(startdate_eq: "2025-12-12") {
    id
    name
    startdate
  }
}
```

### 3. Date Range Filter
```graphql
query {
  tbltasks(
    startdate_gte: "2025-12-01",
    startdate_lte: "2025-12-31"
  ) {
    id
    name
  }
}
```

### 4. Create Record
```graphql
mutation {
  addTbltasks(
    name: "New Task",
    startdate: "2025-12-15"
  ) {
    id
    message
  }
}
```

### 5. Update Record
```graphql
mutation {
  updateTbltasks(
    id: 123,
    status: "completed"
  ) {
    message
  }
}
```

### 6. Delete Record
```graphql
mutation {
  deleteTbltasks(id: 123) {
    message
  }
}
```

### 7. Relational Filter
```graphql
query {
  tbltaskstimers(
    relational_filters: "{\"task_id\": {\"startdate_eq\": \"2025-12-12\"}}"
  ) {
    id
    task_id
    start_time
  }
}
```

---

## 🔑 Key Concepts

### Dynamic Schema
The plugin automatically generates GraphQL schemas for **all database tables**. No manual configuration needed!

### Naming Conventions
- **Queries:** Use exact table name (e.g., `tblstaff`, `tbltasks`)
- **Mutations:** Use `add/update/delete` + PascalCase table name (e.g., `addTblstaff`)
- **Filters:** Use field name + `_` + operator (e.g., `startdate_eq`)

### Type Detection
- Fields named `id` or ending with `_id` → Integer type
- All other fields → String type
- Query results → List of objects

### Foreign Key Mapping
- `task_id` → `tbltasks` or `tbltask`
- `staff_id` → `tblstaffs` or `tblstaff`
- Pattern: `tbl<name>s` or `tbl<name>`

---

## ⚠️ Limitations

❌ **Not Supported:**
- Pagination (LIMIT/OFFSET)
- Sorting (ORDER BY)
- Aggregation (COUNT, SUM, AVG)
- OR logic between filters
- NULL/NOT NULL checks
- Nested relations (beyond one level)
- GraphQL subscriptions
- Batch operations

---

## 🛠️ Troubleshooting

### Empty Results
- Verify filter values match database format
- Check date format: `YYYY-MM-DD`
- Ensure string comparisons match case

### Authentication Failed
- Verify `authtoken` header is present
- Check token matches database value
- Ensure module is activated

### Relational Filter Not Working
- Ensure JSON is properly escaped
- Verify foreign key field name
- Check related table exists

### Syntax Error
- Escape newlines as `\n`
- Properly escape quotes in JSON
- Validate JSON structure

---

## 📊 Documentation Map

```
┌─────────────────────────────────────────────────────────────┐
│                    START HERE                               │
│                                                             │
│  Need quick syntax?  ──────────► QUICK_REFERENCE.md        │
│                                                             │
│  Need detailed info? ──────────► OPERATIONS_DOCUMENTATION.md│
│                                                             │
│  Need complete list? ──────────► COMPLETE_OPERATIONS_LIST.md│
│                                                             │
│  Need visual guide?  ──────────► OPERATION_FLOW_DIAGRAMS.md │
│                                                             │
│  Need filter examples? ────────► GRAPHQL_FILTERING_GUIDE.md │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔗 Additional Resources

- **Admin Panel:** `Admin → GraphQL → Token Management`
- **Online Guide:** https://perfexcrm.themesic.com/graphqlguide/
- **CodeCanyon:** https://codecanyon.net/item/perfex-graphql-api-query-all-crms-data-including-custom-modules/54869954

---

## 📝 Version Information

- **Plugin Version:** 1.0.1
- **Documentation Version:** 1.0
- **Last Updated:** December 16, 2025
- **Minimum Perfex CRM:** 2.9.*

---

## 📧 Support

For issues or questions:
1. Check the relevant documentation file
2. Review the troubleshooting section
3. Test with simple queries first
4. Add complexity incrementally
5. Contact support if needed

---

## 🎓 Learning Path

### Beginner
1. Read **QUICK_REFERENCE.md** for basic syntax
2. Try simple queries from examples
3. Experiment with basic filters

### Intermediate
1. Read **OPERATIONS_DOCUMENTATION.md** for details
2. Try multi-table queries
3. Use relational filtering
4. Combine multiple filters

### Advanced
1. Read **COMPLETE_OPERATIONS_LIST.md** for full scope
2. Study **OPERATION_FLOW_DIAGRAMS.md** for internals
3. Optimize queries for performance
4. Build complex integrations

---

## 📌 Quick Tips

✅ **DO:**
- Request only needed fields
- Use server-side filtering
- Combine multiple filters
- Escape JSON properly

❌ **DON'T:**
- Fetch all fields unnecessarily
- Filter data client-side
- Forget to escape quotes in JSON
- Skip authentication headers

---

## 🎉 Getting Started Checklist

- [ ] Get auth token from admin panel
- [ ] Test basic query with cURL
- [ ] Try filtering with one operator
- [ ] Test create mutation
- [ ] Test update mutation
- [ ] Test delete mutation
- [ ] Try multi-table query
- [ ] Experiment with relational filtering
- [ ] Review best practices
- [ ] Build your integration

---

**Happy Querying! 🚀**
