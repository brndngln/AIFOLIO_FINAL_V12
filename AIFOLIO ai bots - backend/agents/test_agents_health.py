from agents.adam import handle_adam
from agents.barbara import handle_barbara
from agents.bobby import handle_bobby
from agents.cassie import handle_cassie
from agents.ceevee import handle_ceevee
from agents.emmi import handle_emmi
from agents.victor import handle_victor
from agents.vinnie import handle_vinnie

def test_adam_health():
    resp = handle_adam("Test ad copy", user="test_health")
    assert isinstance(resp, str) and len(resp) > 0
    assert "sentient" not in resp.lower()

def test_barbara_health():
    resp = handle_barbara("Write a blog intro about AI", user="test_health")
    assert isinstance(resp, str) and len(resp) > 0
    assert "sentient" not in resp.lower()

def test_bobby_health():
    resp = handle_bobby("Give me a business growth tip", user="test_health")
    assert isinstance(resp, str) and len(resp) > 0
    assert "sentient" not in resp.lower()

def test_cassie_health():
    resp = handle_cassie("How do I onboard a new client?", user="test_health")
    assert isinstance(resp, str) and len(resp) > 0
    assert "sentient" not in resp.lower()

def test_ceevee_health():
    resp = handle_ceevee("Tips for a standout CV", user="test_health")
    assert isinstance(resp, str) and len(resp) > 0
    assert "sentient" not in resp.lower()

def test_emmi_health():
    resp = handle_emmi("How do I use VLOOKUP?", user="test_health")
    assert isinstance(resp, str) and len(resp) > 0
    assert "sentient" not in resp.lower()

def test_victor_health():
    resp = handle_victor("How to answer a product question?", user="test_health")
    assert isinstance(resp, str) and len(resp) > 0
    assert "sentient" not in resp.lower()

def test_vinnie_health():
    resp = handle_vinnie("How to be a great virtual assistant?", user="test_health")
    assert isinstance(resp, str) and len(resp) > 0
    assert "sentient" not in resp.lower()
