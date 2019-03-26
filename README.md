# ![alt text](https://assets.breatheco.de/apis/img/images.php?blob&random&cat=icon&tags=breathecode,32) Flask

To install Flask in C9:

First: Make sure you're using Python 3.6.6 of newer:
  
  ```pyenv install 3.6.6``` This could take a while
  
  ```pyenv global 3.6.6```

1. Run the install command:
  
  ```sudo pip install Flask```

2. Create a file, (```app.py```). Do not use flask.py, it can generate conflicts with the flask application.

3. Paste this code into ```app.py```:
  
```python
import os
from flask import Flask, jsonify
  
app = Flask(__name__)
  
@app.route('/')
def hello():
    return jsonify({ "hello": "World" })
  
  
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
```
  
This code configures the ```'/'``` endpoint (*https://your_c9_url/*), and returns a string

4. Click ```run```, C9 top bar. Remember to have the file opened. Alternatively you can run ```python app.py``` in your terminal to run the server manually.

5. *voilá*, backend server running.

## (Optional) Expanding your API

#### To enable CORS
  
1. Run: ```sudo pip install -U flask-cors```
2. Copy this into your `app.py` file:
    ```python
      
    #imports and stuff above this comment
      
    # Don't repeat this line in the code
    app = Flask(__name__)
      
    # Possible code
    CORS(app)
      
    #routes and stuff below
      
    ```

#### Awesome Documentation for your API
  
https://github.com/gangverk/flask-swagger