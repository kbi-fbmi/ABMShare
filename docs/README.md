# abmShareDoc

## For initialize you have to create virtual environment
For creating venv run in shell ```python3 -m venv .venv``` and activate the virtual env on<br>
Windows```.venv/Scripts/Activate``` <br> 
Mac/Linux ```source .venv/bin/activate ``` <br>
Next step is to install dependencies by ```pip install -r requirements.txt```

## Running version for develop
In root folder (where ***mkdocs.yml*** is) run ```mkdocs serve``` In terminal you can see address to access the served documenatation on your local host. If the port is already taken, look for [MkDocs documentation](https://www.mkdocs.org/).

## Building website
Build a website with ```mkdocs build``` After build the content of **site** folder is prepared to be uploaded in www/

