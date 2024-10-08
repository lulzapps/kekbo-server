# Running

## Windows

* Install Python 3.12.6 oir higher and make sure Python is in your PATH.
* Checkout the code `git clone <repo>`
* `cd kekbo-serv`
* Create a virtual Python environment: `python3.12 -m venv <virtual-env-folder>` (i.e. `py_win`)

* Depending on your system, you may have to allow PowerShel to run PowerScripts:
```ps
Set-ExecutionPolicy -ExecutionPolicy Unrestricted
```

* Activate the virtual Python environment: `./<virtual-en-folder>/Scripts/Activate.ps1`
* Install dependencies: `pip install -r requirements.txt`

Now you're ready to start and stop the `kekbosrv.py` script as needed. There are two main ways to do: 

#### The Normal Python-like Way
```bash
python kekbosrv.py
```

The problem with this way is that I have yet to find a way to pass in the `log-level` and see it get adjusted on the output. For example, `python kekbosrv.py --log-level debug` still only shows `INFO` logs (and above)

#### Using Uvicorn

As I write this `uvicorn` "just works" in my environment after I load up the Python virtual environment (it's listed in `requirements.txt`). Using `uvicorn` I am able to adjust the log levels:
```bash
uvicorn kekbosrv:app --log-level debug
```

