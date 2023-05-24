from flask import Flask, render_template, jsonify

app = Flask(_name_)
app.config['DEBUG'] = True

Vrms = 0
Irms = 0
act_pow = 0
E = 0

dynamic_data = {
    'VandI' : f"{Vrms} {Irms}" ,
    'pow_act': act_pow,
    'unit_consumed': E
    # file.write("VandI: {}   {}\n".format(Vrms, Irms))
	# file.write("pow_act: {}\n".format(act_pow))
	# file.write("unit consumed: {}\n".format(E))
}

@app.route('/')
def index():
    return render_template('index.html', data=dynamic_data)

@app.route('/refresh_div', methods=['GET'])
def refresh_div():
    return jsonify(dynamic_data)


@app.route('/trip_relay')
def trip_relay():
    GPIO.output(17, GPIO.LOW)
    return 'Relay tripped'


if _name_ == '_main_':
    app.run()





import time
#import pyplot as plt

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)





# Software SPI configuration:
CLK  =11
MISO =9
MOSI =10
CS   =8

GPIO.setup(17,GPIO.OUT)
GPIO.output(17,GPIO.HIGH)

mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#SPI_DEVICE = 0
#mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)
# Main program loop.



def rms(runtime):
 
    smpl=0
    ens=0
    start_time=time.time()
    loop_value=0
    isqr_sm=0
    vsqr_sm=0
    avgir=0
    avgvr=0
   
    
    
    while (ens<runtime):
        # Read all the ADC channel values in a list.
        smpl=smpl+1
        values = [0]*8
        for i in range(8):
            # The read_adc function will get the value of the specified channel (0-7).
            values[i] = mcp.read_adc(i)
        # Print the ADC values.
       # print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
        # Pause for half a second.
        #print('| {0:>4} | {1:>4} |'.format(*values))
        channel0_value = float(values[0])
        result = float((((channel0_value) * 5/1023)-2.5)*7.6)
        
       
        
        channel1_value = float(values[1])
        result1 = float((((channel1_value) * 5/1023)-2.5)*425)
       #print('voltage:', result1)
        #print('current:', result)
        #print ("power", result*result1)
        j=0+result*result
        #print ("current sqr",a)
        loop_value=loop_value+1
        v=0+result1*result1
        isqr_sm=isqr_sm+j
        vsqr_sm=vsqr_sm+v
        end_time=time.time()
        ens=(end_time-start_time)
       #print(ens)
        
        
        
        
         
    
    x=(isqr_sm/smpl)**0.5
    #print("irms",x)
    y=(vsqr_sm/smpl)**0.5
    #print("vrms",y)
    return x,y
    
   
    #print("time",ens)
    #print(smpl)
    

    #rms(runtime)    
E=0


while True:
	z=0
	
	Vrsum=0
	Irsum=0
	while(z<10):

	 m,n=rms(0.3)
	 Vrsum=Vrsum+n
	 Irsum=Irsum+m
	 z=z+1
	Vrms=Vrsum* 0.1
	Irms=Irsum*0.1
	if(Irms<0.28):
	 Irms=0
	

	print("VandI",Vrms,"   ",Irms)
	if(Irms>2):
	    GPIO.output(17,GPIO.LOW)
	act_pow=Vrms*Irms
	E=E+act_pow/120000
	print("pow_act",act_pow)
	print("unit consumed=",E)
	file = open('output.txt', 'a')
	file.write("VandI: {}   {}\n".format(Vrms, Irms))
	file.write("pow_act: {}\n".format(act_pow))
	file.write("unit consumed: {}\n".format(E))
	file.write("\n")
	# Plotting the graph
	#plt.plot(time_values, unit_consumed_values, 'b-')
	#plt.xlabel('Time')
	#plt.ylabel('Energy (E)')
	#plt.title('Energy Consumption over Time')
	#plt.grid(True)
	#plt.show()
