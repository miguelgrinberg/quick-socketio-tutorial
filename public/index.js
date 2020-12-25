const sio = io();

sio.on('connect', () => {
  console.log('connected');
  sio.emit('sum', {numbers: [1, 2]}, (result) => {
    console.log(result);
  });
});

sio.on('disconnect', () => {
  console.log('disconnected');
});

sio.on('mult', (data, cb) => {
  const result = data.numbers[0] * data.numbers[1];
  cb(result);
});

sio.on('client_count', (count) => {
  console.log('There are ' + count + ' connected clients.');
});

sio.on('room_count', (count) => {
  console.log('There are ' + count + ' clients in my room.');
});
