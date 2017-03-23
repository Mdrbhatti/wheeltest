from cffi import FFI
import weakref
global_weakrefs = weakref.WeakKeyDictionary()

ffi = FFI()
ffi.cdef("""
	typedef long long GoInt64;
	typedef GoInt64 GoInt;
	typedef struct { const char *p; GoInt n; } GoString;
	typedef struct { void *data; GoInt len; GoInt cap; } GoSlice;
	typedef double GoFloat64;
	GoInt Add(GoInt p0, GoInt p1);
	GoFloat64 Cosine(GoFloat64 p0);
	void Sort(GoSlice p0);
	GoInt Log(GoString p0);
	""")

lib = ffi.dlopen('../lib/./awesome.so')

# Convert a python string to a GoString
def toGoString(string):
	# CFFI works fully with python3, but all strings need to be encoded, decoded
	# i.e. string_p = ffi.new('char[]', string.encode())
	string_p = ffi.new('char[]', string)
	v = ffi.new('GoString*', {'p': string_p,'n': len(string)})[0]
	global_weakrefs[v] = (string_p,)
	return v

# Convert python list to a GoSlice
def toGoSlice(data):
	data_p = ffi.new('GoInt[]', data)
	v = ffi.new('GoSlice*', {'data': data_p,'len': len(data),'cap': len(data)})[0]
	# Let data_p live as long as v
	global_weakrefs[v] = (data_p,)
	return v

# Convert a GoSlice to a python list
def toPythonList(data):
	pylist = []
	for i in range(data.len):
		pylist.append(ffi.cast('GoInt*', data.data)[i])
	return pylist

def testAllMethods():
	print "5 + 6 = ", lib.Add(5,6)
	# Run Cosine
	print "Cos(3.148) = ", lib.Cosine(3.148)
	# Run Sort
	data = [-441,10,-3,9,-88,100]
	data_go = toGoSlice(data)
	lib.Sort(data_go)
	print "Sorted ", data, "  =  ", toPythonList(data_go)
	# Run Log
	print "Count : ", lib.Log(toGoString("Hello from Go"))