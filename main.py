from textwrap import dedent
from flask import Flask
from uuid import uuid4
from blockchain import Blockchain

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()
