
import serial
import time
import sys

import MDSplus

def qc_connect (port) :
	ser = serial.Serial(port, 115200, timeout=1)
	time.sleep(0.5)

	if not ser.isOpen() :
		print('Serial port not open.')
		sys.exit(1)

	return ser

def qc_talk (ser, msg) :
	ser.write(msg + '\r\n')

	reply = ser.readline()
	ser.read(1) # clear out extra \x00 character

	return reply.strip('\r\n')

class QC9200 (MDSplus.Device) :
	"""Limited control for the Quantum Composers Sapphire 9200 Series Pulse Generator."""

	parts=[{'path': ':PORT',        'type': 'TEXT',    'value': 'COM3'}, # likely /dev/ttyACM0 on Linux
	       {'path': ':TRIG_LEVEL',  'type': 'NUMERIC', 'value': 2.5},
	       {'path': ':TRIG_EDGE',   'type': 'TEXT',    'value': 'RISING'}, # or FALLING
	       {'path': ':PERIOD',      'type': 'NUMERIC', 'value': 0.1},      # seconds
	       {'path': ':N_BURST',     'type': 'NUMERIC', 'value': 5},
	       {'path': ':ACT_INIT',    'type': 'ACTION',  'valueExpr': "Action(Dispatch('DAQ_SERVER', 'INIT',   1, None), Method(None, 'init',   head))"},
	       {'path': ':ACT_DEINIT',  'type': 'ACTION',  'valueExpr': "Action(Dispatch('DAQ_SERVER', 'DEINIT', 1, None), Method(None, 'disarm', head))"},
	       {'path': ':INIT_CONFIG', 'type': 'TEXT'}] # includes "plus" status, *IDN?, list of channels

	for ch in ('A', 'B', 'C', 'D') :
		parts.append({'path': '.CHANNEL_%s'          % ch, 'type': 'STRUCTURE'})
		parts.append({'path': '.CHANNEL_%s:DELAY'    % ch, 'type': 'NUMERIC', 'value': 0.0})      # seconds
		parts.append({'path': '.CHANNEL_%s:WIDTH'    % ch, 'type': 'NUMERIC', 'value': 10e-3})    # seconds
		parts.append({'path': '.CHANNEL_%s:LEVEL'    % ch, 'type': 'NUMERIC', 'value': 5.0})      # Volts
		parts.append({'path': '.CHANNEL_%s:POLARITY' % ch, 'type': 'TEXT',    'value': 'NORMAL'}) # or INVERTED

	def init (self, arg) :

		#### read config nodes ####

		try :
			port       = self.port.data()
			trig_level = float(self.trig_level.data())
			trig_edge  = self.trig_edge.data().upper()
			period     = float(self.period.data())
			n_burst    = int(self.n_burst.data())

			if trig_level < 0.2 or trig_level > 15.0 or not (trig_edge == 'RISING' or trig_edge == 'FALLING') : raise Oops
			if period <= 0.0 or n_burst < 1                                                                   : raise Oops

			enable   = []
			delay    = []
			width    = []
			level    = []
			polarity = []

			for ch in ('A', 'B', 'C', 'D') :
				enable.append(     self.getNode('.CHANNEL_%s'          % ch).on)
				delay.append(float(self.getNode('.CHANNEL_%s:DELAY'    % ch).data()))
				width.append(float(self.getNode('.CHANNEL_%s:WIDTH'    % ch).data()))
				level.append(float(self.getNode('.CHANNEL_%s:LEVEL'    % ch).data()))
				polarity.append(   self.getNode('.CHANNEL_%s:POLARITY' % ch).data().upper())

			for n in range(4) :
				if delay[n] < 0.0          or  delay[n] > 1e3            : raise Oops
				if width[n] < 10e-9        or  width[n] > 1e3            : raise Oops
				if level[n] < 3.3          or  level[n] > 5.0            : raise Oops
				if polarity[n] != 'NORMAL' and polarity[n] != 'INVERTED' : raise Oops

		except :
			print('One or more configs is missing or invalid.')
			return 0

		#### pre-program ####

		ser = qc_connect(port)

		ans = qc_talk(ser, '*IDN?')
		config = 'Identification: ' + ans + '\n' # first line of INIT_CONFIG

		ans = qc_talk(ser, ':SYST:VERS?')
		config += 'SCPI version: ' + ans + '\n'

		ans = qc_talk(ser, ':SYST:COMM:BLUE:EN?')
		config += 'Bluetooth: ' + ('No' if '?2' in ans else 'Yes') + '\n'

		ans = qc_talk(ser, ':PULS0:COUN:STAT?')
		config += 'Plus features: ' + ('No' if '?2' in ans else 'Yes') + '\n'

		ans = qc_talk(ser, ':INST:CAT?')
		config += 'Channels: ' + ans + '\n'
		N_chan = len(ans.split(',')) - 1 # system timer is also a channel

		ans = qc_talk(ser, '*RCL 0')
		config += 'Load defaults: ' + ('OK' if 'ok' in ans else 'Failed') + '\n'

		#### program user settings ####

		ok =        'ok' in qc_talk(ser, ':PULS0:MOD BURS') # first OK check
		ok = ok and 'ok' in qc_talk(ser, ':PULS0:PER %.9f'     % period)
		ok = ok and 'ok' in qc_talk(ser, ':PULS0:BCO %d'       % n_burst)
		ok = ok and 'ok' in qc_talk(ser, ':PULS0:EXT:MOD TRIG')
		ok = ok and 'ok' in qc_talk(ser, ':PULS0:EXT:LEV %.3f' % trig_level)
		ok = ok and 'ok' in qc_talk(ser, ':PULS0:EXT:EDG %s'   % trig_edge)

		for n in range(N_chan) :
			ok = ok and 'ok' in qc_talk(ser, ':PULS%d:STAT %d'        % (n + 1, enable[n]))
			ok = ok and 'ok' in qc_talk(ser, ':PULS%d:DEL %.9f'       % (n + 1, delay[n]))
			ok = ok and 'ok' in qc_talk(ser, ':PULS%d:WIDT %.9f'      % (n + 1, width[n]))
			ok = ok and 'ok' in qc_talk(ser, ':PULS%d:OUTP:AMPL %.3f' % (n + 1, level[n]))
			ok = ok and 'ok' in qc_talk(ser, ':PULS%d:POL %s'         % (n + 1, polarity[n]))

		config += 'Program settings: ' + ('OK' if ok else 'Failed') + '\n'

		#### read other settings ####

		config += 'Other settings:\n'

		msg = ':SYST:AUT?'
		config += '  ' + msg + ' ' + qc_talk(ser, msg) + '\n'

		for key in ('PCO', 'OCO', 'EXT:POL') :
			msg = ':PULS0:%s?' % key
			config += '  ' + msg + ' ' + qc_talk(ser, msg) + '\n'

		for n in range(N_chan) :
			for key in ('SYNC', 'MUX', 'CMOD', 'BCO', 'PCO', 'OCO', 'WCO', 'CGAT') :
				msg = ':PULS%d:%s?' % (n + 1, key)
				config += '  ' + msg + ' ' + qc_talk(ser, msg) + '\n'

		#### arm system ####

		if ok :
			ans = qc_talk(ser, ':PULS0:STAT 1')
			ok = 'ok' in ans
			config += 'Armed: ' + 'OK' if ok else 'Failed'

		ser.close()

		self.init_config.putData(config)

		return 1 if ok else 0

	def trigger (self, arg) :
		ser = qc_connect(self.port.data())
		ans = qc_talk(ser, '*TRG')
		ser.close()

		return 1 if 'ok' in ans else 0

	def disarm (self, arg) :
		ser = qc_connect(self.port.data())
		ans = qc_talk(ser, ':PULS0:STAT 0')
		ser.close()

		return 1 if 'ok' in ans else 0
