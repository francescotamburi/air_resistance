import math

#constants
dt = 0.01
k = 0.02
g = 9.8

class Projectile:
	def __init__(self, velocity, angle):
		self.angle = angle
		self.v0 = velocity
		self.setup(velocity, angle)
	
	def setup(self, velocity, angle):
		theta = math.radians(angle)
		self.x_vel = math.cos(theta) * velocity
		self.y_vel = math.sin(theta) * velocity
		self.x = 0
		self.y = 0
		self.in_air = True
		self.loglist = []
	
	def reset(self):
		self.setup(self.v0, self.angle)
	
	#x-acceleration
	def ax(self):
		return -k*self.x_vel*math.sqrt(self.x_vel**2+self.y_vel**2)
	
	#y-acceleration
	def ay(self):
		return -k*self.y_vel*math.sqrt(self.x_vel**2+self.y_vel**2)-g
	
	#checks for ground collision
	def collision_handler(self, vx, vy, x, y):
		if y >= 0: #commit points
			self.x_vel = vx
			self.y_vel = vy
			self.x     = x
			self.y     = y
			
		else: #calculate point of collision
			
			#line between two points
			dy = self.y - y
			dx = self.x - x
			m = dy/dx
			q = y - m*x
			
			#intersection with y=0
			self.y = 0
			self.x = -q/m
			
			self.in_air = False
	
	#logs current point
	def log(self):
		self.loglist.append((self.x, self.y))
	
	#calculates new position and velocity after a given dt
	def step(self, dt):
		if self.in_air:
			vx  = self.x_vel + self.ax() * dt #new x velocity
			vy  = self.y_vel + self.ay() * dt #new y velocity
			x   = self.x + vx * dt            #new x position
			y   = self.y + vy * dt            #new y position
			
			self.collision_handler(vx, vy, x, y)

#writes table in a .csv file from list of rows
def table(rows, filename, rownames):
	f = open(filename, "w")
	f.write(rownames + "\n")
	line = "%f, " * len(rownames.split(",")) + "\n"
	
	for row in rows:
		f.write(line % row)
	
	f.close()
	
#finds angle that gives longest range for a given speed
def angletest(projectile):
	
	#(angle, range)
	maxangle = (0,0)
	
	for a in range(0,90):
	
		projectile.angle = a
		projectile.reset()
	
		while projectile.in_air:
			projectile.step(dt)
		
		#print((a,p.x))
		if projectile.x > maxangle[1]:
			maxangle = (a, projectile.x)
	
	return maxangle


#Ranges, given angle

v0 = 150
projectiles = [Projectile(v0, angle) for angle in range(10, 81, 10)]

logs = []

for p in projectiles:
	while p.in_air:
		p.step(dt)
	logs.append((p.angle, p.x))

table(logs, "atable.csv", "angle,range")


#trajectory at 30°

p = Projectile(v0, 30)
p.log()

while p.in_air:
	p.step(dt)
	p.log()

table (p.loglist, "trajectory30.csv", "x,y")

#optimum angle and range for given launch speeds

projectiles = [Projectile(v, 0) for v in (5, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250)]

log = []

for p in projectiles:
	row = list(angletest(p))
	row = [p.v0] + row
	log.append(tuple(row))

table(log, "vtable.csv", "speed,angle,range")
