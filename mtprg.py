# import secrets
import binascii, os
import random

class MersenneTwisterPRNG(object):
	def __init__(self):
		self.N = 624
		self.M = 397
		self.A = 0x9908b0df
		self.UPPER = 0x80000000
		self.LOWER = 0x7fffffff
		self.m = [None] * self.N
		self.mi = self.N

	def setSeed(self, seed):
		self.m[0] = seed & 0xffffff
		for i in xrange(1, self.N):
			self.m[i] = (69069 * self.m[i - 1]) & 0xffffffff

		self.mi = self.N

	def nextInt(self):
		if self.mi >= self.N:
			for k in xrange(0, self.N - 1):
				y = (self.m[k] & self.UPPER) | (self.m[(k + 1) % self.N] & self.LOWER)
				self.m[k] = self.m[(k + self.M) % self.N] ^ (y >> 1)

				if y % 2 == 1:
					self.m[k] = self.m[k] ^ self.A

			self.mi = 0

		y = self.m[self.mi]
		self.mi += 1
		y = y ^ (y >> 11)
		y = y ^ ((y << 7) & 0x9d2c5680)
		y = y ^ ((y << 15) & 0xefc60000)
		y = y ^ (y >> 18)

		return y

secret_key = random.getrandbits(32)
init_vec = random.getrandbits(32)
prg = MersenneTwisterPRNG()

def encrypt(message, secret_key, init_vec):
	prg.setSeed(secret_key ^ init_vec)

	S = 127
	pad = [prg.nextInt() for i in xrange(len(message))]
	return ''.join([chr((ord(m) + p) % S) for m, p in zip(message, pad)])

def decrypt(ciphertext, secret_key, init_vec):
	prg.setSeed(secret_key ^ init_vec)

	S = 127
	pad = [prg.nextInt() for i in xrange(len(ciphertext))]
	# dec = []
	# for c, p in zip(ciphertext, pad):
	# 	d = chr((ord(c) + p) % S)
	# 	print d, p
	# 	dec.append(d)
	#
	# return dec
	return ''.join([chr((ord(c) - p) % S) for c, p in zip(ciphertext, pad)])

ciphertext = encrypt('Hello World', secret_key, init_vec)
print 'Encrypted: ', ciphertext
print 'Decrypted: ', decrypt(ciphertext, secret_key, init_vec)
