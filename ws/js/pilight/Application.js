Ext.define('pilight.Application', {
    init:function(){
        var typemap = {
            'SubMaster' : 'pilight.submaster.Panel',
            'ShowManager' : 'pilight.showrunner.Panel',
            'ColorWheel' : 'pilight.show.colorwheel.Panel',
            'Messaging' : 'pilight.messaging.Panel'
        }

        var windows = {};

        var generateWindow = function(controllable){
            var type = controllable.type;
            var id = controllable.id;
            if (typeof(typemap[type]) == 'undefined') return;
            var win = Ext.create('Ext.window.Window', {
                layout:'fit',
                title:type,
                stateful:true,
                stateId:id,
                items:[
                    Ext.create(typemap[type], {
                        socket:socket
                    })
                ]
            });
            win.show()

            windows[id] = win;
        };

        var socket;
        var connectWin = Ext.create('pilight.ConnectWindow', {
            connectionHandler:function(host, port){
                connectWin.setLoading('Connecting');

                socket = Ext.create('pilight.socket.Socket', {
                    host:host,
                    port:port
                });

                socket.on('connect', function(){
                    connectWin.setLoading(false);
                    connectWin.hide();

                    socket.sendCommand({'command':'getControllables'}, function(data){
                        data.forEach(generateWindow);

                        socket.listen('controlserver', {
                            receiveEvent:function(data){
                                for (var key in data) {
                                    switch (key) {
                                        case 'add':
                                            generateWindow(data[key]);
                                            break;
                                        case 'remove':
                                            var id = data[key]['id'];
                                            var win = windows[id];
                                            if (win) {
                                                win.close();
                                                delete(windows[id]);
                                            }
                                            break;
                                    }
                                }
                            }
                        });
                    });
                });
            }
        });
        connectWin.show();        
    }
});
