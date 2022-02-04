import datetime
from fnmatch import translate
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse
import sys

port = sys.argv[1]
miner = sys.argv[2]

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.mempool = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()
        
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    # adds a new block after it is mined
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.mempool
        }
        self.mempool = []
        self.chain.append(block)
        return block
    
    def get_last_block(self):
        return self.chain[-1]
    
    def check_proof(self, proof, previous_proof):
        hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
        if hash_operation[:4] == '0000':
            return True
        else:
            return False
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        while True:
            if self.check_proof(new_proof, previous_proof):
                return new_proof
            new_proof = new_proof + 1
            
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            current_proof = block['proof']
            if self.check_proof(current_proof, previous_proof) is False:
                return False
            block_index = block_index + 1
            previous_block = block
        return True

    def add_transaction(self, sender, receiver, amount):
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        }
        self.mempool.append(transaction)
        previous_block = self.get_last_block()
        return previous_block['index'] + 1

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get-chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
    
blockchain = Blockchain()


app = Flask(__name__)

# address for node on port :5000
node_address = str(uuid4()).replace('-', '')

@app.route('/', methods=['GET'])
def home_page():
    return "Welcome to MeCoin\'s server"

@app.route('/transactions/add', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in json for key in transaction_keys):
        return "Incomplete transaction request", 400
    index = blockchain.add_transaction(
        json['sender'],
        json['receiver'],
        json['amount']
    )
    response = {
        'message': f"This transaction will be added to block #{index}"
    }
    return jsonify(response), 201

@app.route('/mine-block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_last_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address, receiver=miner, amount=1)
    blockchain.create_block(proof, previous_hash)
    block = blockchain.get_last_block()
    response = {
        'message': "Congratulations! You just mined a block.",
        'block': block
    }
    return jsonify(response), 201

@app.route('/get-chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/verify-chain', methods=['GET'])
def verify_chain():
    response = {
        'is_valid': blockchain.is_chain_valid(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/connect-node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {
        'message': "Nodes have been added to the network",
        'nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201

@app.route('/replace-chain', methods=['GET'])
def replace_chain():
    chain_replaced = blockchain.replace_chain()
    if chain_replaced:
        return jsonify({'message': "Chain replaced with the longest one in the network"}), 201
    else:
        return jsonify({'message': "The chain is the longest in the network"}), 200

app.run(host='0.0.0.0', port=port)