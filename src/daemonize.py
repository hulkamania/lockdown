import os
import sys

class Daemonize:
	''' Generic class for creating a daemon
		http://code.activestate.com/recipes/578072-generic-way-to-create-a-daemonized-process-in-pyth/
	'''

	def daemonize(self):
		try:
			#this process would create a parent and a child
			pid = os.fork()
			if pid > 0:
				# take care of the first parent
				sys.exit(0)
		except OSError, err:
			sys.stderr.write("Fork 1 has failed --> %d--[%s]\n" % (err.errno, err.strerror))
			sys.exit(1)

		#change to root
		os.chdir('/')
		#detach from terminal
		os.setsid()
		# file to be created ?
		os.umask(0)

		try:
			# this process creates a parent and a child
			pid = os.fork()
			if pid > 0:
				print "Daemon process pid %d" % pid
				#bam
				sys.exit(0)
		except OSError, err:
			sys.stderr.write("Fork 2 has failed --> %d--[%s]\n" % (err.errno, err.strerror))
			sys.exit(1)

		sys.stdout.flush()
		sys.stderr.flush()

	def start_daemon(self):
		self.daemonize()
		self.run_daemon()

	def run_daemon(self):
		''' override this function
		'''
		pass
