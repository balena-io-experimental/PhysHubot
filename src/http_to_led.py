# coding=utf-8

from flask import Flask, request
import scrollphathd as leds
import threading
import time
import os
import math


class LedManager(threading.Thread):
	def __init__(self):
		super(LedManager, self).__init__(target=self._loop)
		leds.rotate(180)
		leds.clear()
		leds.set_brightness(0.2)
		self.daemon = True
		self.scroll_remaining = 0
		self.phrases = []
		self.start()

	def queue(self, text="Hello world!"):
		self.phrases.append(text)
		return len(self.phrases)

	def _loop(self):
		while True:
			self.scroll_remaining -= 1
			if self.scroll_remaining == 0:
				leds.clear()
				leds.show()
			elif self.scroll_remaining > 0:
				leds.scroll()
				leds.show()
			elif len(self.phrases) > 0:
				self.scroll_remaining = leds.write_string("|      " + self.phrases.pop(0) + "      |") - 20
			else:
				t = self.scroll_remaining
				fade_in = min(1.0, -t / 30000.0)  # fade in over 10 minutes, at sleep(0.02) (50Hz)
				ox = math.sin(t/50.0) * 2.0
				oy = math.cos(t/50.0) * 2.0
				for x in range(17):
					dx = float(x) + ox - 8.0
					for y in range(7):
						dy = float(y) + oy - 3.0
						d = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
						b = math.sin(d + (t/5.0))
						b = (b + 1) / 2
						b = b * fade_in
						leds.set_pixel(x, y, b)
				leds.show()
			time.sleep(0.02)


ledManager = LedManager()
print(' * Connected to LEDs.')
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def handle_request():
	output = '<html><body>'
	try:
		text = request.form['text']
		before = ledManager.queue(text)
		output += '<p>'+ text + " is behind " + str(before) + " other items.</p>"
	except KeyError:
		pass
	output += '<form method="post"><input type="text" name="text" placeholder="phrase"></input></form>'
	output += '</body></html>'
	return output


if __name__ == '__main__':
	app.run(port=80)
