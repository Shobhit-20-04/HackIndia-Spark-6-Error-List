import hashlib
import json,os
from time import time
from flask import Flask, jsonify, request,render_template
from flask_cors import CORS

class Vote:
    def _init_(self, voter_id, candidate):
        self.voter_id = voter_id
        self.candidate = candidate
        self.vote_hash = self.create_hash()

    def create_hash(self):
        vote_string = f"{self.voter_id}{self.candidate}".encode()
        return hashlib.sha256(vote_string).hexdigest()

class VotingSystem:
    def _init_(self, storage_file='votes.json'):
        self.storage_file = storage_file
        self.votes = self.load_votes()

    def load_votes(self):
        """Load votes from a JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                votes_data = json.load(file)
                return [Vote(vote['voter_id'], vote['candidate']) for vote in votes_data]
        return []

    def save_votes(self):
        """Save votes to a JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump([{'voter_id': vote.voter_id, 'candidate': vote.candidate, 'vote_hash': vote.vote_hash} for vote in self.votes],file)
class Blockchain:
    def __init__(self):
        self.chain = []
        self.ct = []
        self.nb(previous_hash='1', proof=100)

    def nb(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.ct,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.ct = []
        self.chain.append(block)
        return block

    def new_vote(self, voter_id, party):
        self.ct.append({
            'voter_id': voter_id,
            'party': party,
            'timestamp': time(),
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def checkWork(self, last_proof):
        proof = 0
        while self.checkproof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def checkproof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

app = Flask(__name__)
CORS(app)
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.checkWork(last_proof)

    blockchain.new_vote(
        voter_id="0",
        party="",
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.nb(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_vote():
    values = request.get_json()

    required = ['voter_id', 'party']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_vote(values['voter_id'], values['party'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

def new_vote(self, voter_id, party):
    self.ct.append({
        'voter_id': voter_id,
        'party': party,
        'timestamp': time(),
    })
    return self.last_block['index']+1

@app.route('/chain', methods=['GET'])
def finalChain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
