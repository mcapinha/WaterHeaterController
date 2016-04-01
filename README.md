# WaterHeaterController #
Control a water heater based on its temperature

![Alt text](images/sketch.png?raw=true "Sketch")

## Description ##

Using a Raspberry Pi, an Adafruit T-Cobbler, a MCP3008 , a TMP36, a relay board and some Python, control an appliance's power supply based on input temperature.


## What you get ##

Inside the package you'll find:
- a sketch detailing the circuit
- Python code to:
   - Log the current temperature input
   - Plot it to http://www.plot.ly
   - Control the relay (open or close) based on the temperature

## But why ?? ##

At my home I use an electric water heater that is controlled by a thermostat.

I wanted to have a finer control over its operation, allowing me to only run it at certain hours, so I added a timer. But this meant that sometimes there wasn't enough hot water so I created this solution, that allows me to run it on the timer AND override it if the water gets too cold.


If this helps you in any way, drop me a line.

Pull requests are obviously welcome :)



