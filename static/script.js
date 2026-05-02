window.onload = loadExpenses;

function loadExpenses() {
    fetch("/get_expenses")
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("expense-list");
            list.innerHTML = "";

            data.forEach(exp => {
                list.innerHTML += `
                    <div class="expense">
                        ${exp.title} - ₹${exp.amount} (${exp.category})
                        <button onclick="deleteExpense(${exp.id})">Delete</button>
                    </div>
                `;
            });
        });
}

function addExpense() {
    const title = document.getElementById("title").value;
    const amount = document.getElementById("amount").value;
    const category = document.getElementById("category").value;

    fetch("/add_expense", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ title, amount, category })
    })
    .then(() => {
        loadExpenses();

        document.getElementById("title").value = "";
        document.getElementById("amount").value = "";
        document.getElementById("category").value = "";
    });
}

function deleteExpense(id) {
    fetch(`/delete_expense/${id}`, {
        method: "DELETE"
    })
    .then(() => loadExpenses());
}