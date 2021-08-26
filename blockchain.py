import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests

# TODO include previous hash in next block's proof, something the guide writer did not think about.

# class definiton created with base structure from Learn Blockchains by Building One, (van Flymen, 2017).

class Blockchain:

    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.nodes = set()

        self.new_block(previous_hash = 1, proof = 100)
    
    def register_node(self, node_address):
        parsed_url = urlparse(node_address)
        self.nodes.add(parsed_url.netloc)
    
    def valid_chain(self, chain):
        
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print('\n----------\n')
            if block['previous_hash'] != self.hash(last_block):
                return False
            
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            
            last_block = block
            current_index += 1
        
        return True
    
    def resolve_conflicts(self):
        # definition of consensus algorithm TODO Edit this to make it optimal

        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True
        
        return False
    
    def new_block(self, proof, previous_hash = None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash,
        }

        self.current_transactions = []
        self.chain.append(block)

        return block

    def new_transactions(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        proof = 0

        # including the last block's transactions in the proof of the next block to ensure immutability. 
        while self.valid_proof(last_proof, proof, Blockchain.hash(self.chain[-1])) is False:
            proof += 1

        return proof

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def valid_proof(last_proof, proof, last_block_hash=None):
        guess = f'{last_proof}{proof}{last_block_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:5] == "00000"

    @property
    def last_block(self):
        return self.chain[-1]
