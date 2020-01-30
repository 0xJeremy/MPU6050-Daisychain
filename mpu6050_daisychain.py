from mpu6050 import MPU6050

class MPU6050_Daisy():
	def __init__(self, i2c_bus, addresses, names=None, file=None):
		self._devices = []
		self._addresses = addresses
		for addr in addresses:
			try:
				self._devices.append(MPU6050(i2c_bus, addr))
			except RuntimeError:
				raise RuntimeError("Failed to find MPU6050 device at address {}".format(addr))
		if names is not None:
			self.name_devices(names)
		else: self._names = None
		if file is not None:
			self.set_file(file)
		else: self._file = None

	def reset_all(self):
		for i in self._devices:
			i.reset()

	######################################
	### WRAPPERS FOR MPU6050 INTERFACE ###
	######################################

	@property
	def temperature(self):
		return [i.temperature() for i in self._devices]

	@property
	def acceleration(self):
		return [i.acceleration() for i in self._devices]

	@property
	def gyro(self):
		return [i.gyro() for i in self._devices]

	@property
	def cycle(self):
		return [i.cycle() for i in self._devices]

	@property
	def gyro_range(self):
		return [i.gyro_range for i in self._devices]

	def set_gyro_range(self, value):
		for i in range(len(self._devices)):
			try:
				self._devices[i].gyro_range = value
			except ValueError:
				raise ValueError("gyro_range must be in GyroRange on device {}". self._addresses[i])
	
	@property
	def acceleration_range(self):
		return [i.acceleration_range for i in self._devices]

	@property
	def filter_bandwidth(self):
		return [i.filter_bandwidth for i in self._devices]

	def set_filter_bandwidth(self, value):
		for i in range(len(self._devices)):
			try:
				self._devices[i].filter_bandwidth = value
			except ValueError:
				raise ValueError("filter_bandwidth must be a Bandwidth on device {}".format(self._addresses[i]))

	@property
	def cycle_rate(self):
		return [i.cycle_rate for i in self._devices]

	def set_cycle_rate(self, value):
		for i in range(len(self._devices)):
			try:
				self._devices[i].cycle_rate = value
			except ValueError:
				raise ValueError("cycle_rate must be a Rate on device {}".format(self._addresses[i]))

	################################
	### ADDITIONAL FUNCTIONALITY ###
	################################

	def get(self, pos):
		return self._devices[pos]

	def get_with_addr(self, pos):
		return self._devices[pos], self._addresses[pos]

	def get_all(self):
		return self._devices

	def get_all_with_name(self):
		if self._names is None:
			raise RuntimeError("No device names specified.")
		return [(self._devices[i], self._names[i]) for i in range(len(self._devices))]

	def name_devices(self, names):
		if len(names) is not len(self._devices):
			raise RuntimeError("Length of names is not the same as number of devices")
		self._names = names

	def set_file(self, file):
		if self._file is not None:
			raise RuntimeError("File already opened! Cannot open another.")
		self._file = open(file, "a")

	def write(self):
		if self._file is None:
			raise RuntimeError("No file opened.")
		for i in self._devices:
			self._file.write("{}, {}".format(i.acceleration, i.gyro))

	def close_file(self):
		if self._file is None:
			raise RuntimeError("No file opened.")
		self._file.close()
