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

import sys
from informationProvider import *
importjson
#Mode 1 the interval is a day, and mode 2 is an hour.
mode = int(sys.argv[1])
startDate = datetime(2014, 8, 12)
endDate = datetime(2014, 10, 13)
array = []
if mode == 1:
    interval = timedelta(days=1)
elif mode == 2:
    interval = timedelta(hours=1)
while startDate < endDate:
    data = {}
    data['date'] = str(startDate)
    data['activeness'] = getActiveness(startDate, mode)
    data['socialization'] = getSocializationLevel(startDate, mode)
    data['occupation_level'] = getOccupationLevel(startDate, mode)
    data['presence'] = getPresence(startDate, mode)
    startDate = startDate+interval
    array.append(data)
with open('data_hourly.json', 'a') as thefile:
    thefile.write(json.dumps(array))
