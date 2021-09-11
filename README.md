# monte-carlo-stock-api

This is a REST API made with flask and flask-restful/Swagger. 

It takes a number of user defined parameters and generates fake but realistic looking stock price trajectories for a given number of periods. In each period, a price is generated for a given number of steps, then the OHLC stats are calculated and added to the trajectory. Multiple repeats of a trajectory can be generated as well.

Requirements:

flask
flask-restful
numpy

Clone/download the repository, then go to the root directory and run the `./start.sh` script in a terminal. 

Then go to [localhost:5000](http://127.0.0.1:5000/) in your browser to see the Swagger documentation. On this page you can try the API out. If you leave a value blank/undefined, the following defaults will be used:

```python
no_periods = 50
len_periods = 50
mean = 0.0001
std = 0.001
start_price = 10.0
repeats = 1
```

MIT license (see LICENSE.txt)