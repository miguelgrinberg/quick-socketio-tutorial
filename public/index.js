const sio = io();

sio.on('connect', () => {
  console.log('connected');
});

sio.on('disconnect', () => {
  console.log('disconnected');
});
