"""
Copyright (c) 2015 Aritz Bilbao, Aitor Almeida
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
@author: "Aritz Bilbao, Aitor Almeida"
@contact: aritzbilbao@deusto.es, aitor.almeida@deusto.es
"""


import string
import random
from hashlib import sha512
from time import time


def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.
    Note: this method may produce invalid filenames such as ``, `.` or `..`
    When I use this method I prepend a date string like '2009_01_15_19_46_32_'
    and append a file extension like '.txt', so I avoid the potential of using
    an invalid filename.
    Source: https://gist.github.com/seanh/93666
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ', '_')  # I don't like spaces in filenames.
    return filename


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """Generates a new id to be used as salt when hashing"""
    try:
        # secure random number. Uses the OS random source, so might raise error
        return ''.join(random.SystemRandom().choice(chars) for x in range(size))
    except NotImplementedError:
        # no-so-secure random number, only called if there is no random source in the OS (unlikely)
        return ''.join(random.choice(chars) for x in range(size))


def hash_pass(password, salt=None):
    """Securely hashes the given password"""
    if not salt:
        salt = sha512(id_generator(32, chars=string.ascii_letters + string.digits)).hexdigest()
    hsh = sha512('%s%s' % (salt, password)).hexdigest()
    return '%s$%s' % (salt, hsh)


def check_pass(password, hsh):
    """Checks whether the given password corresponds to the given hash"""
    salt, passhash = hsh.split('$')
    return hsh == hash_pass(password, salt)


def get_timestamp(timestamp=None):
    """Returns the given UNIX timestamp, or the current time if it is not given, in milliseconds"""
    if timestamp is None:
        timestamp = time()
    return int(round(timestamp * 1000))
