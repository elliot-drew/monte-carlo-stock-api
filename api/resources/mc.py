import numpy as np 

def makeHistory(mean, std, start_price, no_periods, len_periods, repeats):

	history = []
	current_price = start_price
	for r in range(0, repeats):
		tmp_history = []
		for i in range(0, no_periods):
			period_tmp = []
			for j in range(0, len_periods):
				new_price = projectPrice(mean, std, current_price)
				current_price = new_price
				period_tmp.append(current_price)

			o = period_tmp[0]
			c = period_tmp[-1]
			h = np.max(period_tmp)
			l = np.min(period_tmp)

			tmp_history.append({
				"o": o,
				"c": c,
				"h": h,
				"l": l
				})

		history.append(tmp_history)


	return(history)

def projectPrice(mean, std, current_price):

	rng = np.random.default_rng()

	drift = mean - (std * std) / 2
	random_shock = std * rng.normal()

	current_price = current_price * np.exp(drift + random_shock)

	# pulls value back to mean - like a spring, force stronger further it gets
	mean_reversion = current_price*((1-mean/current_price))*rng.normal()*0.01
	
	price = current_price - mean_reversion

	return(price)

