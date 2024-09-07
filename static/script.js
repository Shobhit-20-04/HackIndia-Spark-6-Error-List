document.getElementById('submit-transaction').addEventListener('click', async () => {
    const voterId = document.getElementById('voter_id').value;
    const party = document.getElementById('party').value;

    const response = await fetch('/transactions/new', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ voter_id: voterId, party: party })
    });

    const result = await response.json();
    alert(result.message);

    document.getElementById('voter_id').value = '';
    document.getElementById('party').value = '';
    
    // Fetch and display the current transactions
    fetchCurrentTransactions();
});

async function fetchCurrentTransactions() {
    const response = await fetch('/chain', {
        method: 'GET'
    });

    const result = await response.json();
    const transactions = result.chain[result.chain.length - 1].transactions; // Get transactions from the latest block
    document.getElementById('transactions').innerText = JSON.stringify(transactions, null, 2);
}

// Load the blockchain and transactions when the page is loaded
window.onload = async () => {
    await fetchBlockchain();
    await fetchCurrentTransactions();
};
