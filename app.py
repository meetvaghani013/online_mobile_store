from itertools import product

from flask import Flask, render_template, request, redirect, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import threading, os, time
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = "secret123"

# ================= DATABASE CONFIG =================

basedir = os.path.abspath(os.path.dirname(__file__))

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/check_products")
def check_products():
    products = Product.query.all()
    return str([(product.id, product.name, product.image) for product in products])


# ================= MODELS =================



class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default="user")
    # each user has its own DB
    db_name = db.Column(db.String(100), nullable=False)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    # Basic
    name = db.Column(db.String(100))
    brand = db.Column(db.String(50))
    weight = db.Column(db.Integer)
    color = db.Column(db.String(50))

    # Connectivity
    network = db.Column(db.String(50))
    sim_type = db.Column(db.String(50))
    display = db.Column(db.String(50))

    # Performance
    ram = db.Column(db.String(50))
    storage = db.Column(db.String(50))
    battery = db.Column(db.String(50))

    # Camera
    back_camera = db.Column(db.String(100))
    front_camera = db.Column(db.String(100))

    # Price & Stock
    price = db.Column(db.Integer)
    processor = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    about = db.Column(db.Text)

    image = db.Column(db.String(300))


class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    product_name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    qty = db.Column(db.Integer)


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)

    customer_name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    payment_method = db.Column(db.String(20))
    total = db.Column(db.Integer)

    status = db.Column(db.String(20), default="Not Delivered")
    tracking_id = db.Column(db.String(100))

    delivered_date = db.Column(db.DateTime)
    estimated_delivery = db.Column(db.DateTime)

    # 🔥 NEW
    cancel_reason = db.Column(db.Text)
    cancel_date = db.Column(db.DateTime)

    return_status = db.Column(db.String(50))
    return_reason = db.Column(db.Text)
    return_date = db.Column(db.DateTime)

    order_items = db.relationship("OrderItem", backref="order", lazy=True)


class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    product_brand = db.Column(db.String(100))
    product_name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    product_image = db.Column(db.String(300))


# ================= AUTH =================


@app.route("/")
def index():
    if "username" not in session:
        return redirect("/login")

    if session["role"] != "user":
        return redirect("/admin")

    products = Product.query.all()
    return render_template("index.html", products=products)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # 1. Khali field check
        if not username or not password:
            return jsonify({"success": False, "message": "All fields are required!"})

        # 2. Password match check
        if password != confirm_password:
            return jsonify({"success": False, "message": "Passwords do not match!"})

        # 3. User existence check
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"success": False, "message": "Username already exists!"})

        try:
            # New user save karna
            new_user = User(
                username=username,
                password=password,  # Mashwara: use generate_password_hash(password)
                role="user",
                db_name=f"{username}_db",
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "message": "Database Error occurred!"})

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user_id"] = user.id
            session["role"] = user.role
            session["username"] = user.username
            return redirect("/admin" if user.role == "admin" else "/")
        else:
            return render_template("login.html", error="Invalid Username or Password")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")

    user = User.query.filter_by(username=session["username"]).first()

    orders = Order.query.filter_by(customer_name=user.username).all()

    total_spent = 0
    total_products = 0

    for order in orders:
        # ✅ Sabhi orders ke liye total_amount calculate hoga (display ke liye)
        order.total_amount = sum(item.price * item.qty for item in order.order_items)

        # ✅ Sirf Delivered orders stats me count honge
        if order.status == "Delivered":
            total_spent += order.total_amount
            total_products += sum(item.qty for item in order.order_items)

    pending_orders = Order.query.filter_by(
        customer_name=user.username, status="Ordered"
    ).count()

    delivered_orders = Order.query.filter_by(
        customer_name=user.username, status="Delivered"
    ).count()

    cancelled_orders = Order.query.filter_by(
        customer_name=user.username, status="Cancelled"
    ).count()

    returned_orders = Order.query.filter_by(
        customer_name=user.username, status="Return"
    ).count()

    recent_orders = (
        Order.query.filter_by(customer_name=user.username)
        .order_by(Order.id.desc())
        .limit(10)
        .all()
    )

    return render_template(
        "profile_dashboard.html",
        user=user,
        total_products=total_products,
        total_spent=total_spent,
        cancelled_orders=cancelled_orders,
        returned_orders=returned_orders,
        pending_orders=pending_orders,
        delivered_orders=delivered_orders,
        recent_orders=recent_orders,
    )


