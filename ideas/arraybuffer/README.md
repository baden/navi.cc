Идея в том, чтобы передавать бинарные данные треков и разбирать их на стороне клиента.

Процедура получения выглядит примерно так:

'''
BDParser = function() {
}

BDParser.load = function(src, callback, onerror) {
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'arraybuffer';
    xhr.onload = function() {
	//console.log('xhr.response=', xhr.response);
	var d = new BDParser().parse(xhr.response);		// WTF?
	callback(d);
    };
    xhr.onerror = onerror;
    xhr.open('GET', src);
    xhr.send(null);
}

BDParser.prototype.parse = function(arrayBuffer) {
    var o = {};
    var dv = new DataView(arrayBuffer);
    var idx = 0;

    /*
    Useful functions:
        byte getInt8(unsigned long byteOffset);
        unsigned byte getUint8(unsigned long byteOffset);
        short getInt16(unsigned long byteOffset, optional boolean littleEndian);
        unsigned short getUint16(unsigned long byteOffset, optional boolean littleEndian);
        long getInt32(unsigned long byteOffset, optional boolean littleEndian);
        unsigned long getUint32(unsigned long byteOffset, optional boolean littleEndian);
        float getFloat32(unsigned long byteOffset, optional boolean littleEndian);
        double getFloat64(unsigned long byteOffset, optional boolean littleEndian);

    */

    o.data1 = dv.getInt32(idx, true);
    idx += 4;

    o.data2 = dv.getFloat32(idx, true);
    idx += 4;
    o.data2 = dv.getFloat64(idx, true);
    idx += 8;

    o.sometype = this.parseType1(dv, idx);
}

BDParser.prototype.parseType1 = function(dv, idx) {
    var res = {}
    res.some1 = dv.getInt32(idx, true);
    return res;
}

И использование:
    BDParser.load('api/get/04324.bin', bdLoad, dbError);
    function bdLoad(bd) {
	console.log('loaded bd=', bd);
	// ...
    }

'''
