class RainbowColors:
	@staticmethod
	def get(c):
		
		r, g, b, mc = 0, 0, 0, c % 256
		
		if c < 256:
			r, g, b = mc, 0, 255
		elif c < 512:
			r, g, b = 255, 0, 255 - mc
		elif c < 768:
			r, g, b = 255, mc, 0
		elif c < 1024:
			r, g, b = 255 - mc, 255, 0
		elif c < 1280:
			r, g, b = 0, 255, mc
		elif c < 1536:
			r, g, b = 0, 255 - mc, 255
		
		c += 32
		if c >= 1536: c = 0
		
		return r, g, b, c