@app.route("/change-password", methods=["GET", "POST"])
def change_password():

    if "username" not in session:
        return redirect("/login")

    user = User.query.filter_by(username=session["username"]).first()

    if request.method == "POST":

        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if user.password != old_password:
            return jsonify({"status": "error", "message": "Old password incorrect"})

        if new_password != confirm_password:
            return jsonify({"status": "error", "message": "Passwords do not match"})

        if len(new_password) < 4:
            return jsonify(
                {"status": "error", "message": "Minimum 4 characters required"}
            )

        user.password = new_password
        db.session.commit()

        return jsonify(
            {"status": "success", "message": "Password changed successfully"}
        )

    return render_template("change_password.html", username=session["username"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ================= CART =================


@app.route("/add/<int:pid>")
def add_to_cart(pid):
    if "user_id" not in session:
        return redirect("/login")

    product = Product.query.get(pid)

    cart_item = Cart.query.filter_by(user_id=session["user_id"], product_id=pid).first()

    if cart_item:
        cart_item.qty += 1
    else:
        cart_item = Cart(
            user_id=session["user_id"],
            product_id=product.id,
            product_name=product.name,
            price=product.price,
            qty=1,
        )
        db.session.add(cart_item)

    db.session.commit()
    return redirect("/")


@app.route("/cart")
def cart():
    if "user_id" not in session:
        return redirect("/login")

    cart_items = Cart.query.filter_by(user_id=session["user_id"]).all()

    items = []
    total = 0
    stock_error = False

    for item in cart_items:
        product = Product.query.get(item.product_id)

        if item.qty > product.quantity:
            stock_error = True

        sub = item.price * item.qty
        total += sub
        items.append((product, item.qty, sub))

    return render_template(
        "cart.html", items=items, total=total, stock_error=stock_error
    )


@app.route("/update_qty/<int:pid>/<action>")
def update_qty(pid, action):

    if "user_id" not in session:
        return redirect("/login")

    cart_item = Cart.query.filter_by(user_id=session["user_id"], product_id=pid).first()

    product = Product.query.get(pid)

    if cart_item and product:

        if action == "plus":
            if cart_item.qty < product.quantity:
                cart_item.qty += 1
            else:
                flash(f"Only {product.quantity} items available in stock!", "error")

        elif action == "minus":
            cart_item.qty -= 1
            if cart_item.qty <= 0:
                db.session.delete(cart_item)

        db.session.commit()

    return redirect("/cart")


@app.route("/remove/<int:pid>")
def remove(pid):

    cart_item = Cart.query.filter_by(user_id=session["user_id"], product_id=pid).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()

    return redirect("/cart")


# ================= PURCHASE FULL CART =================


@app.route("/purchase")
def purchase():

    if "user_id" not in session:
        return redirect("/login")

    cart_items = Cart.query.filter_by(user_id=session["user_id"]).all()

    if not cart_items:
        flash("Your cart is empty!", "error")
        return redirect("/cart")

    items = []
    total = 0

    for item in cart_items:
        product = Product.query.get(item.product_id)

        if not product:
            flash("Product not found!", "error")
            return redirect("/cart")

        if item.qty > product.quantity:
            flash(
                f"{product.brand} {product.name} has only {product.quantity} items available!",
                "error",
            )
            return redirect("/cart")

        if product.quantity <= 0:
            flash(f"{product.brand} {product.name} is out of stock!", "error")
            return redirect("/cart")

        sub = product.price * item.qty
        total += sub
        items.append((product, item.qty, sub))

    return render_template("purchase.html", items=items, total=total)


# ================= PURCHASE SINGLE =================


@app.route("/purchase_single/<int:pid>")
def purchase_single(pid):

    if "user_id" not in session:
        return redirect("/login")

    cart_item = Cart.query.filter_by(user_id=session["user_id"], product_id=pid).first()

    product = Product.query.get(pid)

    if not cart_item or not product:
        flash("Item not found!", "error")
        return redirect("/cart")

    if cart_item.qty > product.quantity:
        flash(f"Only {product.quantity} items available!", "error")
        return redirect("/cart")

    if product.quantity <= 0:
        flash("Product out of stock!", "error")
        return redirect("/cart")

    sub = product.price * cart_item.qty

    return render_template(
        "purchase.html", items=[(product, cart_item.qty, sub)], total=sub
    )


# ================= CONFIRM PURCHASE =================


@app.route("/confirm_purchase", methods=["POST"])
def confirm_purchase():

    if "user_id" not in session:
        return redirect("/login")

    payment = request.form.get("payment")
    single_pid = request.form.get("single_pid")

    items = []
    total = 0

    # ================= SINGLE PURCHASE =================
    if single_pid:

        qty = int(request.form.get("single_qty", 1))
        product = Product.query.get(int(single_pid))

        if not product:
            flash("Product not found!", "error")
            return redirect("/cart")

        if product.quantity <= 0:
            flash("Product is out of stock!", "error")
            return redirect("/cart")

        if qty > product.quantity:
            flash(f"Only {product.quantity} items available!", "error")
            return redirect("/cart")

        sub = product.price * qty
        total = sub
        items.append((product, qty, sub))

    # ================= FULL CART =================
    else:

        cart_items = Cart.query.filter_by(user_id=session["user_id"]).all()

        if not cart_items:
            flash("Cart is empty!", "error")
            return redirect("/cart")

        for item in cart_items:

            product = Product.query.get(item.product_id)

            if not product:
                flash("Product not found!", "error")
                return redirect("/cart")

            if product.quantity <= 0:
                flash(f"{product.name} is out of stock!", "error")
                return redirect("/cart")

            if item.qty > product.quantity:
                flash(
                    f"{product.name} has only {product.quantity} items available!",
                    "error",
                )
                return redirect("/cart")

            sub = product.price * item.qty
            total += sub
            items.append((product, item.qty, sub))

    # ================= ORDER CREATE =================

    tracking_id = "TRK-" + uuid.uuid4().hex[:8].upper()
    estimated_delivery = datetime.now() + timedelta(days=3)

    new_order = Order(
        customer_name=session["username"],
        address=request.form.get("address"),
        phone=request.form.get("phone"),
        payment_method=payment,
        total=total,
        tracking_id=tracking_id,
        estimated_delivery=estimated_delivery,
        status="Ordered",
    )

    db.session.add(new_order)
    db.session.commit()

    # ================= SAVE ITEMS + REDUCE STOCK =================

    for product, qty, sub in items:

        product.quantity -= qty  # reduce stock

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            product_name=product.name,
            product_brand=product.brand,
            price=product.price,
            qty=qty,
            product_image=product.image,
        )

        db.session.add(order_item)

    # ================= CLEAR CART =================

    if single_pid:
        Cart.query.filter_by(
            user_id=session["user_id"], product_id=int(single_pid)
        ).delete()
    else:
        Cart.query.filter_by(user_id=session["user_id"]).delete()

    db.session.commit()

    return render_template("thankyou.html", order=new_order, items=items, total=total)


@app.route("/track/<tracking_id>")
def track_order(tracking_id):

    order = Order.query.filter_by(tracking_id=tracking_id).first()

    if not order:
        return render_template("track.html", order=None)

    return render_template("track.html", order=order)


@app.route("/track_search", methods=["POST"])
def track_search():
    tracking_id = request.form.get("tracking_id")
    return redirect(f"/track/{tracking_id}")


# ================= ADMIN =================


@app.route("/admin")
def admin_dashboard():
    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    total_products = Product.query.count()

    total_users = User.query.filter(User.role != "admin").count()

    total_orders = Order.query.count()

    pending_orders = Order.query.filter_by(status="Ordered").count()

    delivered_orders = Order.query.filter_by(status="Delivered").count()
    return_orders = Order.query.filter_by(status="Return").count()
    cancelled_orders = Order.query.filter_by(status="Cancelled").count()

    # Profit = sum of delivered orders only
    total_profit = (
        db.session.query(db.func.sum(Order.total))
        .filter_by(status="Delivered")
        .scalar()
        or 0
    )

    return render_template(
        "admin/dashboard.html",
        total_products=total_products,
        total_users=total_users,
        total_orders=total_orders,
        pending_orders=pending_orders,
        delivered_orders=delivered_orders,
        total_profit=total_profit,
        return_orders=return_orders,
        cancelled_orders=cancelled_orders
    )


@app.route("/admin/products")
def admin_products():
    products = Product.query.all()
    return render_template("admin/products.html", products=products)


@app.route("/admin/add_product", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        image_file = request.files["image"]

        filename = None
        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            import uuid

            unique_name = str(uuid.uuid4()) + "_" + filename
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
            image_file.save(save_path)
            image_db_path = "images/" + unique_name

        new_product = Product(
            name=request.form.get("name"),
            brand=request.form.get("brand"),
            weight=request.form.get("weight"),
            color=request.form.get("color"),
            network=request.form.get("network"),
            sim_type=request.form.get("sim_type"),
            display=request.form.get("display"),
            ram=request.form.get("ram"),
            storage=request.form.get("storage"),
            battery=request.form.get("battery"),
            back_camera=request.form.get("back_camera"),
            front_camera=request.form.get("front_camera"),
            price=request.form.get("price"),
            processor=request.form.get("processor"),
            quantity=request.form.get("quantity"),
            about=request.form.get("about"),
            image=image_db_path,
        )

        db.session.add(new_product)
        db.session.commit()

        return redirect("/admin/products")

    return render_template("admin/add_product.html")


@app.route("/admin/edit_product/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    product = Product.query.get_or_404(id)

    if request.method == "POST":

        product.name = request.form.get("name")
        product.brand = request.form.get("brand")
        product.weight = request.form.get("weight")
        product.color = request.form.get("color")
        product.price = request.form.get("price")
        product.ram = request.form.get("ram")
        product.storage = request.form.get("storage")
        product.battery = request.form.get("battery")
        product.processor = request.form.get("processor")
        product.network = request.form.get("network")
        product.sim_type = request.form.get("sim_type")
        product.display = request.form.get("display")
        product.back_camera = request.form.get("back_camera")
        product.front_camera = request.form.get("front_camera")
        product.quantity = request.form.get("quantity")
        product.about = request.form.get("about")

        image_file = request.files.get("image")

        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            import uuid

            unique_name = str(uuid.uuid4()) + "_" + filename
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
            image_file.save(save_path)
            product.image = "images/" + unique_name

        db.session.commit()
        return redirect("/admin/products")

    return render_template("admin/edit_product.html", product=product)


@app.route("/admin/update_order/<int:id>", methods=["POST"])
def update_order(id):

    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    order = Order.query.get_or_404(id)
    new_status = request.form.get("status")

    order.status = new_status

    if new_status == "Shipped":
        thread = threading.Thread(target=auto_update_status, args=(order.id,))
        thread.start()

    if new_status == "Delivered":
        if not order.delivered_date:
            order.delivered_date = datetime.now()

    db.session.commit()

    # Delivered logic
    if new_status == "Delivered":

        if not order.tracking_id:
            import uuid

            order.tracking_id = "TRK-" + uuid.uuid4().hex[:8].upper()

        if not order.delivered_date:
            order.delivered_date = datetime.now()

    db.session.commit()
    return redirect("/admin/orders")


def auto_update_status(order_id):

    time.sleep(60)  # 1 minute

    with app.app_context():
        order = Order.query.get(order_id)
        if order and order.status == "Shipped":
            order.status = "Out for Delivery"
            db.session.commit()

    time.sleep(60)  # another 1 minute

    with app.app_context():
        order = Order.query.get(order_id)
        if order and order.status == "Out for Delivery" and not order.return_status:
            order.status = "Delivered"
            order.delivered_date = datetime.now()
            db.session.commit()


@app.route("/admin/delivered_orders")
def admin_delivered_orders():
    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    # Show only delivered orders
    orders = Order.query.filter(Order.status != "Ordered", Order.status != "Cancelled", Order.status != "Return").all()
    return render_template("admin/delivered_orders.html", orders=orders)


@app.route("/admin/return-orders")
def admin_return_orders():

    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    orders = (
        Order.query.filter_by(status="Return").order_by(Order.id.desc()).all()
    )

    return render_template("admin/return_orders.html", orders=orders)


@app.route("/admin/cancel-orders")
def admin_cancel_orders():

    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    orders = Order.query.filter_by(status="Cancelled") \
                .order_by(Order.id.desc()).all()

    return render_template("admin/cancel_orders.html", orders=orders)

@app.route("/my_orders")
def my_orders():
    orders = Order.query.filter_by(customer_name=session["username"]).all()

    return render_template("my_orders.html", orders=orders)


@app.route("/cancel-order/<int:order_id>", methods=["GET", "POST"])
def cancel_order(order_id):

    if "username" not in session:
        return redirect("/login")

    order = Order.query.get_or_404(order_id)

    if request.method == "POST":

        if order.status not in ["Ordered", "Shipped"]:
            return redirect("/my_orders")

        reason = request.form.get("reason")

        order.status = "Cancelled"
        order.cancel_reason = reason
        order.cancel_date = datetime.now()

        db.session.commit()

        return redirect("/my_orders")

    return render_template("cancel_order.html", order=order)


@app.route("/return-order/<int:order_id>", methods=["GET", "POST"])
def return_order(order_id):

    if "username" not in session:
        return redirect("/login")

    order = Order.query.get_or_404(order_id)

    if request.method == "POST":

        if order.status.strip() != "Delivered":
            flash("Return allowed only for delivered orders", "danger")
            return redirect("/my_orders")

        if order.return_status:
            flash("Return already requested", "warning")
            return redirect("/my_orders")

        try:
            reason = request.form.get("reason")
            extra = request.form.get("extra_reason")

            full_reason = reason
            if extra:
                full_reason += " - " + extra

            order.status = "Return"
            order.return_status = "Return Requested"
            order.return_reason = full_reason
            order.return_date = datetime.now()

            for item in order.order_items:
                product = Product.query.get(item.product_id)
                if product:
                    product.quantity += item.qty

            db.session.commit()

            flash("Return Request Submitted Successfully", "success")

        except Exception as e:
            db.session.rollback()
            print("RETURN ERROR:", e)

        return redirect("/my_orders")

    return render_template("return_order.html", order=order)


@app.route("/admin/delete_product/<int:id>")
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect("/admin/products")


@app.route("/admin/orders")
def admin_orders():
    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    # Only show pending orders
    orders = Order.query.filter(Order.status == "Ordered").all()

    return render_template("admin/orders.html", orders=orders)


@app.route("/admin/users")
def admin_users():
    users = User.query.all()
    return render_template("admin/users.html", users=users)


@app.route("/admin/delete_user/<int:id>")
def delete_user(id):
    user = User.query.get_or_404(id)

    # Don't delete admin
    if user.role == "admin":
        return redirect("/admin/users")

    db.session.delete(user)
    db.session.commit()

    return redirect("/admin/users")

@app.route("/about")
def about():
    return render_template("about.html")


# ================= DATABASE INIT =================
with app.app_context():

    db.create_all()

    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            password="1234",
            role="admin",
            db_name="admin_db"
        )
        db.session.add(admin)

    if not User.query.filter_by(username="user").first():
        user = User(
            username="user",
            password="1234",
            role="user",
            db_name="user_db"
        )
        db.session.add(user)

    db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
