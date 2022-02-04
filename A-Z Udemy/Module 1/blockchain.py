# Module 1 - Create a Blockchain

import datetime
import hashlib
import json
from flask import Flask, jsonify


class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')
        
    # Adds a new block after it is mined
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            # 'data':         
        }
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
    
blockchain = Blockchain()


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home_page():
    return 'Welcome to TogeCoin\'s server'

@app.route('/mine-block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_last_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
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

app.run(host='0.0.0.0', port=5000)