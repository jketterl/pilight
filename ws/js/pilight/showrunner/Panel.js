Ext.define('pilight.showrunner.Show', {
    extend:'Ext.data.Model',
    fields:[
        {name:'id'},
        {name:'name'}
    ]
});

Ext.define('pilight.showrunner.Panel', {
    extend:'Ext.grid.Panel',
    store:Ext.data.Store({
        model:'pilight.showrunner.Show',
        data:[]
    }),
    columns:[
        {'header':'Name', dataIndex:'name', flex:1}
    ],
    initComponent:function(){
        var me = this;

        me.socket.sendCommand({module:'showmanager', command:'getShows'}, function(data){
            data.forEach(function(data){
                var show = Ext.create('pilight.showrunner.Show', data);
                me.store.add(show);
            });
        });

        var startshow = function(show) {
            me.socket.sendCommand({module:'showmanager', command:'startShow', params:{id:show.get('id')}}); 
        };

        me.dockedItems = [{
            dock:'top',
            ui:'toolbar',
            items:[{
                xtype:'button',
                text:'Show starten',
                handler:function(){
                    var show = me.getSelectionModel().getSelection()[0];
                    startshow(show);
                }
            },{
                xtype:'button',
                text:'Show stoppen',
                handler:function(){
                    me.socket.sendCommand({module:'showmanager', command:'stopShow'});
                }
            }]
        }];

        me.on('itemdblclick', function(grid, show) {
            startshow(show);
        });

        me.callParent(arguments);
    }
});
