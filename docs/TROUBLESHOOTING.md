# Troubleshooting

This is a small list of some of the problems you could run into while working on spaceshare.


#### If you're on OSX you might find that the virtualenv needs python 2.7.9 and not 2.7.6 because of the built in python version. This is something that can be really frustrating if you don't have some good shell knowledge.
```shell
virtualenv venv -p /usr/local/bin/python
```

## can't import celery?

I frequently had this weird irritating problem after having set up the Muse for development on my machine.

```Python
(venv)➜  spaceshare git:(master) ✗ make run
python spaceshare/__init__.py
INFO:werkzeug: * Running on http://127.0.0.1:4000/ (Press CTRL+C to quit)
INFO:werkzeug: * Restarting with stat
INFO:werkzeug: * Detected change in '/Users/david/Code/spaceshare/spaceshare/__init__.py', reloading
INFO:werkzeug: * Restarting with stat
Traceback (most recent call last):
  File "spaceshare/__init__.py", line 3, in <module>
    from tasks import print_words
  File "/Users/david/Code/spaceshare/spaceshare/tasks.py", line 3, in <module>
    from celery import Celery
  File "/Users/david/Code/spaceshare/venv/lib/python2.7/site-packages/celery/__init__.py", line 130, in <module>
    from celery import five
  File "/Users/david/Code/spaceshare/venv/lib/python2.7/site-packages/celery/five.py", line 51, in <module>
    from kombu.five import monotonic
  File "/Users/david/Code/spaceshare/venv/lib/python2.7/site-packages/kombu/five.py", line 52, in <module>
    libSystem = ctypes.CDLL('libSystem.dylib')
  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/ctypes/__init__.py", line 365, in __init__
    self._handle = _dlopen(self._name, mode)
OSError: dlopen(libSystem.dylib, 6): image not found
make: *** [run] Error 1
(venv)➜  spaceshare git:(master) ✗ unset DYLD_FALLBACK_LIBRARY_PATH
```


## getting weird traffic on port 5000
I would sometimes get weird traffic while building this on my own machine, it turned out that it was my apple magic trackpad, which sends random information to port 5000.

This is nothing to worry about but if you like of course you can simply change the port of the flask server in.  

```python
if __name__ == '__main__':
    app.run(
        debug=config['DEBUG'],
        use_reloader=True,
        threaded=True,
        port=4000
        )

```
