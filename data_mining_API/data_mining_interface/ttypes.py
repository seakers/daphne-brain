#
# Autogenerated by Thrift Compiler (0.10.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
import sys

from thrift.transport import TTransport


class DrivingFeature(object):
    """
    Attributes:
     - id
     - name
     - expression
     - metrics
    """

    thrift_spec = (
        None,  # 0
        (1, TType.I32, 'id', None, None, ),  # 1
        (2, TType.STRING, 'name', 'UTF8', None, ),  # 2
        (3, TType.STRING, 'expression', 'UTF8', None, ),  # 3
        (4, TType.LIST, 'metrics', (TType.DOUBLE, None, False), None, ),  # 4
    )

    def __init__(self, id=None, name=None, expression=None, metrics=None,):
        self.id = id
        self.name = name
        self.expression = expression
        self.metrics = metrics

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I32:
                    self.id = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.expression = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.LIST:
                    self.metrics = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in range(_size0):
                        _elem5 = iprot.readDouble()
                        self.metrics.append(_elem5)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('DrivingFeature')
        if self.id is not None:
            oprot.writeFieldBegin('id', TType.I32, 1)
            oprot.writeI32(self.id)
            oprot.writeFieldEnd()
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 2)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        if self.expression is not None:
            oprot.writeFieldBegin('expression', TType.STRING, 3)
            oprot.writeString(self.expression.encode('utf-8') if sys.version_info[0] == 2 else self.expression)
            oprot.writeFieldEnd()
        if self.metrics is not None:
            oprot.writeFieldBegin('metrics', TType.LIST, 4)
            oprot.writeListBegin(TType.DOUBLE, len(self.metrics))
            for iter6 in self.metrics:
                oprot.writeDouble(iter6)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class Architecture(object):
    """
    Attributes:
     - id
     - bitString
     - science
     - cost
    """

    thrift_spec = (
        None,  # 0
        (1, TType.I32, 'id', None, None, ),  # 1
        (2, TType.STRING, 'bitString', 'UTF8', None, ),  # 2
        (3, TType.DOUBLE, 'science', None, None, ),  # 3
        (4, TType.DOUBLE, 'cost', None, None, ),  # 4
    )

    def __init__(self, id=None, bitString=None, science=None, cost=None,):
        self.id = id
        self.bitString = bitString
        self.science = science
        self.cost = cost

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I32:
                    self.id = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.bitString = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.DOUBLE:
                    self.science = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.DOUBLE:
                    self.cost = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('Architecture')
        if self.id is not None:
            oprot.writeFieldBegin('id', TType.I32, 1)
            oprot.writeI32(self.id)
            oprot.writeFieldEnd()
        if self.bitString is not None:
            oprot.writeFieldBegin('bitString', TType.STRING, 2)
            oprot.writeString(self.bitString.encode('utf-8') if sys.version_info[0] == 2 else self.bitString)
            oprot.writeFieldEnd()
        if self.science is not None:
            oprot.writeFieldBegin('science', TType.DOUBLE, 3)
            oprot.writeDouble(self.science)
            oprot.writeFieldEnd()
        if self.cost is not None:
            oprot.writeFieldBegin('cost', TType.DOUBLE, 4)
            oprot.writeDouble(self.cost)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
