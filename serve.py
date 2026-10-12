"""Minimal Flask service for later course units."""
from flask import Flask, jsonify, request
from agent import run_agent
from utils.data_loader import get_example_wardrobe
app=Flask(__name__)
@app.get('/health')
def health(): return jsonify({"ok":True})
@app.post('/ask')
def ask():
    q=(request.get_json(silent=True) or {}).get('query','')
    return jsonify(run_agent(q,get_example_wardrobe()))
if __name__=='__main__': app.run(port=5000)
