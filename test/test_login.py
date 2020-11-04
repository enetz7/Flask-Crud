from requests import post


def test_login():
    response=post('http://localhost:5000/login', data=dict(username='Endibra90',password='123456789'))
    assert 'ole' in response.text