# Manual hardware

- Add manual hardware to the central SQLite order facts; a Traveler is not required and is not read or modified.
- Accept either the canonical factory-order number or its factory-order name, and resolve it uniquely from the active order index.
- Resolve the SKU, name, and specification from the local product catalog; do not query live stock.
- Require a positive integer quantity. Aggregate an existing active manual row when factory-order number, SKU, and specification all match; collapse duplicate legacy rows during the same transaction.
- Show the full item preview and require local approval before writing.
- Write and commit the database transaction, then reread the target row and verify the final quantity.
- Generate or update a Traveler later from the central database when the user explicitly requests that export.
- Keep factory orders separate in `Picking List`; do not display an order-level hardware total.
- Do not query inventory when hardware is added. Include it only in a later requested stock check or outbound preview.
