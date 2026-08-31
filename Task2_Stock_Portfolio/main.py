import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

# Predefined hardcoded stock prices (Fallback/Mock Data)
MOCK_STOCK_PRICES = {
    "AAPL": 180.50,
    "TSLA": 240.20,
    "MSFT": 415.00,
    "GOOGL": 175.80,
    "AMZN": 185.30,
    "NVDA": 120.40,
    "META": 500.60,
    "NFLX": 640.10,
}

DATA_FILE = "portfolio.json"


class StockPortfolioTracker:

    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        self.root.geometry("600x650")
        self.root.minsize(550, 500)
        self.root.configure(bg="#0f172a")

        self.portfolio = self.load_portfolio()
        self.create_widgets()
        self.update_portfolio_table()

    def load_portfolio(self):
        """Loads saved portfolio data from a JSON file."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_portfolio(self):
        """Saves current portfolio data to a JSON file."""
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(self.portfolio, f, indent=4)
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save portfolio: {e}")

    def create_widgets(self):
        # 1. Header
        header = tk.Label(
            self.root,
            text="📈 Stock Portfolio Tracker",
            font=("Arial", 16, "bold"),
            bg="#1e293b",
            fg="#f8fafc",
            pady=12,
        )
        header.pack(side="top", fill="x")

        # 2. Input Frame (Add/Update Stock)
        input_frame = tk.LabelFrame(
            self.root,
            text=" Add or Update Stock ",
            font=("Arial", 10, "bold"),
            bg="#1e293b",
            fg="#94a3b8",
            padx=15,
            pady=10,
            relief="solid",
            bd=1,
        )
        input_frame.pack(side="top", fill="x", padx=15, pady=10)

        # Stock Symbol Input
        tk.Label(
            input_frame,
            text="Symbol:",
            font=("Arial", 10),
            bg="#1e293b",
            fg="#f8fafc",
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.symbol_entry = tk.Entry(
            input_frame, font=("Arial", 10), width=10, justify="center"
        )
        self.symbol_entry.grid(row=0, column=1, padx=5, pady=5)

        # Quantity Input
        tk.Label(
            input_frame,
            text="Quantity:",
            font=("Arial", 10),
            bg="#1e293b",
            fg="#f8fafc",
        ).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.quantity_entry = tk.Entry(
            input_frame, font=("Arial", 10), width=10, justify="center"
        )
        self.quantity_entry.grid(row=0, column=3, padx=5, pady=5)

        # Add Button
        add_btn = tk.Button(
            input_frame,
            text="Add / Update",
            font=("Arial", 10, "bold"),
            bg="#22c55e",
            fg="white",
            activebackground="#16a34a",
            activeforeground="white",
            relief="flat",
            command=self.add_stock,
            padx=10,
            cursor="hand2",
        )
        add_btn.grid(row=0, column=4, padx=10, pady=5)

        # 3. Portfolio Table (Treeview)
        table_frame = tk.Frame(self.root, bg="#0f172a")
        table_frame.pack(side="top", fill="both", expand=True, padx=15, pady=5)

        columns = ("symbol", "quantity", "price", "total_val")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=8
        )

        # Styling Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#1e293b",
            foreground="#f8fafc",
            rowheight=25,
            fieldbackground="#1e293b",
            font=("Arial", 10),
        )
        style.configure(
            "Treeview.Heading",
            background="#334155",
            foreground="#f8fafc",
            font=("Arial", 10, "bold"),
        )
        style.map("Treeview", background=[("selected", "#3b82f6")])

        self.tree.heading("symbol", text="Stock Symbol")
        self.tree.heading("quantity", text="Shares Owned")
        self.tree.heading("price", text="Price / Share ($)")
        self.tree.heading("total_val", text="Total Value ($)")

        self.tree.column("symbol", anchor="center", width=120)
        self.tree.column("quantity", anchor="center", width=120)
        self.tree.column("price", anchor="center", width=130)
        self.tree.column("total_val", anchor="center", width=140)

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # 4. Remove Stock Button
        remove_btn = tk.Button(
            self.root,
            text="Remove Selected Stock",
            font=("Arial", 10, "bold"),
            bg="#ef4444",
            fg="white",
            activebackground="#dc2626",
            activeforeground="white",
            relief="flat",
            command=self.remove_stock,
            padx=10,
            pady=3,
            cursor="hand2",
        )
        remove_btn.pack(side="top", anchor="e", padx=15, pady=5)

        # 5. Summary Dashboard Footer
        summary_frame = tk.Frame(self.root, bg="#1e293b", pady=15, padx=15)
        summary_frame.pack(side="bottom", fill="x")

        self.total_val_label = tk.Label(
            summary_frame,
            text="Total Investment Value: $0.00",
            font=("Arial", 13, "bold"),
            bg="#1e293b",
            fg="#38bdf8",
        )
        self.total_val_label.pack()

    def add_stock(self):
        symbol = self.symbol_entry.get().strip().upper()
        quantity_str = self.quantity_entry.get().strip()

        if not symbol or not quantity_str:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Input Error", "Quantity must be a positive integer."
            )
            return

        # Check if stock exists in mock database
        if symbol not in MOCK_STOCK_PRICES:
            messagebox.showinfo(
                "Stock Not Found",
                f"'{symbol}' is not in the system. Available mock symbols:\n"
                + ", ".join(MOCK_STOCK_PRICES.keys()),
            )
            return

        # Save or update portfolio
        self.portfolio[symbol] = quantity
        self.save_portfolio()
        self.update_portfolio_table()

        # Clear entries
        self.symbol_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

    def remove_stock(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(
                "Selection Error",
                "Please select a stock from the list to remove.",
            )
            return

        item_values = self.tree.item(selected_item, "values")
        symbol = item_values[0]

        if symbol in self.portfolio:
            del self.portfolio[symbol]
            self.save_portfolio()
            self.update_portfolio_table()

    def update_portfolio_table(self):
        # Clear existing table items
        for item in self.tree.get_children():
            self.tree.delete(item)

        total_portfolio_value = 0.0

        for symbol, qty in self.portfolio.items():
            price = MOCK_STOCK_PRICES.get(symbol, 0.0)
            total_val = price * qty
            total_portfolio_value += total_val

            self.tree.insert(
                "",
                "end",
                values=(symbol, qty, f"${price:,.2f}", f"${total_val:,.2f}"),
            )

        self.total_val_label.config(
            text=f"Total Investment Value: ${total_portfolio_value:,.2f}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = StockPortfolioTracker(root)
    root.mainloop()
