import serial


com_serial = serial.Serial('/dev/ttyUSB0', timeout=1, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=False, rtscts=False, dsrdtr=False)


status = []
statusraw = []

#Send CMD_PC_CTRL_STOP
CMD_PC_CTRL_STOP = "\x02\x01\x02\x03\xFC"
com_serial.write(CMD_PC_CTRL_STOP)


#Send CMD_PC_CTRL_START
CMD_PC_CTRL_START = "\x02\x02\x01\x01\x03\xFB"
com_serial.write(CMD_PC_CTRL_START)

read_byte = com_serial.read()
status.append(ord(read_byte))
statusraw.append(read_byte)

while read_byte is not None:
    read_byte = com_serial.read()
    if read_byte == '':
        read_byte = None
        break
    status.append(ord(read_byte))
    statusraw.append(read_byte)

l = len(status)
device = status[0:status[1]+4]
sensor = status[status[1]+4:l]



#Send CMD_PC_CTRL_STOP
CMD_PC_CTRL_STOP = "\x02\x01\x02\x03\xFC"
com_serial.write(CMD_PC_CTRL_STOP)

ndata = device[1]-1
actualcurr = device[3]
dataindex = device[4]
modeindex = device[5]
batchindex = device[6]
batchn1 = device[7]
batchn2 = device[8]
currn = device[9]
currencies = []
i = 10
for j in range(currn):
    currencies.append('')
    for k in range(3):
        currencies[j] = currencies[j]+chr(device[10+j*3+k])
        i = i + 1

ndenom = []
for j in range(currn-1):
    ndenom.append(device[i])
    i = i + 1

cant_batch = []
for j in range(ndata-i+3):
    cant_batch.append(device[i])
    i = i + 1

sensores = [0,0,0,0,0,0,0,0]
sensorstatus = sensor[3]
i=0
while sensorstatus // 2 != 0:
    sensores[i]=sensorstatus % 2
    sensorstatus = sensorstatus // 2
    i = i + 1
    if sensorstatus == 1:
        sensores[i]=sensorstatus % 2

BosilloR = ['Libre','Ocupado']
Puerta = ['Cerrada','Abierta']
Modos = ['Mezcla','Denominacion','Cuentanotas','Cara','Orientacion','Issue','Serial','Separate','Barcode','Barcode + Efectivo','','Dissue']
Lote = ['100','50','25','20','10','Batch Apagado','Batch por numero personalizado','Batch por monto']
print 'Moneda Actual:' + currencies[actualcurr]
print 'Modo de conteo:' + Modos[modeindex]
print 'Modo de batch:' + Lote[batchindex]
print 'Cantidad de monedas instaladas: ' + str(currn-2)
print 'Estado de bolsillo de rechazo: ' + BosilloR[sensores[7]]
print 'Estado de bandeja de entrada: ' + BosilloR[sensores[5]]
print 'Estado de apilador: ' + BosilloR[sensores[6]]
print 'Estado de puerta superior: ' + Puerta[sensores[0]]
print 'Estado de apilador: ' + Puerta[sensores[2]]

# print sensores
# print statusraw
# print status
# # print cant_batch
# # print statusraw
# # print status