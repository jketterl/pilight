Ext.define('pilight.showrunner.Show', {
    extend:'Ext.data.Model',
    fields:[
        {name:'id'},
        {name:'name'},
        {name:'running', type:'boolean'}
    ]
});

Ext.define('pilight.showrunner.Panel', {
    extend:'Ext.grid.Panel',
    store:Ext.data.Store({
        model:'pilight.showrunner.Show',
        data:[]
    }),
    columns:[
        {header:'Name', dataIndex:'name', flex:1},
        {header:'', dataIndex:'running', width:50, renderer:function(v){
            if (v) return 'ON';
            return '';
        }}
    ],
    width:250,
    height:300,
    initComponent:function(){
        var me = this;

        me.socket.sendCommand({module:'showmanager', command:'getShows'}, function(data){
            data.forEach(function(data){
                var show = Ext.create('pilight.showrunner.Show', data);
                me.store.add(show);
            });
        });

        me.socket.listen('showmanager', me);

        var startShow = function(show) {
            me.socket.sendCommand({module:'showmanager', command:'startShow', params:{id:show.get('id')}}); 
        };
        var stopShow = function(show) {
            me.socket.sendCommand({module:'showmanager', command:'stopShow', params:{id:show.get('id')}});
        };

        me.dockedItems = [{
            dock:'top',
            ui:'toolbar',
            items:[{
                xtype:'button',
                text:'Show starten',
                handler:function(){
                    var show = me.getSelectionModel().getSelection()[0];
                    startShow(show);
                }
            },{
                xtype:'button',
                text:'Show stoppen',
                handler:function(){
                    var show = me.getSelectionModel().getSelection()[0];
                    stopShow(show);
                }
            },{
                xtype:'button',
                text:'Alle Shows stoppen',
                handler:function(){
                    me.socket.sendCommand({module:'showmanager', command:'stopAllShows'});
                }
            }]
        }];

        me.on('itemdblclick', function(grid, show) {
            var fn = show.get('running') ? stopShow : startShow;
            fn(show);
        });

        me.callParent(arguments);
    },
    receiveEvent:function(data){
        var me = this;
        var show;
        if (data.show) {
            var show = me.store.getById(data.show);
            show.set('running', data.running || false);
            show.commit();
        }
    }
});
