import serial

# Configuracion del puerto serial
com_serial = serial.Serial('/dev/ttyUSB0', timeout=1, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=False, rtscts=False, dsrdtr=False)

# Declaracion de listas
status = []
statusraw = []
statisticsraw = []
statistics = []
statdata=[]

# Declaracion de comandos
CMD_PC_CTRL_START = [0x02,0x02,0x01,0x01,0x03,0xFB]
CMD_PC_CTRL_STOP = [0x02,0x01,0x02,0x03,0xFC]
CMD_PC_CTRL_STATISTICS = [0x02,0x02,0x20,0x00,0x03,0xDD]

# Declarcion de listas para interpretar los datos
BosilloR = ['Libre','Ocupado']
Puerta = ['Cerrada','Abierta']
Modos = ['Mezcla','Denominacion','Cuentanotas','Cara','Orientacion','Issue','Serial','Separate','Barcode','Barcode + Efectivo','','Dissue']
Lote = ['100','50','25','20','10','Batch Apagado','Batch por numero personalizado','Batch por monto']

#Send CMD_PC_CTRL_STOP
com_serial.write(serial.to_bytes(CMD_PC_CTRL_STOP))

#Send CMD_PC_CTRL_START
com_serial.write(serial.to_bytes(CMD_PC_CTRL_START))

# Lectura de datos recibidos DEVICE STATUS y SENSOR STATUS
read_byte = com_serial.read()
statusraw.append(read_byte)
status.append(int.from_bytes(read_byte, "big"))
while read_byte is not None:
    read_byte = com_serial.read()
    if read_byte == b'':
        read_byte = None
        break
    statusraw.append(read_byte)
    status.append(int.from_bytes(read_byte, "big"))

# Separacion de los resultados leidos en DEVICE y SENSOR
l = len(statusraw)
length1 = status[1]
device = status[0:length1+4]
sensor = status[length1+4:l]

# Envio de solicitud de STATISTICS
com_serial.write(serial.to_bytes(CMD_PC_CTRL_STATISTICS))

# Lectura de datos recibidos STATISTICS
read_byte = com_serial.read()
statistics.append(int.from_bytes(read_byte, "big"))
statisticsraw.append(read_byte)
while read_byte is not None:
    read_byte = com_serial.read()
    if read_byte == b'':
        read_byte = None
        break
    statisticsraw.append(read_byte)
    statistics.append(int.from_bytes(read_byte, "big"))

# Envio solicitud CMD_PC_CTRL_STOP
com_serial.write(serial.to_bytes(CMD_PC_CTRL_STOP))

# Tratamiento de datos DEVICE STATUS
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

# Tratamiento datos SENSOR STATUS
sensores = [0,0,0,0,0,0,0,0]
sensorstatus = sensor[3]
i=0
while sensorstatus // 2 != 0:
    sensores[i]=sensorstatus % 2
    sensorstatus = sensorstatus // 2
    i = i + 1
    if sensorstatus == 1:
        sensores[i]=sensorstatus % 2

# Tratamiento datos STATISTICS
statdata = statistics[3:statistics[1]+2]
totalcount = (statdata[0]<<24 | statdata[1]<<16 | statdata[2]<<8 | statdata[3])


print ('Moneda Actual:' + currencies[actualcurr])
print ('Modo de conteo:' + Modos[modeindex])
print ('Modo de batch:' + Lote[batchindex])
# print (totalcount)
# print ('Cantidad de monedas instaladas: ' + str(currn-2))
# print ('Estado de bolsillo de rechazo: ' + BosilloR[sensores[7]])
# print ('Estado de bandeja de entrada: ' + BosilloR[sensores[5]])
# print ('Estado de apilador: ' + BosilloR[sensores[6]])
# print ('Estado de puerta superior: ' + Puerta[sensores[0]])
# print ('Estado de inferior: ' + Puerta[sensores[2]])