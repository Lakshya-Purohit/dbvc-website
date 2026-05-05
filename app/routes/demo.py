from flask import Blueprint, render_template

demo_bp = Blueprint("demo", __name__)


@demo_bp.route("/demo", methods=["GET"])
def demo():
    diffs = [
        {
            "type": "tables",
            "name": "users",
            "status": "missing_in_target",
            "source_sql": (
                "CREATE TABLE users (\n"
                "    id SERIAL PRIMARY KEY,\n"
                "    username VARCHAR(50) UNIQUE NOT NULL,\n"
                "    email VARCHAR(100) UNIQUE NOT NULL,\n"
                "    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
                ");"
            ),
            "target_sql": "",
        },
        {
            "type": "tables",
            "name": "orders",
            "status": "modified",
            "source_sql": (
                "CREATE TABLE orders (\n"
                "    id SERIAL PRIMARY KEY,\n"
                "    user_id INTEGER REFERENCES users(id),\n"
                "    total_amount DECIMAL(10, 2) NOT NULL,\n"
                "    status VARCHAR(20) DEFAULT 'pending',\n"
                "    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
                "    shipping_address TEXT\n"
                ");"
            ),
            "target_sql": (
                "CREATE TABLE orders (\n"
                "    id SERIAL PRIMARY KEY,\n"
                "    user_id INTEGER REFERENCES users(id),\n"
                "    total_amount DECIMAL(10, 2) NOT NULL,\n"
                "    status VARCHAR(20) DEFAULT 'pending',\n"
                "    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
                ");"
            ),
        },
        {
            "type": "functions",
            "name": "calculate_order_total",
            "status": "missing_in_target",
            "source_sql": (
                "CREATE OR REPLACE FUNCTION calculate_order_total(order_id INT)\n"
                "RETURNS DECIMAL AS $$\n"
                "BEGIN\n"
                "    RETURN (\n"
                "        SELECT SUM(quantity * unit_price)\n"
                "        FROM order_items\n"
                "        WHERE order_items.order_id = $1\n"
                "    );\n"
                "END;\n"
                "$$ LANGUAGE plpgsql;"
            ),
            "target_sql": "",
        },
        {
            "type": "views",
            "name": "active_users_view",
            "status": "missing_in_target",
            "source_sql": (
                "CREATE OR REPLACE VIEW active_users_view AS\n"
                "SELECT id, username, email\n"
                "FROM users\n"
                "WHERE TRUE;"
            ),
            "target_sql": "",
        },
        {
            "type": "triggers",
            "name": "update_modified_at",
            "status": "modified",
            "source_sql": (
                "CREATE TRIGGER update_modified_at\n"
                "BEFORE UPDATE ON users\n"
                "FOR EACH ROW\n"
                "EXECUTE FUNCTION set_updated_timestamp();"
            ),
            "target_sql": (
                "CREATE TRIGGER update_modified_at\n"
                "BEFORE UPDATE ON users\n"
                "FOR EACH ROW\n"
                "EXECUTE FUNCTION set_modified_timestamp();"
            ),
        },
    ]

    return render_template("demo.html", diffs=diffs)
