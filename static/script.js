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
});

document.getElementById('mine-block').addEventListener('click', async () => {
    const response = await fetch('/mine', {
        method: 'GET'
    });

    const result = await response.json();
    alert(result.message);
    fetchBlockchain();
});

async function fetchBlockchain() {
    const response = await fetch('/chain', {
        method: 'GET'
    });

    const result = await response.json();
    document.getElementById('blockchain').innerText = JSON.stringify(result.chain, null, 2);
}

// Load the blockchain when the page is loaded
window.onload = fetchBlockchain;
