import sys
import time
import threading

from baseplatform import BasePlatform


class DesktopPlatform(BasePlatform):

	def __init__(self, config):
		super(DesktopPlatform, self).__init__(config)

		self.__config = config
		self.__pconfig = config['platforms']['common']
		self.__pconfig.update(config['platforms']['desktop'])

		self.should_confirm_trigger = self.__pconfig['should_confirm_trigger']

		self.trigger_thread = None

		self.started = 0

	def setup(self):
		pass

	def indicate_setup_failure(self):
		print("setup_failure")
		sys.exit()

	def indicate_setup_success(self):
		print("setup_complete")

	def indicate_recording(self, state=True):
		print("indicate_recording_on " + str(state))

	def indicate_playback(self, state=True):
		print("indicate_playback " + str(state))

	def after_setup(self):
		self.trigger_thread = DesktopPlatformTriggerThread(self)
		self.trigger_thread.setDaemon(True)
		self.trigger_thread.start()

	def should_record(self):
		return time.time() - self.started < self.__pconfig['min_seconds_to_record']

	def cleanup(self):
		self.trigger_thread.stop()


class DesktopPlatformTriggerThread(threading.Thread):
	def __init__(self, platform):
		threading.Thread.__init__(self)

		self.platform = platform
		self.should_run = True

	def stop(self):
		self.should_run = False

	def run(self):
		while self.should_run:
			key = ""
			while key != 'a':
				key = raw_input('Type "a" to trigger Alexa: ')

			self.platform.started = time.time()
