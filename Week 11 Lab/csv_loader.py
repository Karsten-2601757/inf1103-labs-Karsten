import csv
from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier
def load_products(path: str, inventory: Inventory, supplier: Supplier) -> int:
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for row in reader:
                try:
                    if len(row) not in (5, 6):
                        raise ValueError("expected 5 or 6 columns")
                    product_type, product_id, name, price, stock = row[:5]
                    extra = float(row[5]) if len(row) == 6 else 0.0
                    product = ProductFactory.create(
                        product_type.strip().lower(), product_id.strip(),
                        name.strip(), float(price), int(stock), supplier, extra)
                    if not inventory.add_product(product):
                        raise ValueError(f"duplicate product ID {product_id}")
                    loaded += 1
                except ValueError as error:
                    print(f"Skipping row {row}: {error}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
    return loaded