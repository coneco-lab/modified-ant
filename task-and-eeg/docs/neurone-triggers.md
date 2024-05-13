<h2 style="text-align: center;">How to connect a stimulus PC, a Bittium NeurOne system, and TMS <br> via a parallel port</h2>

### Set-up

- One PC with PsychoPy installed
	- MATLAB-Psychtoolbox would work the same
- One EEG system
- One TMS stimulator
- One parallel port to connect the stimulus PC to:
	- The EEG system (to mark the EEG trace at experimental events of interest)
	- The stimulator (to trigger stimulation with experimental events of interest)
	- Both 

What the parallel port connects to (i.e., the EEG system, the stimulator, or both) depends on the type of cable. 
In our current set-up (April 2024), we can connect the stimulus PC to both the EEG system and the stimulator via a DB-25 connector, from which two cables depart: 

- One 3-meters long cable that ends with a DB-15 connector to plug into the EEG system
- One 3-meters long cable that ends with a BNC connector to plug into the stimulator

### Send signals through the parallel port with PsychoPy

PsychoPy provides tools to interact with a wealth of external hardware, including parallel ports. They are not well documented, but they work. 

As of April 2024, the syntax to send one signal along a given pin of the parallel port is the following:

	from psychopy import parallel
	port = parallel.ParallelPort(address=<insert address here>)
	port.setPin(pinNumber=<insert pin number here>, state=1
	<code for the experimental event of interest here>
	port.setPin(pinNumber=<insert same pin number here>, state=0)

#### Step-by-step breakdown

1. `from psychopy import parallel`
Imports the `parallel` module from the PsychoPy library, i.e., it makes it available to the script you are running. Place this atop your script
2. `port = parallel.ParallelPort(address=<insert address here>)`
Initializes a `port` object from the  `ParallelPort` class contained in `parallel`. This object will have an `address` attribute with the value that you insert.  In other words, this code line tells Python that there's a thing called `port` which is a parallel port with address `address`. Place it before you begin iterating over trials
3. `port.setPin(pinNumber=<insert pin number here>, state=1)`
Sends a signal through a given pin of the parallel port. Place it wherever you need to send a signal (i.e., every time you present a given stimulus)
4. `port.setPin(pinNumber=<insert pin number here>, state=0)`
Stops sending a signal through the given pin of the parallel port.

#### What happens when you open pins

Signals come out the stimulus PC, travel in parallel along corresponding pin and cable, then enter:

- The EEG system if that's the only thing connected to the PC
- The stimulator if that's the only thing connected to the PC
- Both if they are both connected to the PC

In our current set-up, the stimulator receives signals sent over pin 2. If you want to deliver TMS at an experimental event of interest, use `pinNumber=2`. If you are doing concurrent TMS and EEG, using `pinNumber=2` marks the EEG trace _and_ triggers TMS. 

### Relationship between pin number and event code

All parallel port connections implement a map between a pin's identity and the code that the signal sent through it is assigned on the receiving machine (i.e., the name of the corresponding marker on the EEG trace). Our montage[1] is tailored to the proprietary EEG hardware that we use (Bittium NeurOne) and  is as follows: 

| Stimulus PC output (DB25 connector) | Corresponding EEG system input (DB15 connector) |
|-------------------------------------|-------------------------------------------------|
| pin 2 (true 0)                      | pin 1                                           |
| pin 3 (true 1)                      | pin 2                                           |
| pin 4 (true 2)                      | pin 3                                           |
| pin 5 (true 3)                      | pin 4                                           |
| pin 6 (true 4)                      | pin 5                                           |
| pin 7 (true 5)                      | pin 6                                           |
| pin 8 (true 6)                      | pin 7                                           |
| pin 9 (true 7)                      | pin 8                                           |
| all other pins inactive             | all other pins inactive                         |

The information contained in this table shall be read as:

- When you open pin number 2 from the stimulus PC via PsychoPy (`pinNumber=2`), the receiver (i.e., the EEG system) will encode the incoming signal as $2^0 = 1$ and you will see a `1` marker on the EEG trace
- When you open pin number 3, the receiver will encode the incoming signal as $2^1 = 2$ and you will see a `2` marker on the EEG trace
- When you open pin number 4, the receiver will encode the incoming signal as $2^2 = 4$ and you will see a `4` marker on the EEG trace
- When you open pin number 5, the receiver will encode the incoming signal as $2^3 = 8$ and you will see an `8` marker on the EEG trace
- etc.

In general, the receiver will encode incoming signals as: 
$$2^n, \ \text{where} \ n = \ \text{true pin number} $$

#### Contemporaneously opened pins sum up

Opening more pins at the same time results in cumulative codes, i.e., the receiver will encode the first signal as per the rule described above, and all following signals as the sum of their regular code plus all the codes of contemporaneously opened pins. Therefore, opening pins 2, 3 and 4 will result in the following situation:

$$\text{code(pin2)} = 2^0 = 1$$
$$\text{code(pin3)} = \text{code(pin2)} + \text{code(pin3)} = 2^0 + 2^1 = 1 + 2 = 3 $$
$$\text{code(pin4)} = \text{code(pin2)} + \text{code(pin3)} + \text{code(pin4)} = 
2^0 + 2^1 + 2^2 = 1 + 2 + 4 = 7 $$

Which, in general terms, can be written as:

$$\text{code(pinN)} = \sum_{i=d}^{N} 2^{i-d}$$

where $d$ is the difference between a pin's number as assigned by the software and its true number. In our case, $d= 2$  (cf. table), so we have:

$$\text{code(pinN)} = \sum_{i=2}^{N} 2^{i-2}$$

---

[1] Both the DB25 connector on the PC end of the cable and the DB15 connector on the EEG end of the cable have 8 active pins, i.e., the signal travelling along the trigger cable is an 8-bit signal (_"8-bit trigger"_). This means that there are 8 signal carriers (the pins), each of which can be either open (`state=1`) or closed (`state=0`). In turn, this implies that there are $256$ possible state distributions over the 8 pins. Indeed, the number of possible combinations for $n$ elements taken $k$ at a time is always $n^k$. In our case, there are $n = 2$ state values (open, closed) taken $k = 8$ at a time (because there are 8 pins, state values are observed 8 at a time). $2^8 = 256$, so we have 256 possible combinations of open/closed states over the 8 pins.  